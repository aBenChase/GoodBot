# Transcript protocol

## Record shape

The canonical append-only JSONL shape is defined in `docs/log-schema.md`. Codex
uses `agent: "openai"`, `role: "prompt" | "response"`, and puts the model and
turn identifier in `meta`.

## Codex setup

The repository contains `.codex/hooks.json`. Codex requires project hooks to be
reviewed and trusted before they run. Start Codex with `vcs` as its project root,
then review the hooks in the Codex hook interface. The hooks invoke
`tools/transcript_hook.py` for `UserPromptSubmit` and `Stop` events.

The current Codex conversation began one directory above this Git repository, so the
project-local hook cannot retroactively capture earlier turns. Earlier exchanges can
be imported as reviewed historical records later.

## Files produced automatically

- `logs/raw/openai/<session-hash>.jsonl` contains canonical raw records and is
  ignored.
- `logs/receipts/YYYY/MM/DD/<timestamp>-<turn-hash>-<role>.json` contains only a
  timestamp, content hash, agent/model provenance, and publication status.

## Publication workflow

1. Run `py -3 tools/transcript_admin.py list`.
2. Prepare an ignored review copy with
   `py -3 tools/transcript_admin.py prepare <session-id>`.
3. Review and redact `logs/review/openai/<session-id>.jsonl`.
4. Publish with `py -3 tools/transcript_admin.py publish <session-id> --reviewer <name> --confirm-privacy-review`.
5. Inspect the resulting Git diff before committing and pushing.

Promotion validates the JSONL, marks it reviewed, and writes it to
`logs/published/openai/`. It never commits or pushes automatically.

## Anthropic

Anthropic should emit the same public JSON schema and receipt fields. Its native
capture mechanism can differ, but raw unreviewed content must remain ignored and
publication must use the same privacy gate.
