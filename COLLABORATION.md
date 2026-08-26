# Collaboration protocol — Claude ⇄ OpenAI

Two AI agents share this repository. We work **together**, and we deliberately
**red-team each other's financial and technical assumptions** before anything is
acted on. This document keeps us from colliding and makes any boundary crossing
visible.

## Participants

- **Claude** (Anthropic) — works in `claude/`.
- **OpenAI** — works in `openai/`.
- **Joint** work lives in `shared/`.

## Directory ownership

- An agent edits **only its own directory** and `shared/`.
- To touch another agent's directory, first leave a note in
  `shared/HANDOFF.md` explaining what and why. This is the "surprise editing"
  guardrail the human asked for: crossings are allowed, but never silent.

## Commit attribution (so crossings are auditable)

Both agents push as the same GitHub user, so commit *author* can't distinguish
us. Instead, every commit carries a trailer naming the agent:

```
<summary line>

<body>

Agent: claude            # or: Agent: openai
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

`git log` + `git diff` then show who changed what. If stronger enforcement is
wanted later: a GitHub `CODEOWNERS` file plus branch protection, or a pre-commit
hook that rejects cross-directory edits lacking a `shared/HANDOFF.md` entry.

## Red-team step

Substantive plans (anything involving money, legal structure, or spend) get a
`RED-TEAM:` note from the *other* agent in `shared/DECISIONS.md` before they're
executed. Disagreements are logged, not overwritten.

## Coordination files (created as needed)

- `shared/DECISIONS.md` — dated decisions + red-team notes.
- `shared/HANDOFF.md` — cross-boundary edits and open asks between agents.
- `shared/REVIEWS.md` — finding IDs, evidence, ownership, acknowledgement, and
  resolution status for cross-agent reviews.

## Cadence

Commit small and often, so `git diff` stays a clean timeline of who did what.
Never leave a cross-agent review only in chat; commit it through the review register
and handoff before ending the turn.
