#!/usr/bin/env python3
"""Capture Codex prompt/response hook events as private canonical JSONL."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, TextIO


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = REPO_ROOT / "logs" / "raw" / "openai"
RECEIPTS_ROOT = REPO_ROOT / "logs" / "receipts"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@contextmanager
def locked(stream: TextIO) -> Iterator[None]:
    """Hold an exclusive lock while reading and appending one session file."""

    if os.name == "nt":
        import msvcrt

        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl

        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def read_stream(stream: TextIO) -> list[dict[str, Any]]:
    stream.seek(0)
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(stream, start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"JSONL line {line_number} is not an object")
        records.append(value)
    return records


def append_record(path: Path, record: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8", newline="\n") as stream:
        with locked(stream):
            existing = read_stream(stream)
            duplicate = next(
                (
                    item
                    for item in existing
                    if item.get("role") == record["role"]
                    and item.get("meta", {}).get("turn_id")
                    == record["meta"]["turn_id"]
                ),
                None,
            )
            if duplicate:
                return duplicate
            record["seq"] = max(
                (int(item.get("seq", 0)) for item in existing), default=0
            ) + 1
            stream.seek(0, os.SEEK_END)
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    return record


def receipt_path(turn_hash: str, role: str) -> Path | None:
    matches = sorted(RECEIPTS_ROOT.glob(f"**/*-{turn_hash}-{role}.json"))
    return matches[0] if matches else None


def write_receipt(record: dict[str, Any], session_hash: str) -> None:
    turn_id = str(record["meta"]["turn_id"])
    turn_hash = digest(turn_id)[:16]
    role = str(record["role"])
    if receipt_path(turn_hash, role):
        return

    captured_at = datetime.fromisoformat(str(record["ts"]).replace("Z", "+00:00"))
    timestamp = captured_at.strftime("%Y%m%dT%H%M%S.%fZ")
    receipt = {
        "schemaVersion": 1,
        "capturedAt": record["ts"],
        "agent": "openai",
        "model": record["meta"].get("model", "unknown"),
        "sessionHash": session_hash,
        "turnHash": turn_hash,
        "role": role,
        "contentSha256": record["meta"]["content_sha256"],
        "publicationStatus": "awaiting-review",
    }
    destination = (
        RECEIPTS_ROOT
        / captured_at.strftime("%Y")
        / captured_at.strftime("%m")
        / captured_at.strftime("%d")
        / f"{timestamp}-{turn_hash}-{role}.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    event = json.load(sys.stdin)
    event_name = str(event.get("hook_event_name", ""))
    session_id = str(event.get("session_id", "unknown-session"))
    turn_id = str(event.get("turn_id", "unknown-turn"))
    model = str(event.get("model", "unknown"))
    permission_mode = str(event.get("permission_mode", "unknown"))

    if event_name == "UserPromptSubmit":
        role = "prompt"
        content = str(event.get("prompt", ""))
    elif event_name == "Stop":
        role = "response"
        content = str(event.get("last_assistant_message") or "")
        if not content:
            print("{}")
            return 0
    else:
        return 0

    now = utc_now()
    session_hash = digest(session_id)[:16]
    record = {
        "ts": iso_utc(now),
        "agent": "openai",
        "session": session_id,
        "seq": 0,
        "role": role,
        "channel": "chat",
        "text": content,
        "redacted": False,
        "meta": {
            "model": model,
            "turn_id": turn_id,
            "permission_mode": permission_mode,
            "content_sha256": digest(content),
            "capture_event": event_name,
        },
    }
    stored = append_record(RAW_ROOT / f"{session_hash}.jsonl", record)
    write_receipt(stored, session_hash)

    if event_name == "Stop":
        print("{}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # Report failure without echoing transcript content.
        print(f"Good Bot transcript capture failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
