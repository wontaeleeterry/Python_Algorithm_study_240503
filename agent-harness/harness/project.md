# Project Config  ★ 작업마다 이 파일만 수정하세요

## 1. 프로젝트 개요
- 이름:
- 한 줄 설명:

## 2. 기술 스택
- 언어/런타임:
- 프레임워크/라이브러리:
- 의존성 정책: (예: 표준 라이브러리만 / 기존 package.json 의존성만 / 추가 시 spec 에 사유 명시)

## 3. 경로
- source_paths: (생성자가 구현할 위치. 예: `src/`)
- test_paths: (예: `tests/`)
- readonly_paths: (수정 금지. 예: `vendor/`, `migrations/`)

## 4. 명령어 (평가자가 그대로 실행함)
- install_command: (없으면 `none`)
- test_command: (예: `PYTHONPATH=src python3 -m unittest discover -s tests -v`)
- run_command: (예: `PYTHONPATH=src python3 -m myapp`)
- lint_command: (없으면 `none`)
- build_command: (없으면 `none`)

## 5. 반복 / 품질 기준
- max_iterations: 3
- 최소 요건: 모든 FR 수용 기준 충족, test_command 전부 통과, lint 오류 0
- 테스트 정책: (예: FR 마다 최소 1개 테스트 / 외부 네트워크 금지 / 임시 디렉터리 사용)

## 6. 제약·금지 사항
- (예: 실제 홈 디렉터리 쓰기 금지, 비밀키 하드코딩 금지, 공개 API 시그니처 변경 금지)

## 7. 코딩 컨벤션 / 참고 문서
- (예: PEP8, 기존 모듈 구조 따르기, `docs/architecture.md`)

## 8. 테스트 불가 작업일 때 (선택)
- 코드가 아닌 산출물(문서, 설정, 스크립트)이면 평가자가 사용할 **검증 체크리스트**를 여기에 적는다.
