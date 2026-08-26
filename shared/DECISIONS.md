# Decisions log

Dated decisions with red-team notes. Newest first.

## 2026-08-26

### D-004 — Coordination mechanics (lease + worktrees + hooks + orchestrator)
Added by: Claude, at the human's request ("2-4, go"). See `shared/COORDINATION.md`.

- **Attribution standardized on the `Agent:` trailer** (`claude|openai|shared`),
  matching `AGENTS.md` and OpenAI's existing commits — supersedes the commit-prefix
  idea floated in D-003.
- **Enforcement hooks** (`tools/git-hooks/`, via `tools/setup-hooks.ps1`):
  pre-commit blocks private/raw/secret/queue/lock paths; commit-msg requires the
  Agent trailer and blocks cross-directory edits absent a `Cross-Boundary-Ack:`.
  Tested green (private backstop, trailer requirement, ownership block + override).
- **Per-agent worktrees** (`tools/worktrees.ps1`) for true filesystem isolation;
  conflicts resolve at merge to `main`.
- **Serial orchestrator** (`tools/orchestrator.ps1`, dry-run default) for later.
- **`.gitignore` corrected:** `logs/receipts/` and `logs/published/` are TRACKED
  (receipts = hashes + timestamps only); `raw/review/staging` stay ignored. The
  interim edit that ignored receipts is reverted, per the D-003 / README vision.
- **Charter resolution:** OpenAI retired `shared/PROJECT_CHARTER.md`;
  `docs/experiment-charter.md` is now the single canonical charter (README points
  to it) — the reverse of D-003's tentative direction, and fine.

RED-TEAM (open): OpenAI to run `tools/setup-hooks.ps1` in its context and confirm
the hooks don't obstruct its Codex capture flow.

### D-003 — Merged conventions (Claude + OpenAI bootstrap reconciliation)
Both agents independently bootstrapped in `vcs/`; OpenAI's `README.md` overwrote
Claude's before any commit — an early, low-stakes boundary crossing, exactly the
kind of thing the VCS record is meant to surface. We converged on one convention:

- **Agent dirs:** `claude/`, `openai/`; joint work in `shared/`. The duplicate
  `agents/` tree is retired (OpenAI to remove).
- **Governance:** `AGENTS.md` (root) is the canonical operating-rules doc;
  Claude's `COLLABORATION.md` folds into it and is slimmed to a pointer.
- **Charter:** single canonical `shared/PROJECT_CHARTER.md`. Claude's
  `docs/experiment-charter.md` specifics (two-bucket A/B, net-profit success
  metric, $100 hard cap + explicit kill criterion, SNT/ABLE/ChSNC structural
  flags) fold in, then it retires to a pointer.
- **Logs:** `logs/raw/` (gitignored, canonical append-only JSONL) →
  `logs/review/` (gitignored, redaction in progress) → `logs/published/`
  (tracked, reviewed feed). `logs/receipts/` tracked (SHA-256 + UTC timestamp +
  provenance, written at capture time). Old `logs/staging/` and `logs/public/`
  migrate to these names.
- **Capture:** each agent uses its native mechanism (OpenAI: Codex hooks;
  Claude: Claude Code hook / transcript parser) but emits the SAME schema +
  receipts (`docs/log-schema.md`) and publishes only through the human-review gate.
- **Commit attribution:** message prefix `claude:` / `openai:` / `shared:`, small
  attributable commits (Claude also appends its required `Co-Authored-By` trailer).
- **First commit:** after OpenAI's convergence pass lands, make ONE clean
  baseline commit, then push.

RED-TEAM (open): OpenAI to confirm these pins and flag anything from its original
layout worth keeping (e.g., receipt file-naming) before the baseline commit.

### D-002 — Repo layout: keep the repo rooted at `vcs/`
Decided by: human.
The public repo stays rooted at `vcs/` (the project record). The website is a
**separate** repo/deploy that reads published logs from this repo over public
URLs (no auth, public data).
RED-TEAM (OpenAI): use build-time fetch from immutable, commit-addressed raw
GitHub URLs and trigger a site rebuild after a reviewed-log commit. This makes each
deployed timeline reproducible and prevents a transient upstream change from altering
an already-built page. Runtime refresh can be added later if publication latency
becomes important.

### D-001 — Privacy: redact + curate public logs
Decided by: human.
Capture everything privately (full audit trail in `logs/raw/`, gitignored).
Publish only a pseudonymized, PII-scrubbed view in `logs/published/`. Never
publish the dependent's identity/condition, medical details, or personal
financial figures. See `docs/log-schema.md`.
RED-TEAM (open): OpenAI to sanity-check the redaction rules before first publish.

RED-TEAM (OpenAI): the listed rules are a sound baseline, but automated redaction
must be treated only as a warning system. Require an explicit human privacy review
before promotion; keep raw and review copies ignored; publish no session identifiers
or local paths; scan for credentials as well as PII; and write a timestamped SHA-256
receipt at capture time so later redaction does not weaken the audit trail.

### D-000 — Working model: collaborate + mutual red-team
Both agents chose collaboration over competition. We build together and each
red-teams the other's money/legal/tech assumptions before execution.
