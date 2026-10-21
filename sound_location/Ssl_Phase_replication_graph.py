#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2채널(마이크 2개) wav 파일로부터 다중 음원 DoA(도래각)를 추정하는 구현.

참고 논문:
  H. Song and J. W. Shin, "Multiple Sound Source Localization Based on
  Interchannel Phase Differences in All Frequencies with Spectral Masks,"
  Interspeech 2021.
  (기반 방법: K. Chen et al., "Robust phase replication method for spatial
   aliasing problem in multiple sound sources localization," WASPAA 2017)

처리 흐름 (논문 Figure 1)
  X1, X2 (STFT)
    -> 잡음 PSD 추정 -> 국소 SNR 마스크 M_SNR            (식 8, 9)
    -> 코히어런스 마스크 M_coh                            (식 10~12)
    -> M_TF = M_SNR * M_coh                               (식 13)
    -> IPD 계산 및 replicated IPD(위상 복제) -> DoA 후보   (식 1, 4, 5, 6)
    -> 가중 투표 히스토그램 h_prop (bin당 1/(2A_k+1))      (식 14)
    -> LPC 스무딩 -> 피크 탐색 (임계 beta, 최대 P_N개)

각도 부호 규칙
  wav의 채널 1(좌)을 primary(X1), 채널 2(우)를 secondary(X2)로 본다.
  IPD = angle(X1 * conj(X2) ) > 0  <=> 소리가 채널 1(좌) 마이크에 먼저 도달
  => 양(+)의 각도 = 채널 1(좌) 쪽, 음(-)의 각도 = 채널 2(우) 쪽
  (broadside 방향, 즉 두 마이크를 잇는 선에 수직인 방향이 0도)
  부호가 반대로 나오면 --flip 옵션을 사용.

사용 예
  python ssl_phase_replication.py input.wav --mic-distance 0.14 --plot
  python ssl_phase_replication.py input.wav -d 0.14 --polar          # 방사형 그래프 저장
  python ssl_phase_replication.py input.wav -d 0.14 --polar --no-mirror
"""

import argparse
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft, lfilter, find_peaks, freqz
from scipy.linalg import solve_toeplitz

SPEED_OF_SOUND = 343.0  # [m/s]


# ----------------------------------------------------------------------------
# 입출력
# ----------------------------------------------------------------------------
def read_stereo_wav(path):
    """2채널 wav를 읽어 float64 (x1, x2, fs)로 반환."""
    fs, data = wavfile.read(path)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError("입력은 2채널(스테레오) wav 파일이어야 합니다.")
    if data.shape[1] > 2:
        print(f"[경고] {data.shape[1]}채널 파일입니다. 앞의 2채널만 사용합니다.")
    if np.issubdtype(data.dtype, np.integer):
        data = data.astype(np.float64) / np.iinfo(data.dtype).max
    else:
        data = data.astype(np.float64)
    return data[:, 0], data[:, 1], fs


# ----------------------------------------------------------------------------
# 잡음 PSD 추정 (논문 [14] Gerkmann & Hendriks의 MMSE 기반 방식의 간략 구현)
# ----------------------------------------------------------------------------
def estimate_noise_psd(X, alpha_pH1=0.9, alpha_psd=0.8, xi_h1_db=15.0,
                       prior_h1=0.5, n_init=5):
    """
    음성 존재 사후확률 P(H1|y)를 이용한 재귀적 잡음 전력 추정.
      E[N | y] = P(H1|y) * sigma_prev + P(H0|y) * |y|^2
    (원 논문의 bias 보정 상수는 생략한 간략 버전)
    X: (F, T) 복소 STFT  ->  반환: (F, T) 잡음 전력 추정치
    """
    P = np.abs(X) ** 2
    F, T = P.shape
    eps = 1e-12
    xi = 10.0 ** (xi_h1_db / 10.0)
    prior_ratio = (1.0 - prior_h1) / prior_h1

    noise = P[:, :min(n_init, T)].mean(axis=1) + eps
    pH1_mean = np.full(F, 0.5)
    out = np.empty_like(P)
    for t in range(T):
        y = P[:, t]
        snr_post = y / np.maximum(noise, eps)
        pH1 = 1.0 / (1.0 + prior_ratio * (1.0 + xi) *
                     np.exp(-snr_post * xi / (1.0 + xi)))
        pH1_mean = alpha_pH1 * pH1_mean + (1.0 - alpha_pH1) * pH1
        # 'stuck' 방지: 장기 평균이 너무 높으면 확률 상한을 둔다
        pH1 = np.where(pH1_mean > 0.99, np.minimum(pH1, 0.99), pH1)
        est = pH1 * noise + (1.0 - pH1) * y
        noise = alpha_psd * noise + (1.0 - alpha_psd) * est
        out[:, t] = np.maximum(noise, eps)
    return out


# ----------------------------------------------------------------------------
# 스펙트럼 마스크 (식 8 ~ 13)
# ----------------------------------------------------------------------------
def snr_mask(X1, X2, lambda_th_db=5.0):
    """식 (8),(9): 두 채널 중 더 낮은 국소 SNR이 임계값보다 큰 bin만 1."""
    Pv1 = estimate_noise_psd(X1)
    Pv2 = estimate_noise_psd(X2)
    lam = np.minimum(np.abs(X1) ** 2 / Pv1 - 1.0,
                     np.abs(X2) ** 2 / Pv2 - 1.0)
    lam_db = 10.0 * np.log10(np.maximum(lam, 1e-10))
    return (lam_db > lambda_th_db).astype(np.float64)


def _causal_mean(a, C):
    """식 (12): 현재 프레임 포함 과거 C+1 프레임 이동평균 (시간축 = axis 1)."""
    return lfilter(np.ones(C + 1) / (C + 1), [1.0], a, axis=1)


def coherence_mask(X1, X2, gamma_th=0.9, C=5):
    """식 (10),(11): 두 마이크 신호의 코히어런스가 임계값보다 큰 bin만 1."""
    cross = _causal_mean(X1 * np.conj(X2), C)
    p1 = _causal_mean(np.abs(X1) ** 2, C)
    p2 = _causal_mean(np.abs(X2) ** 2, C)
    gamma = np.abs(cross) / np.sqrt(np.maximum(p1 * p2, 1e-20))
    return (gamma > gamma_th).astype(np.float64)


# ----------------------------------------------------------------------------
# Replicated IPD -> DoA 후보 -> 가중 투표 히스토그램 (식 4 ~ 7, 14)
# ----------------------------------------------------------------------------
def build_doa_histogram(ipd, mask, fs, nfft, d, c=SPEED_OF_SOUND,
                        grid_step=5.0, equal_weight=True, f_min=0.0):
    """
    ipd : (F, T)  관측 IPD  (F = nfft//2 + 1, DC 포함)
    mask: (F, T)  M_TF (0/1)
    equal_weight=True  -> 제안 방법 (식 14): 각 bin 가중치 1/(2A_k+1)
    equal_weight=False -> 기존 phase replication [13]: 가중치 1 (모든 후보 동등)
    반환: (grid[deg], hist)
    """
    F = ipd.shape[0]
    k = np.arange(F)
    freqs = k * fs / nfft

    # 식 (3): 공간 에일리어싱이 시작되는 주파수 f_a0 = c/(2d) 와 해당 bin 인덱스
    f_a0 = c / (2.0 * d)
    N_a0 = f_a0 / (fs / nfft)

    # 식 (5): k번째 bin의 최대 unwrapping 횟수 A_k
    A = np.ceil((k - N_a0) / (2.0 * N_a0)).astype(int)
    A = np.maximum(A, 0)
    A_max = int(A.max())

    valid_freq = (k >= 1) & (freqs >= f_min)       # DC bin 제외 (식 6에서 f_k=0)
    grid = np.arange(-90.0, 90.0 + 1e-9, grid_step)
    nb = len(grid)
    hist = np.zeros(nb)

    safe_f = np.where(freqs > 0, freqs, 1.0)[:, None]
    weight_k = (1.0 / (2 * A + 1)) if equal_weight else np.ones(F)
    weight_mat = np.broadcast_to(weight_k[:, None], ipd.shape)

    base_ok = (mask > 0) & valid_freq[:, None]

    # 식 (4): l = -A_k ... +A_k 만큼 2*pi*l 을 더한 위상차 후보
    for l in range(-A_max, A_max + 1):
        ok = base_ok & (A >= abs(l))[:, None]
        cand = ipd + 2.0 * np.pi * l
        sin_t = c * cand / (2.0 * np.pi * safe_f * d)        # 식 (2)를 sin(theta)로 정리
        ok &= np.abs(sin_t) <= 1.0                            # 물리적으로 불가능한 후보 제거
        if not ok.any():
            continue
        theta = np.degrees(np.arcsin(sin_t[ok]))              # 식 (6)
        idx = np.clip(np.round((theta + 90.0) / grid_step).astype(int), 0, nb - 1)
        hist += np.bincount(idx, weights=weight_mat[ok], minlength=nb)
    return grid, hist


# ----------------------------------------------------------------------------
# LPC 스무딩 + 피크 탐색 ([15],[16] 방식)
# ----------------------------------------------------------------------------
def lpc_smooth(h, order=10):
    """히스토그램을 한쪽 스펙트럼으로 보고 LPC(all-pole) 포락선으로 스무딩."""
    nb = len(h)
    if h.max() <= 0:
        return h.copy()
    order = min(order, nb - 2)
    r = np.fft.irfft(h)[:order + 1]               # 파워 스펙트럼 -> 자기상관
    r[0] *= (1.0 + 1e-9)
    try:
        a = solve_toeplitz(r[:order], -r[1:order + 1])
    except np.linalg.LinAlgError:
        return h.copy()
    A = np.concatenate(([1.0], a))
    gain = max(r[0] + a @ r[1:order + 1], 1e-20)
    _, H = freqz([1.0], A, worN=np.linspace(0, np.pi, nb))
    env = gain * np.abs(H) ** 2
    return env / env.max() * h.max()


def peak_search(h_s, grid, beta=0.5, max_sources=2):
    """
    가장 높은 피크 -> 첫 음원.
    다음 피크가 (beta * 직전에 채택된 피크 높이)보다 크면 음원 수를 1 증가.
    임계값 미만이거나 max_sources에 도달하면 종료.
    """
    padded = np.pad(h_s, 1, mode="constant")      # 양 끝(+-90도)도 피크 후보로 허용
    pk, _ = find_peaks(padded)
    pk = pk - 1
    if len(pk) == 0:
        return []
    pk = pk[np.argsort(h_s[pk])[::-1]]            # 높이 내림차순
    est = [pk[0]]
    for p in pk[1:]:
        if len(est) >= max_sources:
            break
        if h_s[p] > beta * h_s[est[-1]]:
            est.append(p)
        else:
            break
    return [float(grid[i]) for i in est]


# ----------------------------------------------------------------------------
# 전체 파이프라인
# ----------------------------------------------------------------------------
def localize(x1, x2, fs, mic_distance=0.14, nfft=512, hop=None,
             lambda_th_db=5.0, gamma_th=0.9, C=5, beta=0.5, max_sources=2,
             grid_step=5.0, lpc_order=10, use_masks=True, equal_weight=True,
             f_min=0.0, flip=False):
    """
    반환: dict(doas, grid, hist, hist_smooth, mask)
    """
    hop = hop or nfft // 2
    _, _, X1 = stft(x1, fs, window="hann", nperseg=nfft, noverlap=nfft - hop,
                    boundary=None, padded=False)
    _, _, X2 = stft(x2, fs, window="hann", nperseg=nfft, noverlap=nfft - hop,
                    boundary=None, padded=False)

    ipd = np.angle(X1 * np.conj(X2))              # 식 (1)

    if use_masks:
        m_snr = snr_mask(X1, X2, lambda_th_db)    # 식 (8),(9)
        m_coh = coherence_mask(X1, X2, gamma_th, C)  # 식 (10)~(12)
        mask = m_snr * m_coh                      # 식 (13)
    else:
        mask = np.ones_like(ipd)

    grid, hist = build_doa_histogram(ipd, mask, fs, nfft, mic_distance,
                                     grid_step=grid_step,
                                     equal_weight=equal_weight, f_min=f_min)
    hist_s = lpc_smooth(hist, lpc_order) if lpc_order > 0 else hist.copy()
    doas = peak_search(hist_s, grid, beta, max_sources)

    if flip:
        doas = [-a for a in doas]
        grid, hist, hist_s = -grid[::-1], hist[::-1], hist_s[::-1]
    return dict(doas=doas, grid=grid, hist=hist, hist_smooth=hist_s, mask=mask)


# ----------------------------------------------------------------------------
# 방사형(polar) 시각화: 마이크 2개 + 추정 음원 방향
# ----------------------------------------------------------------------------
def plot_polar(doas, mic_distance, grid=None, hist=None,
               out_path="doa_polar.png", show_mirror=True):
    """
    위에서 내려다본(top view) 방사형 그래프를 PNG로 저장.

      - 0도(위쪽) = 정면(broadside), +각도 = 왼쪽(ch1), -각도 = 오른쪽(ch2)
      - 마이크: 중심에서 좌(ch1) / 우(ch2) 로 배치 (크기는 실제 비율이 아님)
      - 음원: DoA만 추정되므로 거리는 알 수 없고, 반지름 1.0 위에 방향만 표시
      - 마이크가 2개뿐이면 앞/뒤를 구분할 수 없으므로(front-back ambiguity)
        뒤쪽 대칭 위치(180도 - theta)를 속이 빈 연한 별표로 함께 표시
      - grid/hist를 주면 (스무딩된) DoA 히스토그램을 연한 음영으로 겹쳐 그림
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_zero_location("N")      # 0도 = 정면(위)
    ax.set_theta_direction(1)            # 반시계 방향 = +  (왼쪽 = ch1 쪽)
    ax.set_ylim(0, 1.3)
    ax.set_rgrids([1.0], labels=[""])    # 음원 방향이 표시되는 기준 원
    ax.set_thetagrids(np.arange(0, 360, 30),
                      labels=[f"{a if a <= 180 else a - 360}°" for a in range(0, 360, 30)])
    ax.grid(alpha=0.35)

    # DoA 히스토그램 (선택)
    if grid is not None and hist is not None and np.max(hist) > 0:
        hn = np.asarray(hist, dtype=float) / np.max(hist)
        ax.fill_between(np.radians(grid), 0.2, 0.2 + 0.7 * hn,
                        color="tab:blue", alpha=0.15, label="DoA histogram (smoothed)")

    # 마이크 위치 (좌: ch1 = +90도, 우: ch2 = -90도)
    r_m = 0.12
    ax.plot([np.pi / 2, np.pi / 2, -np.pi / 2, -np.pi / 2], [r_m, 0, 0, r_m],
            color="k", lw=1.5, zorder=3)                       # 마이크 축(중심 경유)
    ax.plot([np.pi / 2, -np.pi / 2], [r_m, r_m], "s", ms=10, color="k", zorder=4)
    lbl = dict(ha="center", va="center", fontsize=10, fontweight="bold", zorder=7,
               bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.5))
    ax.text(np.pi / 2, 0.42, "Mic 1\n(ch1, L)", **lbl)
    ax.text(-np.pi / 2, 0.42, "Mic 2\n(ch2, R)", **lbl)

    # 방향 표지
    ax.text(0, 1.2, "FRONT", ha="center", va="center", fontsize=9, color="gray")
    ax.text(np.pi, 1.2, "BACK", ha="center", va="center", fontsize=9, color="gray")

    # 추정 음원
    colors = ["tab:red", "tab:green", "tab:orange", "tab:purple", "tab:brown"]
    for i, a in enumerate(doas):
        col = colors[i % len(colors)]
        th = np.radians(a)
        ax.annotate("", xy=(th, 0.97), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2), zorder=5)
        ax.plot([th], [1.0], "*", ms=20, color=col, zorder=6,
                label=f"Source #{i + 1}: {a:+.1f}°")
        if show_mirror:
            ax.plot([np.radians(180.0 - a)], [1.0], "*", ms=15, mfc="none",
                    mec=col, alpha=0.5, zorder=5)
    if doas and show_mirror:
        ax.plot([], [], "*", ms=12, mfc="none", mec="gray", ls="",
                label="Front-back mirror (ambiguous)")

    ax.set_title("Estimated source directions (top view)", pad=22)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=2, frameon=False)
    fig.text(0.5, 0.01,
             f"mic distance d = {mic_distance * 100:.1f} cm (mic markers not to scale; "
             "source distance unknown, shown on unit circle)",
             ha="center", fontsize=8, color="gray")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="2-mic 다중 음원 DoA 추정 (Song & Shin, Interspeech 2021)")
    ap.add_argument("wav", help="2채널 wav 파일 (ch1=좌, ch2=우)")
    ap.add_argument("--mic-distance", "-d", type=float, default=0.14, help="마이크 간 거리 [m] (기본 0.14)")
    ap.add_argument("--nfft", type=int, default=512, help="FFT 크기 (기본 512, 16kHz에서 K=257)")
    ap.add_argument("--hop", type=int, default=None, help="hop 크기 (기본 nfft/2)")
    ap.add_argument("--lambda-th", type=float, default=5.0, help="SNR 마스크 임계값 [dB]")
    ap.add_argument("--gamma-th", type=float, default=0.9, help="코히어런스 임계값")
    ap.add_argument("--C", type=int, default=5, help="코히어런스 평균 프레임 수 C")
    ap.add_argument("--beta", type=float, default=0.5, help="피크 임계 비율 beta")
    ap.add_argument("--max-sources", type=int, default=2, help="최대 음원 수 P_N")
    ap.add_argument("--grid-step", type=float, default=5.0, help="히스토그램 각도 간격 [deg]")
    ap.add_argument("--lpc-order", type=int, default=10, help="LPC 스무딩 차수 (0이면 사용 안함)")
    ap.add_argument("--no-mask", action="store_true", help="스펙트럼 마스크 비활성화")
    ap.add_argument("--conventional", action="store_true",
                    help="가중 투표 대신 기존 phase replication [13] 방식 히스토그램 사용")
    ap.add_argument("--flip", action="store_true", help="각도 부호 반전 (좌/우 정의가 반대일 때)")
    ap.add_argument("--plot", action="store_true", help="히스토그램을 PNG로 저장")
    ap.add_argument("--polar", action="store_true",
                    help="마이크 2개와 추정 음원 방향을 방사형 그래프(PNG)로 저장")
    ap.add_argument("--polar-out", default=None, help="방사형 그래프 저장 경로 (기본: <wav>_doa_polar.png)")
    ap.add_argument("--no-mirror", action="store_true", help="방사형 그래프에서 앞/뒤 대칭 위치 표시 생략")
    args = ap.parse_args()

    x1, x2, fs = read_stereo_wav(args.wav)
    res = localize(x1, x2, fs, mic_distance=args.mic_distance, nfft=args.nfft,
                   hop=args.hop, lambda_th_db=args.lambda_th,
                   gamma_th=args.gamma_th, C=args.C, beta=args.beta,
                   max_sources=args.max_sources, grid_step=args.grid_step,
                   lpc_order=args.lpc_order, use_masks=not args.no_mask,
                   equal_weight=not args.conventional, flip=args.flip)

    print(f"fs = {fs} Hz, 길이 = {len(x1) / fs:.2f} s, 마이크 간격 = {args.mic_distance * 100:.1f} cm")
    print(f"마스크로 선택된 T-F bin 비율: {res['mask'].mean() * 100:.1f} %")
    if res["doas"]:
        print(f"추정된 음원 수: {len(res['doas'])}")
        for i, a in enumerate(res["doas"], 1):
            print(f"  음원 #{i}: {a:+.1f} deg  (+: ch1/좌 쪽, -: ch2/우 쪽)")
    else:
        print("음원을 찾지 못했습니다.")

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(res["grid"], res["hist"] / max(res["hist"].max(), 1e-12), label="histogram")
        ax.plot(res["grid"], res["hist_smooth"] / max(res["hist_smooth"].max(), 1e-12),
                label="LPC smoothed")
        for a in res["doas"]:
            ax.axvline(a, color="r", ls="--")
        ax.set_xlabel("Degree [deg]")
        ax.set_ylabel("Histogram (normalized)")
        ax.set_xlim(-90, 90)
        ax.legend()
        fig.tight_layout()
        out = args.wav.rsplit(".", 1)[0] + "_doa_hist.png"
        fig.savefig(out, dpi=130)
        print(f"히스토그램 저장: {out}")

    if args.polar:
        out = args.polar_out or (args.wav.rsplit(".", 1)[0] + "_doa_polar.png")
        plot_polar(res["doas"], args.mic_distance, res["grid"], res["hist_smooth"],
                   out_path=out, show_mirror=not args.no_mirror)
        print(f"방사형 그래프 저장: {out}")


if __name__ == "__main__":
    main()