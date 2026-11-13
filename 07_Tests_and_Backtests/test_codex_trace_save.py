import tempfile
from pathlib import Path
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "05_Server_Integration"))
from codex_trace_save import save_trace

TRACE = """🏷️ [TRACE: unknown | 追加検証 | 保存テスト]
<!-- RESEARCH_TRACE_START
ai_id: codex
session_title: 保存テスト
case_id: unknown
parent_case_id: root
decision: 追加検証
target_market: none
attachment_file: none
part_info: 1/1
timestamp: 2026-10-05 12:00:00 JST
-->
日本語と価格：€1.25。テスト専用、実案件ではない。
<!-- RESEARCH_TRACE_END -->
"""


class SaveTests(unittest.TestCase):
    def test_roundtrip_and_duplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            result = save_trace(TRACE, temp)
            self.assertEqual(Path(result["path"]).read_bytes(), TRACE.encode("utf-8"))
            self.assertEqual(save_trace(TRACE, temp)["status"], "already_saved")
            self.assertEqual(len(list(Path(temp).glob("*.md"))), 1)

    def test_changed_body_preserves_both(self):
        with tempfile.TemporaryDirectory() as temp:
            a = save_trace(TRACE, temp)
            b = save_trace(TRACE.replace("€1.25", "€1.26"), temp)
            self.assertNotEqual(a["path"], b["path"])
            self.assertEqual(Path(a["path"]).read_bytes(), TRACE.encode("utf-8"))

    def test_invalid_never_creates_destination(self):
        invalid = ["普通の会話", TRACE.replace("ai_id: codex", "ai_id: scout"),
                   TRACE.replace("<!-- RESEARCH_TRACE_END -->", ""), TRACE + "extra",
                   TRACE.replace("case_id: unknown", "case_id: ../escape"),
                   TRACE.replace("part_info: 1/1", "part_info: 2/1"),
                   TRACE.replace("2026-10-05", "2026-99-05"), TRACE + TRACE]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "not_created"
            for value in invalid:
                with self.subTest(value=value):
                    with self.assertRaises(ValueError):
                        save_trace(value, root)
                    self.assertFalse(root.exists())

    def test_newlines_normalize(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(save_trace(TRACE, temp)["path"], save_trace(TRACE.replace("\n", "\r\n"), temp)["path"])

    def test_failure_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "file"
            root.write_text("do not overwrite", encoding="utf-8")
            with self.assertRaises(OSError):
                save_trace(TRACE, root)
            self.assertEqual(root.read_text(encoding="utf-8"), "do not overwrite")


if __name__ == "__main__":
    unittest.main()
