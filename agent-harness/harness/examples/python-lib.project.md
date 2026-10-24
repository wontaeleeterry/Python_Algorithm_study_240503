# Project Config

## 1. 프로젝트 개요
- 이름: my-lib
- 한 줄 설명: (기존 Python 라이브러리 — 기능 추가/버그 수정용)

## 2. 기술 스택
- 언어/런타임: Python 3.11
- 프레임워크/라이브러리: pyproject.toml 에 명시된 의존성만
- 의존성 정책: 새 의존성 추가 금지

## 3. 경로
- source_paths: `src/my_lib/`
- test_paths: `tests/`
- readonly_paths: `docs/`, `CHANGELOG.md`

## 4. 명령어
- install_command: `pip install -e .[dev]`
- test_command: `pytest -q`
- run_command: none
- lint_command: `ruff check .`
- build_command: none

## 5. 반복 / 품질 기준
- max_iterations: 3
- 최소 요건: 기존 테스트 전부 통과(회귀 0), 신규 기능 테스트 추가, ruff 오류 0
- 테스트 정책: 버그 수정은 실패를 재현하는 테스트를 먼저 추가

## 6. 제약·금지 사항
- 공개 API 시그니처 변경 금지 (변경 필요 시 spec 에 명시하고 사용자 확인)

## 7. 코딩 컨벤션 / 참고 문서
- 기존 코드 스타일을 따른다

## 8. 테스트 불가 작업일 때
- 해당 없음
