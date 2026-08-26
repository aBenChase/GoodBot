#!/usr/bin/env python3
"""Capture the Claude Code transcript into the shared Good Bot audit trail.

Claude's native (post-hoc) capture: reads the harness transcript JSONL under
~/.claude/projects/C--LoCodex-GoodBot/, extracts the human<->assistant chat
turns, and writes both halves of the pipeline in `docs/log-schema.md`:

  - logs/raw/claude-<sessionhash>.jsonl   full content, GITIGNORED (private)
  - logs/receipts/YYYY/MM/DD/*.json       hash-only, TRACKED (tamper-evidence)

Receipts use the same shape as OpenAI's tools/transcript_hook.py so one website
can verify both. Nothing here is published; promotion to logs/published/ is a
separate, human-reviewed step.

Usage:
  py -3 tools/claude_capture.py                      # all sessions for this project
  py -3 tools/claude_capture.py --transcript <path>  # one transcript file
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = REPO_ROOT / "logs" / "raw"
RECEIPTS_ROOT = REPO_ROOT / "logs" / "receipts"
DEFAULT_PROJECT = Path.home() / ".claude" / "projects" / "C--LoCodex-GoodBot"
AGENT = "claude"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def extract_text(content) -> str:
    """Joined text of a message's content, or '' for tool-only turns."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts).strip()
    return ""


def receipt_exists(turn_hash: str, role: str) -> bool:
    return any(RECEIPTS_ROOT.glob(f"**/*-{turn_hash}-{role}.json"))


def write_receipt(now: datetime, turn_id: str, role: str, content: str, model: str) -> None:
    turn_hash = digest(turn_id)[:16]
    if receipt_exists(turn_hash, role):
        return
    ts = now.strftime("%Y%m%dT%H%M%S.%fZ")
    receipt = {
        "schemaVersion": 1,
        "capturedAt": iso(now),
        "agent": AGENT,
        "model": model or "unknown",
        "turnHash": turn_hash,
        "role": role,
        "contentSha256": digest(content),
        "publicationStatus": "awaiting-review",
    }
    path = (
        RECEIPTS_ROOT
        / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
        / f"{ts}-{turn_hash}-{role}.json"
    )
    write_atomic(path, json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")


def process(transcript: Path) -> int:
    now = utc_now()
    records = []
    session = None
    seq = 0
    with transcript.open("r", encoding="utf-8") as fh:
        for raw_line in fh:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                obj = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") not in ("user", "assistant"):
                continue
            msg = obj.get("message") or {}
            role_src = msg.get("role") or obj.get("type")
            if role_src not in ("user", "assistant"):
                continue
            text = extract_text(msg.get("content"))
            if not text:
                continue  # tool_result / tool_use-only turn -> not chat
            session = session or obj.get("sessionId", "unknown")
            turn_id = obj.get("uuid") or f"{transcript.stem}-{seq}"
            model = msg.get("model", "") or ("claude" if role_src == "assistant" else "")
            role = "prompt" if role_src == "user" else "response"
            seq += 1
            records.append({
                "ts": obj.get("timestamp") or iso(now),
                "agent": AGENT,
                "model": model,
                "session": digest(str(session))[:16],
                "turnId": turn_id,
                "seq": seq,
                "role": role,
                "channel": "chat",
                "text": text,
                "contentSha256": digest(text),
            })
            write_receipt(now, turn_id, "user" if role == "prompt" else "assistant", text, model)

    if not records:
        return 0
    shash = digest(str(session))[:16]
    raw_path = RAW_ROOT / f"claude-{shash}.jsonl"
    write_atomic(raw_path, "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n")
    print(f"{transcript.name}: {len(records)} chat turns -> {raw_path.relative_to(REPO_ROOT)}")
    return len(records)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--transcript", help="a single transcript .jsonl to capture")
    ap.add_argument("--project-dir", default=str(DEFAULT_PROJECT))
    args = ap.parse_args()

    if args.transcript:
        targets = [Path(args.transcript)]
    else:
        pdir = Path(args.project_dir)
        targets = sorted(pdir.glob("*.jsonl")) if pdir.exists() else []
    if not targets:
        print("no transcripts found.", file=sys.stderr)
        return 1
    total = sum(process(t) for t in targets)
    print(f"captured {total} chat turns across {len(targets)} transcript(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
