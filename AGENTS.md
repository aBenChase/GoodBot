# Instructions for agents working in Good Bot

This repository is public. Treat every tracked file as immediately publishable.

## Ownership and collaboration

- OpenAI may edit `openai/` without coordination.
- Anthropic may edit `claude/` without coordination.
- `shared/`, `logs/published/`, `logs/receipts/`, and site-facing schemas are shared
  surfaces. Inspect current changes before editing them and leave a handoff note for
  material changes.
- Never modify another agent's owned directory unless the user explicitly requests it.
- Preserve unrelated working-tree changes. Do not reset, clean, or rewrite history.

## Safety and publication

- Do not commit credentials, tokens, addresses, medical record identifiers, full
  names of family members, dates of birth, or unreviewed medical details.
- Raw transcripts belong only in the ignored `logs/raw/` directory. Privacy-review
  drafts belong only in ignored `logs/review/`.
- Publish a transcript only after human privacy review.
- Do not move money, enter contracts, create accounts, contact third parties, or
  incur material expense without the user's explicit approval.
- Label projections, estimates, and simulated results. Never present them as revenue.

## Provenance

- Use UTC ISO-8601 timestamps in machine-readable records.
- Add an `agent` field to work products when the schema supports it.
- Prefer additive notes and small, attributable commits.
- Follow `COLLABORATION.md`, including the `Agent: openai` or `Agent: claude`
  commit trailer.

## Verification

- Run the narrowest relevant checks after an edit.
- Record consequential decisions in `shared/DECISIONS.md`.
- Record every cross-agent review in `shared/REVIEWS.md` and reference its finding
  IDs from `shared/HANDOFF.md` before ending the turn. Chat-only feedback is not a
  completed handoff.
- If two agents disagree, preserve both positions and the evidence needed for the user
  to decide.
