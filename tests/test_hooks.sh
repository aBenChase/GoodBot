#!/bin/sh
# Regression tests for the Good Bot git hooks.
# Covers GB-R003 (renames) and GB-R004 (nested secrets) plus the core rules.
# Runs in a throwaway repo so it never touches the real index.
set -u

HOOKS_DIR=$(cd "$(dirname "$0")/../tools/git-hooks" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cd "$tmp" || exit 9

git init -q
git config core.hooksPath "$HOOKS_DIR"
git config user.email t@example.com
git config user.name tester
mkdir -p claude openai
printf 'x\n' > claude/a.md
printf 'y\n' > openai/b.md
git add claude/a.md openai/b.md
git commit -q -m "seed

Agent: shared"

pass=0; fail=0
check() { # desc  expected  actual
  if [ "$2" = "$3" ]; then pass=$((pass+1)); echo "ok   - $1";
  else fail=$((fail+1)); echo "FAIL - $1 (want $2 got $3)"; fi
}
precommit() { sh "$HOOKS_DIR/pre-commit" >/dev/null 2>&1; echo $?; }
commitmsg() { printf '%s' "$1" > "$tmp/msg"; sh "$HOOKS_DIR/commit-msg" "$tmp/msg" >/dev/null 2>&1; echo $?; }
reset_repo() { git reset -q --hard HEAD >/dev/null 2>&1; git clean -fdq >/dev/null 2>&1; }

# --- GB-R004: nested secrets blocked; positive control raw log blocked ---
mkdir -p openai/secrets; printf 'k\n' > openai/secrets/audit.txt
git add -f openai/secrets/audit.txt
check "GB-R004 nested secrets/ blocked" 1 "$(precommit)"; reset_repo

mkdir -p logs/raw; printf 'r\n' > logs/raw/x
git add -f logs/raw/x
check "control: logs/raw blocked" 1 "$(precommit)"; reset_repo

# --- GB-R003: rename into a protected path (privacy) ---
git mv claude/a.md logs-raw-tmp 2>/dev/null; mkdir -p logs/raw; git mv logs-raw-tmp logs/raw/a.md 2>/dev/null
check "GB-R003 rename into logs/raw blocked" 1 "$(precommit)"; reset_repo

# --- GB-R003: rename across ownership (claude -> openai) ---
git mv claude/a.md openai/a.md
check "GB-R003 rename claude->openai blocked for claude" 1 "$(commitmsg 'x

Agent: claude')"
check "GB-R003 same rename allowed with ack" 0 "$(commitmsg 'x

Agent: claude
Cross-Boundary-Ack: test')"
reset_repo

# --- core: trailer required; rich trailer tolerated (GB-R002 fix path) ---
mkdir -p shared; printf 'q\n' > shared/x.md; git add shared/x.md
check "missing trailer blocked" 1 "$(commitmsg 'no trailer here')"
check "valid trailer ok" 0 "$(commitmsg 'ok

Agent: claude')"
check "rich trailer ok" 0 "$(commitmsg 'ok

Agent: openai (gpt-5-codex)')"
reset_repo

# --- core: env template allowed, real env blocked ---
printf 'A=1\n' > .env.example; git add -f .env.example
check ".env.example allowed" 0 "$(precommit)"; reset_repo
printf 'S=x\n' > .env.local; git add -f .env.local
check ".env.local blocked" 1 "$(precommit)"; reset_repo

echo "---- $pass passed, $fail failed ----"
[ "$fail" -eq 0 ]
