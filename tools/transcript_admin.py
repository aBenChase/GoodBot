#!/usr/bin/env python3
"""Prepare, inspect, and publish privacy-reviewed Good Bot transcripts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = REPO_ROOT / "logs" / "raw" / "openai"
REVIEW_ROOT = REPO_ROOT / "logs" / "review" / "openai"
PUBLISHED_ROOT = REPO_ROOT / "logs" / "published" / "openai"

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "OpenAI-style API key": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.I),
}


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path.name}:{line_number} is not a JSON object")
            records.append(value)
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def display_path(path: Path) -> Path:
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        return path


def raw_sessions() -> list[Path]:
    return sorted(RAW_ROOT.glob("*.jsonl"))


def resolve(identifier: str, root: Path | None = None) -> Path:
    root = root or RAW_ROOT
    matches = sorted(
        path
        for path in root.glob("*.jsonl")
        if path.stem == identifier or path.stem.startswith(identifier)
    )
    if len(matches) != 1:
        raise ValueError(
            f"Expected one transcript for '{identifier}', found {len(matches)}"
        )
    return matches[0]


def validate(records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError("Transcript is empty")
    expected_keys = {
        "ts",
        "agent",
        "session",
        "seq",
        "role",
        "channel",
        "text",
        "redacted",
        "meta",
    }
    sequences: list[int] = []
    for index, record in enumerate(records, start=1):
        missing = expected_keys - record.keys()
        if missing:
            raise ValueError(f"Record {index} is missing: {', '.join(sorted(missing))}")
        if record["agent"] != "openai":
            raise ValueError(f"Record {index} has unexpected agent")
        if record["role"] not in {"prompt", "response"}:
            raise ValueError(f"Record {index} has invalid role")
        if not isinstance(record["text"], str):
            raise ValueError(f"Record {index} text must be a string")
        sequences.append(int(record["seq"]))
    if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
        raise ValueError("Transcript sequence numbers must be unique and increasing")


def list_sessions() -> int:
    for path in raw_sessions():
        records = read_jsonl(path)
        created = records[0].get("ts", "unknown") if records else "empty"
        print(f"{path.stem}\t{created}\t{len(records)} messages")
    return 0


def show_session(identifier: str) -> int:
    path = resolve(identifier)
    for record in read_jsonl(path):
        print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def prepare_session(identifier: str) -> int:
    source = resolve(identifier)
    records = read_jsonl(source)
    validate(records)
    public_session = f"openai-{source.stem[:12]}"
    prepared: list[dict[str, Any]] = []
    for record in records:
        copy = dict(record)
        copy["session"] = public_session
        copy["redacted"] = False
        meta = dict(copy.get("meta", {}))
        turn_id = str(meta.pop("turn_id", "unknown-turn"))
        meta["turn_hash"] = digest(turn_id)[:16]
        meta.pop("permission_mode", None)
        meta.pop("capture_event", None)
        meta["raw_content_sha256"] = meta.pop(
            "content_sha256", digest(str(copy.get("text", "")))
        )
        copy["meta"] = meta
        prepared.append(copy)

    destination = REVIEW_ROOT / f"{public_session}.jsonl"
    if destination.exists():
        raise ValueError(f"Review copy already exists: {destination.name}")
    write_jsonl(destination, prepared)
    print(display_path(destination))
    return 0


def scan_for_secrets(records: list[dict[str, Any]]) -> None:
    combined = "\n".join(str(record.get("text", "")) for record in records)
    findings = [name for name, pattern in SECRET_PATTERNS.items() if pattern.search(combined)]
    if findings:
        raise ValueError("Potential private content remains: " + ", ".join(findings))


def publish_session(identifier: str, reviewer: str, confirmed: bool) -> int:
    if not confirmed:
        raise ValueError("Pass --confirm-privacy-review after completing human review")
    source = resolve(identifier, REVIEW_ROOT)
    records = read_jsonl(source)
    validate(records)
    scan_for_secrets(records)
    reviewed_at = utc_iso()
    for record in records:
        record["redacted"] = True
        meta = dict(record.get("meta", {}))
        meta["published_content_sha256"] = digest(str(record["text"]))
        meta["publication"] = {
            "status": "reviewed",
            "reviewedAt": reviewed_at,
            "reviewedBy": reviewer,
        }
        record["meta"] = meta

    destination = PUBLISHED_ROOT / source.name
    if destination.exists():
        raise ValueError(f"Published transcript already exists: {destination.name}")
    write_jsonl(destination, records)
    print(display_path(destination))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List private raw sessions")
    show = commands.add_parser("show", help="Print one private raw session")
    show.add_argument("session_id")
    prepare = commands.add_parser("prepare", help="Create an ignored review copy")
    prepare.add_argument("session_id")
    publish = commands.add_parser("publish", help="Publish one reviewed copy")
    publish.add_argument("session_id")
    publish.add_argument("--reviewer", required=True)
    publish.add_argument("--confirm-privacy-review", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "list":
        return list_sessions()
    if args.command == "show":
        return show_session(args.session_id)
    if args.command == "prepare":
        return prepare_session(args.session_id)
    if args.command == "publish":
        return publish_session(
            args.session_id, args.reviewer, args.confirm_privacy_review
        )
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
