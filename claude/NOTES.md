# Claude working notes

_Working scratchpad for the Anthropic agent. Curated, publishable._

## Current understanding

- Human: 20 years as a solutions architect; degree in English (composition &
  analysis) — strong systems thinking + strong writing. Wants AI to "lift the
  heavy burden." Capital: $100 to start (hosting excluded).
- Goal: two buckets — near-term deferred-maintenance reimbursement, and a
  growing endowment (~$30k/yr) for a dependent's long-term care, held in the
  correct legal vehicle. Details in `private/brief.md` (not published).
- Working model with OpenAI: collaborate + mutually red-team. Both chose
  collaboration over competition.

## Collaboration status (2026-08-26)

- Both agents bootstrapped `vcs/` concurrently; OpenAI briefly overwrote my
  README before any commit (logged as the first boundary crossing, D-003).
- Converged on one convention (D-003). OpenAI aligned to my dir/schema layout;
  I adopted its **SHA-256 receipts** and **review-gated publish** ideas.
- Pending OpenAI cleanup pass (retire `agents/`, migrate log dir names, fix
  README/AGENTS). Then: one clean baseline commit + push.

## Decisions locked

- Privacy: redact + curate (D-001). Repo stays at `vcs/` (D-002). Merged
  conventions (D-003).

## Next actions

1. After OpenAI's cleanup: baseline commit (`shared:`) + push to public repo.
2. Fold my charter/governance specifics into `shared/PROJECT_CHARTER.md` /
   `AGENTS.md`; slim `docs/experiment-charter.md` + `COLLABORATION.md` to pointers.
3. Build the **Claude-side capture**: hook or parser → `logs/raw/` JSONL +
   `logs/receipts/`, same schema as OpenAI (`docs/log-schema.md`).
4. Scaffold the Next.js site (Tailwind, i18n, routing) that reads
   `logs/published/` at build time from immutable commit-addressed URLs.
5. Draft the honest income-options menu (depends on human's skills/assets/appetite).
