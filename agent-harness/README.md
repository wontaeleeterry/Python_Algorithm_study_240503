# agent-harness

Claude Code 용 범용 Planner / Generator / Evaluator 하네스.

## 구조
```
agent-harness/
├── CLAUDE.md
├── README.md
├── install.sh                      # 다른 프로젝트에 설치
├── .claude/
│   ├── settings.json
│   ├── agents/   planner.md  generator.md  evaluator.md
│   └── commands/ build.md  change.md  evaluate.md
└── harness/
    ├── project.md                  # ★ 작업마다 이 파일만 수정
    ├── templates/ spec / handoff / report
    ├── examples/  todo-cli.project.md  python-lib.project.md  node-api.project.md
    └── runs/                       # 실행 기록 (자동 생성)
```

## 빠른 시작
1. 하네스를 작업 프로젝트에 설치: `./install.sh /path/to/my-project`
2. `harness/project.md` 를 내 작업에 맞게 수정 (또는 `examples/` 에서 복사)
3. 프로젝트 디렉터리에서 `claude` 실행 → `/build "요구사항"` 또는 `/change "변경 요청"`
4. 결과는 `harness/runs/<run-id>/reports/` 에서 확인
