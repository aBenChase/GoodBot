# Revenue options menu (v3 — evidence before hype)

_Shared artifact: OpenAI and Anthropic both create, challenge, and review it under
D-006. Prices below are test hypotheses, not established market value or revenue
forecasts._

## Binding product and marketing constraints

- Do not promise an outcome or deadline before we have independently reproducible
  evidence. “Cut your bill in two weeks” is not acceptable positioning.
- Do not sell “AI” as the value. Sell a specific artifact, completed task, or
  decision that a buyer already needs.
- Do not manufacture a case study, imply a synthetic result was real, or turn the
  family's medical circumstances into conversion copy.
- Do not assume the project will create or host an LLM. Excellent commercial and
  open-source model providers already exist; competing with them is outside scope.
- Do not build a product before observing buyer demand. A reusable tool should
  emerge from repeated paid work, not precede it.
- Count net cash, agent/API cost, and human time. Attention is not revenue.

## Reassessment of v2

| Prior play | Verdict | Reason |
|---|---|---|
| P1 — GoodBot Kit | Keep as infrastructure, not a revenue forecast | Coordination code is useful proof, but templates and agent workflows are easy to copy. No buyer or distribution has been validated. |
| P2 — Build log | Keep as the honest public record | It may create trust, but “flywheel,” subscriber, and sponsorship assumptions are unproven. Publish when there is something worth learning, not to feed an algorithm. |
| P3 — Multi-agent code review | Reject as a generic service; narrow it | GitHub already offers Copilot code review and CodeRabbit offers automated review from free/open-source tiers through paid plans. “More models” is not enough differentiation. |
| P4 — LLM cost audit | Reject | The headline is clickbait, the $3–10k price has no evidence, native providers already expose caching/batching/cost controls, and the premise does not fit this project. |
| P5 — Multi-Agent Playbook | Defer | A guide about an experiment with no commercial result is a souvenir, not yet a product. Revisit only after the process produces verified outcomes. |

## Better candidates

### O1 — Paid open-source issue or documentation bounty · mostly agent-executed

- **Buyer/payment event:** a maintainer posts a fixed reward; payment follows an
  accepted contribution.
- **Why it is authentic:** the work and acceptance criterion are public. Revenue
  comes from completing a named task, not attracting an audience.
- **Current evidence:** Algora supports outcome-based GitHub issue payments, but
  current inventory is sparse and many visible rewards are only tens or hundreds
  of dollars. This is a first-dollar test, not the care-fund strategy.
- **First test:** identify ten currently open, authorized tasks; score fit, reward,
  estimated agent cost, maintainer activity, and ambiguity; ask the human to approve
  one claim/submission.
- **Cost/stop:** $0 platform spend; stop a task at four agent-hours or when its
  acceptance criteria cannot be reproduced locally.
- **Metric:** bounty actually paid minus model cost and payment fees.

### O2 — Repository clarity pack · asynchronous service

- **Buyer:** a small dev-tool company or maintained open-source project preparing
  to onboard contributors, hand off ownership, or ship a release.
- **Artifact:** verified setup instructions, architecture map, dependency and
  runbook gaps, one end-to-end tutorial, and a prioritized documentation patch.
- **Why it may sell:** the buyer receives maintainable repository artifacts and
  recovered engineering context. AI is production leverage, not the pitch.
- **Pilot price hypothesis:** $300–750 fixed after one public sample; never five
  unpaid custom reviews.
- **Cost/stop:** no paid tools; cap the sample at eight agent-hours and two human QA
  hours. Stop if ten qualified prospects produce no paid pilot.
- **Metric:** paid pilot, effective net hourly return, and whether the buyer merges
  or uses the artifacts.

### O3 — Bounded architecture decision memo · asynchronous expert product

- **Buyer:** a small software team facing one concrete choice: migration sequence,
  vendor selection, integration boundary, deployment design, or build-vs-buy.
- **Artifact:** assumptions, cited evidence, option matrix, failure modes,
  recommendation, and explicit unknowns. No implementation promise.
- **Why it fits:** it uses the human's architecture judgment and writing while the
  agents gather evidence, challenge assumptions, and draft the memo.
- **Pilot price hypothesis:** $350–900 for a tightly scoped decision; raise it only
  after buyers pay and report useful outcomes.
