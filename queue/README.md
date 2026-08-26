# Turn queue

Task files drive the serial orchestrator (`../tools/orchestrator.ps1`).

- `pending/` — queued tasks, processed oldest-first. **Task `*.json` are
  gitignored** (they hold prompts = raw input); only this README and `.gitkeep`
  are tracked.
- `done/` — completed tasks are moved here.

Task shape:

```json
{
  "agent": "claude",
  "title": "short imperative summary",
  "prompt": "the full instruction for the agent",
  "worktree": "../gb-claude"
}
```
