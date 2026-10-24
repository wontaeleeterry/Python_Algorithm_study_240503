# Project Config

## 1. 프로젝트 개요
- 이름: todo-cli
- 한 줄 설명: JSON 파일에 저장하는 Python Todo CLI

## 2. 기술 스택
- 언어/런타임: Python 3.10+
- 프레임워크/라이브러리: argparse, json, pathlib, unittest
- 의존성 정책: 표준 라이브러리만

## 3. 경로
- source_paths: `src/todo_cli/`
- test_paths: `tests/`
- readonly_paths: `harness/`, `.claude/`

## 4. 명령어
- install_command: none
- test_command: `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- run_command: `PYTHONPATH=src python3 -m todo_cli`
- lint_command: none
- build_command: none

## 5. 반복 / 품질 기준
- max_iterations: 3
- 최소 요건: 모든 FR 수용 기준 충족, 테스트 전부 통과
- 테스트 정책: FR 마다 최소 1개, 저장소는 `TODO_FILE` 환경변수 + 임시 파일

## 6. 제약·금지 사항
- 실제 `~/.todo.json` 을 건드리지 않는다
- 종료코드: 성공 0, 사용자 오류 1, 사용법 오류 2

## 7. 코딩 컨벤션 / 참고 문서
- PEP8, 타입 힌트 사용

## 8. 테스트 불가 작업일 때
- 해당 없음
