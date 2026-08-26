from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import transcript_admin, transcript_hook


class TranscriptHookTests(unittest.TestCase):
    def test_append_is_idempotent_and_receipt_omits_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transcript_hook.RAW_ROOT = root / "raw"
            transcript_hook.RECEIPTS_ROOT = root / "receipts"
            session_hash = transcript_hook.digest("session")[:16]
            path = transcript_hook.RAW_ROOT / f"{session_hash}.jsonl"
            record = {
                "ts": "2026-08-26T12:00:00.000Z",
                "agent": "openai",
                "session": "session",
                "seq": 0,
                "role": "prompt",
                "channel": "chat",
                "text": "private prompt",
                "redacted": False,
                "meta": {
                    "model": "test-model",
                    "turn_id": "turn-1",
                    "content_sha256": transcript_hook.digest("private prompt"),
                },
            }

            stored = transcript_hook.append_record(path, dict(record))
            transcript_hook.append_record(path, dict(record))
            transcript_hook.write_receipt(stored, session_hash)

            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 1)
            receipt_path = next(transcript_hook.RECEIPTS_ROOT.glob("**/*.json"))
            receipt_text = receipt_path.read_text(encoding="utf-8")
            self.assertNotIn("private prompt", receipt_text)


class TranscriptAdminTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        transcript_admin.RAW_ROOT = root / "raw"
        transcript_admin.REVIEW_ROOT = root / "review"
        transcript_admin.PUBLISHED_ROOT = root / "published"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_prepare_sanitizes_ids_and_publish_requires_confirmation(self) -> None:
        raw = transcript_admin.RAW_ROOT / "abc123.jsonl"
        records = [
            {
                "ts": "2026-08-26T12:00:00.000Z",
                "agent": "openai",
                "session": "real-session-id",
                "seq": 1,
                "role": "prompt",
                "channel": "chat",
                "text": "Reviewed public prompt",
                "redacted": False,
                "meta": {"turn_id": "turn-1", "content_sha256": "hash"},
            },
            {
                "ts": "2026-08-26T12:00:01.000Z",
                "agent": "openai",
                "session": "real-session-id",
                "seq": 2,
                "role": "response",
                "channel": "chat",
                "text": "Reviewed public response",
                "redacted": False,
                "meta": {"turn_id": "turn-1", "content_sha256": "hash"},
            },
        ]
        transcript_admin.write_jsonl(raw, records)
        transcript_admin.prepare_session("abc")
        review = transcript_admin.REVIEW_ROOT / "openai-abc123.jsonl"
        prepared = transcript_admin.read_jsonl(review)
        self.assertEqual(prepared[0]["session"], "openai-abc123")
        self.assertNotIn("turn_id", prepared[0]["meta"])

        with self.assertRaisesRegex(ValueError, "confirm-privacy-review"):
            transcript_admin.publish_session("openai-abc", "reviewer", False)

        transcript_admin.publish_session("openai-abc", "reviewer", True)
        published = transcript_admin.read_jsonl(
            transcript_admin.PUBLISHED_ROOT / "openai-abc123.jsonl"
        )
        self.assertTrue(all(record["redacted"] for record in published))

    def test_secret_scan_blocks_credentials(self) -> None:
        with self.assertRaisesRegex(ValueError, "API key"):
            transcript_admin.scan_for_secrets(
                [{"text": "sk-1234567890abcdefghijklmnop"}]
            )


if __name__ == "__main__":
    unittest.main()
