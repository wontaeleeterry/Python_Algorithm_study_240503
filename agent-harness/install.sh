#!/usr/bin/env bash
# 사용법: ./install.sh /path/to/target-project
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DST="${1:?대상 프로젝트 경로를 지정하세요}"
[ -d "$DST" ] || { echo "디렉터리가 없습니다: $DST"; exit 1; }

mkdir -p "$DST/.claude/agents" "$DST/.claude/commands" \
         "$DST/harness/templates" "$DST/harness/examples" "$DST/harness/runs"

cp "$SRC"/.claude/agents/*.md   "$DST/.claude/agents/"
cp "$SRC"/.claude/commands/*.md "$DST/.claude/commands/"
cp "$SRC"/harness/templates/*   "$DST/harness/templates/"
cp "$SRC"/harness/examples/*    "$DST/harness/examples/"
touch "$DST/harness/runs/.gitkeep"

if [ ! -f "$DST/harness/project.md" ]; then
  cp "$SRC/harness/project.md" "$DST/harness/project.md"
  echo "✔ harness/project.md 생성 (직접 채워야 합니다)"
else
  echo "• harness/project.md 이미 존재 — 유지"
fi

if [ ! -f "$DST/.claude/settings.json" ]; then
  cp "$SRC/.claude/settings.json" "$DST/.claude/settings.json"
  echo "✔ .claude/settings.json 생성"
else
  echo "• .claude/settings.json 이미 존재 — 수동 병합 필요 (소스의 permissions 참고)"
fi

MARK="## 3-에이전트 하네스"
if [ -f "$DST/CLAUDE.md" ]; then
  if ! grep -q "$MARK" "$DST/CLAUDE.md"; then
    {
      echo; echo "$MARK"
      echo "- 작업 설정: \`harness/project.md\` (에이전트는 시작 시 항상 먼저 읽는다)"
      echo "- 명령: \`/build <요구사항>\`, \`/change <변경 요청>\`, \`/evaluate [run-id]\`"
      echo "- 실행 기록: \`harness/runs/<run-id>/\` (spec, handoff, reports)"
    } >> "$DST/CLAUDE.md"
    echo "✔ CLAUDE.md 에 하네스 섹션 추가"
  fi
else
  cp "$SRC/CLAUDE.md" "$DST/CLAUDE.md"
  echo "✔ CLAUDE.md 생성"
fi

echo
echo "완료. 다음 단계:"
echo "  1) $DST/harness/project.md 편집"
echo "  2) cd $DST && claude 재시작"
echo "  3) /build \"요구사항\"  또는  /change \"변경 요청\""
