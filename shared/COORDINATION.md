# Coordination: two agents, one repo, no collisions

Complements `../COLLABORATION.md` (ownership + red-team) and `../AGENTS.md`
(operating rules). This covers the *mechanics*.

## 1. Turn lease — works with a manual queue

One writer at a time. The holder records a lease in `shared/TURN.lock`
(gitignored, transient):

    {"holder":"claude","title":"...","since":"<utc>","expires":"<utc>"}

- Take the lease before writing; release after committing.
- `expires` is a TTL (default 30 min) so a crashed turn can't deadlock.
- Prefer event-driven handoff (release on commit) over fixed clocks — a clock
  slice collides if a turn runs long and idles the repo if it runs short.

## 2. Durable review visibility — required

The repository is the communication channel between agents. Chat commentary,
final responses, and UI-only code comments may be invisible to the other agent.

At the start of every turn:

1. Inspect `git status` and recent commits.
2. Read the newest entry in `shared/HANDOFF.md`.
3. Read open items assigned to you in `shared/REVIEWS.md`.

Before releasing a turn:

1. Put every cross-agent finding in `shared/REVIEWS.md` with a stable ID, evidence,
   status, and owner.
2. Add a short `shared/HANDOFF.md` entry referencing those IDs.
3. Commit and push the durable record. A chat-only review is incomplete.
4. The receiving agent acknowledges each assigned ID on its next turn and records
   the resolving commit when it closes the finding.

Do not copy raw prompts, private facts, credentials, or unreviewed transcript text
into either coordination file.

## 3. Per-agent worktrees — the real isolation

`pwsh tools/worktrees.ps1 create` gives each agent its own working directory
backed by the one repo:

- `../gb-claude` on `claude/work` (goodbot.agent=claude)
- `../gb-openai` on `openai/work` (goodbot.agent=openai)

The two agents then cannot edit the same file at once. Conflicts surface only at
merge into `main`, where git resolves them and the diff answers "did an edit
cross a boundary?" explicitly. Each worktree self-configures hooks + identity.

## 4. Enforcement hooks

`pwsh tools/setup-hooks.ps1` points `core.hooksPath` at `tools/git-hooks/`:

- **pre-commit** — refuses to stage `private/`, `logs/raw|review|staging/`,
  secrets, queued task `*.json`, or `TURN.lock` (a backstop even against
  `git add -f`).
- **commit-msg** — requires an `Agent: claude|openai|shared` trailer, and blocks
  an agent from editing the other's directory unless the commit carries a
  `Cross-Boundary-Ack:` trailer (paired with a `shared/HANDOFF.md` note).

Identity: in a shared dir the agent is read from the commit's `Agent:` trailer;
in a worktree the authoritative `goodbot.agent` config wins. Do **not** set
`goodbot.agent` in a shared dir — both agents would share it.

## 5. Serial orchestrator — retire the manual queue, later

`tools/orchestrator.ps1` (DRY-RUN by default; `-Execute` to run) processes
`queue/pending/*.json` oldest-first: acquire lease -> launch the task's agent
(command from `tools/orchestrator.config.json`) -> auto-commit with the right
`Agent:` trailer -> release -> move the task to `queue/done/`.

## Interim vs. target

- **Now:** hooks active in the shared `vcs/` dir; the human queues turns manually.
- **Target:** a worktree per agent; the orchestrator drives the queue.
