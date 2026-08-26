# Experiment charter

_Last updated: 2026-08-26_

## North star

Fund two buckets for a family:

- **Bucket A — near-term.** Reimburse ~a decade of deferred household
  maintenance. Ordinary money, no special legal structure, needed relatively
  soon.
- **Bucket B — endowment.** A corpus that distributes ~**$30k/year and grows**
  (~**$0.75M–$1M** at a 3–4% safe withdrawal rate), held inside the correct
  legal vehicle for a dependent with possible benefits eligibility (special-needs
  trust and/or ABLE account), set up with licensed professionals.

Keeping the buckets separate matters: only Bucket B has legal strings attached.
A fund simply in the dependent's name can jeopardize means-tested benefits.

## Definition of success

**Net profit, sustained** — revenue minus *every* cost (API tokens, ads,
hosting, fees, tooling). Vanity metrics (traffic, "gross revenue," activity)
do not count.

## Budget & kill criteria

- Hard cap: **$100** of at-risk capital for the income experiment (DigitalOcean
  hosting is already secured for another project and excluded).
- **Kill criterion:** if there is no credible path to positive net profit by an
  agreed checkpoint (date and/or spend), the experiment stops. We name the
  checkpoint before spending.

## Division of labor

- **Human (solutions architect, strong writer):** direction, judgment,
  real-world execution, anything requiring a person or an account. AI is meant to
  "lift the heavy burden."
- **AI agents:** research, drafting, modeling, building, and honest option
  analysis — each checking the other.

## Guardrails

- No autonomous financial trades, transfers, purchases, or credential entry.
- Nothing published without passing the redaction pipeline (`log-schema.md`).
- Not financial/legal/tax advice; structural steps go through licensed
  professionals.

## Open questions (to resolve with the human)

- Bucket A target and deadline (the deferred-maintenance figure).
- Which income avenues fit the human's skills/assets (separate options doc).
- Public-log privacy: **redact + curate** (decided 2026-08-26; see `../shared/DECISIONS.md` D-001).
- Repo layout: repo stays rooted at `vcs/`; website is a separate deploy (D-002).
