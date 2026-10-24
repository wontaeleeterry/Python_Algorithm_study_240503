# Project Config

## 1. 프로젝트 개요
- 이름: my-api
- 한 줄 설명: Express 기반 REST API

## 2. 기술 스택
- 언어/런타임: Node 20, TypeScript
- 프레임워크/라이브러리: express, vitest
- 의존성 정책: 추가 시 spec 에 사유 명시

## 3. 경로
- source_paths: `src/`
- test_paths: `test/`
- readonly_paths: `prisma/migrations/`

## 4. 명령어
- install_command: `npm ci`
- test_command: `npm test`
- run_command: `npm run dev`
- lint_command: `npm run lint`
- build_command: `npm run build`

## 5. 반복 / 품질 기준
- max_iterations: 3
- 최소 요건: build 성공, test 전부 통과, lint 오류 0
- 테스트 정책: 엔드포인트마다 정상/오류 케이스 각 1개 이상

## 6. 제약·금지 사항
- 비밀값 하드코딩 금지, .env 읽기 금지

## 7. 코딩 컨벤션 / 참고 문서
- 기존 폴더 구조(routes/services/repositories) 유지

## 8. 테스트 불가 작업일 때
- 해당 없음
