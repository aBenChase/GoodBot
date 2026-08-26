# Log schema, receipts & redaction pipeline

Goal: automatically record and timestamp every prompt (input) and response
(output) from both agents, keep a complete private copy for the audit trail,
prove tamper-evidently what was captured, and publish only a human-reviewed,
redacted view to the website.

This spec is shared. Both agents emit the **same** canonical record and the
**same** receipt fields, using whatever native capture mechanism each has.

## 1. Canonical record (JSONL, append-only) — `logs/raw/` (gitignored)

One JSON object per line:

```json
{
  "ts": "2026-08-26T17:04:22.123Z",  // ISO-8601 UTC, when the message occurred
  "agent": "claude",                  // "claude" | "openai"
  "model": "claude-opus-4-8",         // capturing model id
  "session": "<sha256-16>",           // hashed session id (never a raw id/path)
  "turnId": "<stable-turn-id>",
  "seq": 1,                            // monotonic order within the session
  "role": "prompt",                   // "prompt" (human) | "response" (agent)
  "channel": "chat",                  // "chat" | "tool" | "note"
  "text": "...",                       // full content (private; stays in logs/raw)
  "contentSha256": "<64-hex>",        // hash of text; matches the receipt
  "meta": {}                           // optional: tool name, tokens, cost
}
```

`logs/raw/` is **gitignored** — full content never leaves the machine.

## 2. Receipts (tracked) — `logs/receipts/YYYY/MM/DD/…json`

Written **at capture time**, before any redaction, so the audit trail can't be
weakened after the fact. Contains provenance and a hash — **never content**:

```json
{
  "schemaVersion": 1,
  "capturedAt": "2026-08-26T17:04:22.123Z",
  "agent": "openai",
  "model": "gpt-...",
  "turnHash": "<sha256-16 of turnId>",
  "role": "user",                     // "user" | "assistant"
  "contentSha256": "<64-hex>",
  "publicationStatus": "awaiting-review"
}
```

Receipts **are committed**. They prove what was said and when, without exposing
what was said. (Concept contributed by OpenAI; adopted.)

## 3. Pipeline: raw → review → published

1. **Capture** → `logs/raw/` (JSONL, private) **+** `logs/receipts/` (tracked)
   simultaneously.
   - **OpenAI:** Codex hooks (`.codex/hooks.json` → `tools/transcript_hook.py`)
     on `UserPromptSubmit` / `Stop`.
   - **Claude:** a Claude Code hook (`UserPromptSubmit` / `Stop`) or a parser
     over the harness transcript at
     `…/.claude/projects/C--LoCodex-GoodBot/<session>.jsonl`. Same schema, same
     receipts.
2. **Review/redact** → `logs/review/` (gitignored). Automated redaction runs
   here but is only a **warning system**; a human must review before promotion.
3. **Publish** → `logs/published/` (tracked). Reviewed, redacted records the
   website consumes. Promotion is manual and hash-verified
   (`tools/transcript_admin.py publish <id> --reviewer <name>`); it never commits
   or pushes automatically.

## 4. Redaction rules (v0)

Automated pass is a safety net, not the gate. Before promotion, a human confirms:

- **Never publish:** real names, the dependent's condition or medical details,
  personal financial figures tied to the family, addresses, account/record
  identifiers, credentials/tokens, **raw session IDs or local filesystem paths**.
- **Pseudonymize** recurring entities to stable aliases (e.g., the dependent →
  one fixed alias) so the narrative stays coherent.
- **Safe to publish:** the experiment's mechanics, non-identifying amounts (the
  $100 budget, the abstract $30k/yr target), decisions, code, commentary.
- Scan for **credentials** as well as PII. When in doubt, redact and ask.

## 5. Verification

Published records carry each message's `contentSha256`; the publish tool
recomputes and matches them against capture-time receipts. A mismatch blocks
promotion. This ties the public record back to the tamper-evident receipts.
