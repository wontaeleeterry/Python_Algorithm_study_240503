# 범용 3-에이전트 하네스 (Planner / Generator / Evaluator)

어떤 코드·작업에도 재사용할 수 있는 멀티 에이전트 하네스입니다.
**작업별로 바뀌는 정보는 전부 `harness/project.md` 한 파일에만 둡니다.** 에이전트 정의는 수정하지 않습니다.

## 명령어
| 명령 | 용도 |
|---|---|
| `/build <요구사항>` | 새로 만들기 (planner → generator ⇄ evaluator) |
| `/change <변경 요청>` | 기존 코드 수정·기능 추가 (회귀 방지 포함) |
| `/evaluate [run-id]` | 평가자만 단독 실행 (현재 코드 점검) |

## 에이전트 (`.claude/agents/`)
| 에이전트 | 하는 일 | 쓰기 범위 |
|---|---|---|
| `planner` | 요구사항 → 검증 가능한 명세와 태스크 | `RUN_DIR/spec.md` 만 |
| `generator` | 명세 구현 + 테스트 | `project.md` 의 소스/테스트 경로, `RUN_DIR/handoff.md` |
| `evaluator` | 독립 검증 + PASS/FAIL | `RUN_DIR/reports/` 만 |

## 공통 규칙
- 에이전트는 시작할 때 **반드시 `harness/project.md` 를 먼저 읽는다.** (스택, 경로, 실행/테스트 명령, 제약)
- 메인 세션이 호출 시 **`RUN_DIR`(이번 실행의 폴더)** 를 프롬프트로 전달한다. 에이전트는 그 폴더만 쓴다.
- 에이전트 간 소통은 **파일로만** 한다: `spec.md` → `handoff.md` → `reports/report-N.md`
- 평가자는 코드를 수정하지 않는다. 생성자는 스스로 합격 판정하지 않는다.
- 판정은 보고서 첫 줄 `VERDICT: PASS|FAIL` 로만 한다. 최대 반복은 `project.md` 의 `max_iterations`.

## 실행 기록 구조
```
harness/runs/<YYYYMMDD-HHMM-slug>/
├── request.md        # 원본 요청
├── spec.md           # 플래너 산출
├── handoff.md        # 생성자 인수인계 (덮어씀)
└── reports/report-1.md, report-2.md ...
```
