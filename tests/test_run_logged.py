"""人工コマンドと一時Gitリポジトリでログの再現性・失敗経路を確認する。"""
import importlib.util
import json
from pathlib import Path
import shutil
import signal
import subprocess
import sys

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts/run_logged.py"


def git(root, *args):
    return subprocess.run(["git", "-c", "user.name=Validation", "-c", "user.email=validation@example.invalid",
                           *args], cwd=root, check=True, capture_output=True, text=True)


@pytest.fixture
def logger(tmp_path, monkeypatch):
    (tmp_path / "scripts").mkdir()
    shutil.copyfile(SCRIPT, tmp_path / "scripts/run_logged.py")
    (tmp_path / ".gitignore").write_text("reports/\n.target-venv/\n", encoding="utf-8")
    (tmp_path / "synthetic.txt").write_text("abc", encoding="utf-8")
    git(tmp_path, "init")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "Artificial test fixture")
    spec = importlib.util.spec_from_file_location("run_logged", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    return module


def invoke(logger, monkeypatch, command, options=()):
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), *options, "--", *command])
    return logger.main()


def read_record(root):
    return json.loads(next((root / "reports").glob("*.json")).read_text())


@pytest.mark.parametrize("exit_code", [0, 3])
def test_records_actual_result_and_jst(logger, tmp_path, monkeypatch, exit_code):
    assert invoke(logger, monkeypatch, [sys.executable, "-c", f"print('synthetic'); raise SystemExit({exit_code})"],
                  ["--input", "synthetic.txt", "--category", "DEV"]) == exit_code
    record = read_record(tmp_path)
    assert record["raw_returncode"] == record["wrapper_exit_code"] == record["exit_code"] == exit_code
    assert record["termination_signal"] is None
    assert record["status"] == ("passed" if exit_code == 0 else "failed")
    assert record["started_at_jst"].endswith("+09:00")
    assert record["finished_at_jst"].endswith("+09:00")
    assert record["case_id"] == "unknown"
    assert record["category"] == "DEV"
    assert record["git_commit"] == git(tmp_path, "rev-parse", "HEAD").stdout.strip()
    assert record["stdout"] == "synthetic\n"
    assert record["inputs"][0]["sha256"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_missing_command_is_logged_as_failure(logger, tmp_path, monkeypatch):
    assert invoke(logger, monkeypatch, [str(tmp_path / "does-not-exist")]) == 127
    record = read_record(tmp_path)
    assert record["status"] == "failed"
    assert record["raw_returncode"] is None
    assert record["wrapper_exit_code"] == 127
    assert "FileNotFoundError" in record["error"]


@pytest.mark.parametrize("input_name", ["absent.csv", "."])
def test_unreadable_input_has_log_without_starting_command(logger, tmp_path, monkeypatch, input_name):
    assert invoke(logger, monkeypatch, [sys.executable, "-c", "raise SystemExit(99)"],
                  ["--input", input_name]) == 2
    record = read_record(tmp_path)
    assert record["status"] == "failed"
    assert not record["command_started"]
    assert record["inputs"][0]["sha256"] is None
    assert record["inputs"][0]["error"]
    assert record["raw_returncode"] is None


def test_permission_error_is_recorded(logger, tmp_path, monkeypatch):
    original_open = Path.open

    def deny_sample(path, *args, **kwargs):
        if path == tmp_path / "synthetic.txt":
            raise PermissionError("synthetic permission denial")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_sample)
    assert invoke(logger, monkeypatch, [sys.executable, "-c", "raise SystemExit(99)"],
                  ["--input", "synthetic.txt"]) == 2
    record = read_record(tmp_path)
    assert "PermissionError" in record["inputs"][0]["error"]
    assert not record["command_started"]


@pytest.mark.parametrize("change", ["tracked", "staged", "untracked"])
def test_dirty_source_is_rejected(logger, tmp_path, monkeypatch, change):
    name = "new.py" if change == "untracked" else "synthetic.txt"
    (tmp_path / name).write_text("changed source", encoding="utf-8")
    if change == "staged":
        git(tmp_path, "add", name)
    assert invoke(logger, monkeypatch, [sys.executable, "-c", "raise SystemExit(99)"]) == 2
    record = read_record(tmp_path)
    assert "未コミット" in record["error"]
    assert record["git_status"]
    assert not record["command_started"]


def test_non_git_directory_is_logged(logger, tmp_path, monkeypatch):
    shutil.rmtree(tmp_path / ".git")
    assert invoke(logger, monkeypatch, [sys.executable, "-c", "raise SystemExit(99)"]) == 2
    record = read_record(tmp_path)
    assert "Git情報" in record["error"]
    assert not record["command_started"]


def test_wrapper_environment_is_not_claimed_as_target(logger, tmp_path, monkeypatch):
    target_venv = tmp_path / ".target-venv"
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(target_venv)], check=True)
    target_python = target_venv / "bin/python"
    assert invoke(logger, monkeypatch, [str(target_python), "-c", "import sys; print(sys.prefix)"]) == 0
    record = read_record(tmp_path)
    assert record["wrapper_environment"]["prefix"] == sys.prefix
    assert record["stdout"].strip() == str(target_venv)
    assert record["command_environment"]["status"] == "unverified"
    assert "dependencies" not in record["command_environment"]


@pytest.mark.skipif(sys.platform == "win32", reason="POSIXシグナル終了規則")
def test_sigterm_cli_exit_matches_log(logger, tmp_path):
    result = subprocess.run([sys.executable, str(tmp_path / "scripts/run_logged.py"), "--",
                             sys.executable, "-c", "import os, signal; os.kill(os.getpid(), signal.SIGTERM)"],
                            cwd=tmp_path, capture_output=True, text=True)
    record = read_record(tmp_path)
    assert record["raw_returncode"] == -signal.SIGTERM
    assert record["termination_signal"] == signal.SIGTERM
    assert record["wrapper_exit_code"] == record["exit_code"] == result.returncode == 143
    assert record["status"] == "failed"
