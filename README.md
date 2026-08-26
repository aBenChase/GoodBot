# Good Bot

Good Bot is a public experiment in whether cooperating AI agents can build durable,
ethical revenue toward a family medical-care fund.

The project begins with a concrete long-term objective: help support approximately
$30,000 per year of future medical costs, with room for those costs to rise. This
repository records the work, decisions, evidence, and reviewed conversation logs
behind the experiment.

## Project principles

- People and medical privacy come before publicity or speed.
- Agents may research, propose, build, and test, but they may not move money,
  accept legal obligations, publish secrets, or contact people without approval.
- Revenue and costs are reported honestly. Forecasts are labeled as forecasts.
- OpenAI and Anthropic work independently when useful, then share evidence and
  challenge one another's conclusions.
- Repository history is part of the audit trail. Do not rewrite it to hide mistakes.

## Repository map

- `openai/` — OpenAI-owned notes and work products.
- `claude/` — Anthropic-owned notes and work products.
- `shared/` — project-wide decisions, handoffs, and specifications.
- `logs/raw/` — local raw conversation capture; intentionally ignored by Git.
- `logs/review/` — local privacy-review copies; intentionally ignored by Git.
- `logs/receipts/` — public timestamps and SHA-256 hashes proving what was captured.
- `logs/published/` — privacy-reviewed JSONL consumed by the public website.
- `tools/` — transcript capture and publication utilities.

## Conversation logging

Codex hooks record each submitted prompt and final response. Raw content first lands
in `logs/raw/`, while a content hash and UTC timestamp land in `logs/receipts/`.
Raw and review directories are never committed. After review, an operator promotes a
conversation to `logs/published/`, where it can be included in the website.

This is intentionally a two-stage system. A public repository cannot undo disclosure
of a name, medical detail, credential, or other sensitive information once committed.

See `shared/TRANSCRIPT_PROTOCOL.md` for setup and operating details.

## Status

The project foundation is being established. No revenue claims have been made. See
`docs/experiment-charter.md` for the initial goals, constraints, and open questions.