- **Cost/stop:** no spend; decline decisions requiring regulated legal, medical, or
  financial advice. Stop the offer after three qualified rejections on value.
- **Metric:** net payment, turnaround time, and buyer-reported decision usefulness.

### O4 — Engineering handoff / recovery pack · higher-value, human-reviewed

- **Buyer:** a founder or small agency inheriting a codebase from a departing team.
- **Artifact:** build/deploy verification, system map, operational unknowns,
  critical dependency risks, missing-access checklist, and a 30-day stabilization
  sequence.
- **Why it may sell:** the triggering event already has urgency and a concrete cost;
  the deliverable reduces uncertainty without claiming to replace engineers.
- **Pilot price hypothesis:** $750–1,500 for a small repository with a strict scope.
- **Risks:** private-code handling, credentials, liability, and unavoidable human
  review. This requires a written data-handling procedure before a pilot.
- **Metric:** paid pilot, hours consumed, defects found by the buyer, and follow-on
  work requested without outbound hype.

### O5 — Reproducible technical tutorial or integration guide · writing-led

- **Buyer:** a developer-tools company with a product that works but lacks a tested
  path for a specific framework or use case.
- **Artifact:** working sample repository, cited tutorial, version-pinned setup, and
  automated verification—not generic SEO copy or undisclosed advocacy.
- **Pilot price hypothesis:** $400–1,000 depending on integration depth.
- **Why it fits:** combines architecture, implementation, and clear writing. Public
  bounty history also shows that maintainers pay for concrete tutorials, though
  individual bounty amounts are generally modest.
- **Cost/stop:** no spend; do not publish a positive opinion the evidence does not
  support. Stop after one sample and ten qualified pitches without a paid pilot.
- **Metric:** net payment, sample reproducibility, and actual developer usage when
  the buyer can measure it.

### O6 — Productize only the repeated step · later scaling path

Do not choose a micro-SaaS idea now. After at least three paid O2–O5 engagements,
inspect which step buyers repeatedly pay to avoid. Only then test a narrow tool,
with pre-commitments or paid pilots before a build. GoodBot Kit can supply pieces;
it is not automatically the product.

## Authentic public communication

The public log should sound like an engineering notebook, not a funnel. Useful
titles describe what happened:

- “Our hook test committed to the live repo; here is why.”
- “Two agents proposed five businesses. The human rejected the weakest premise.”
- “What the first paid task cost in model tokens and human minutes.”

No manufactured urgency, inflated savings claim, teaser gap, or medical-story bait.
If plain language earns less attention, that is an acceptable constraint.

## Recommended first validation

Run two $0 lanes for at most 30 days:

1. **Agent-led lane:** inventory current paid OSS tasks and request approval to
   attempt one whose acceptance test is clear. This tests whether the agents can
   earn a first dollar with almost no marketing.
2. **Higher-ceiling lane:** create one public O2 sample for a suitable repository,
   then offer exactly one paid pilot at a stated fixed scope and price. Any outreach
   or account creation requires the human's approval first.

Success is cash actually received or a signed paid pilot—not views, subscribers,
“interest,” or a sponsor conversation. Failure is also useful: record the time and
cost, close the lane, and do not rescue it with louder marketing.

None of these options is presently evidenced as a path to $30,000 per year. The
point of the first validation is to discover a credible transaction, then measure
whether it repeats.

## Current-source checks (2026-08-26)

- [Algora pricing](https://algora.io/pricing/) — outcome-based GitHub issue
  payments; contributors receive posted rewards when work is accepted.
- [Algora community examples](https://algora.io/algora/bounties/community) and
  [LabLab.ai examples](https://algora.io/lablab-ai/home) — visible rewards and
  current inventory illustrate the modest, variable bounty ceiling.
- [GitHub Copilot code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review)
  and [CodeRabbit plans](https://docs.coderabbit.ai/management/plans) — generic AI
  review is already a well-supplied category.
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/latest-model)
  — provider-native cost controls make generic optimization advice easier to obtain.
- [GitHub Sponsors fees](https://docs.github.com/en/sponsors/sponsoring-open-source-contributors/about-sponsorships-fees-and-taxes)
  — a payment rail for valued open-source work, not evidence that sponsors will
  appear.
