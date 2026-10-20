"""人工コマンドによるログ記録の確認。市場検証ではない。"""
import importlib.util
import json
from pathlib import Path
import sys

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts/run_logged.py"


@pytest.fixture
def logger(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("run_logged", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    return module


@pytest.mark.parametrize("exit_code", [0, 3])
def test_records_actual_result_and_jst(logger, tmp_path, monkeypatch, exit_code):
    sample = tmp_path / "synthetic.txt"
    sample.write_text("abc", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), "--input", "synthetic.txt", "--",
                                     sys.executable, "-c", f"print('synthetic'); raise SystemExit({exit_code})"])
    assert logger.main() == exit_code
    record = json.loads(next((tmp_path / "reports").glob("*.json")).read_text())
    assert record["exit_code"] == exit_code
    assert record["status"] == ("passed" if exit_code == 0 else "failed")
    assert record["started_at_jst"].endswith("+09:00")
    assert record["finished_at_jst"].endswith("+09:00")
    assert record["case_id"] == "unknown"
    assert record["stdout"] == "synthetic\n"
    assert record["inputs"][0]["sha256"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_missing_command_is_logged_as_failure(logger, tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), "--", str(tmp_path / "does-not-exist")])
    assert logger.main() == 127
    record = json.loads(next((tmp_path / "reports").glob("*.json")).read_text())
    assert record["status"] == "failed"
    assert record["exit_code"] == 127
    assert record["stderr"]
