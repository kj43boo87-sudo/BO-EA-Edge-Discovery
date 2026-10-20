#!/usr/bin/env python3
"""クリーンなGitコミットのコマンドを実行し、実測結果をJSTで保存する。"""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
JST = timezone(timedelta(hours=9), name="JST")


def now():
    return datetime.now(JST).isoformat(timespec="seconds")


def capture(command):
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, errors="replace")


def require_git(arguments):
    result = capture(["git", *arguments])
    if result.returncode:
        raise ValueError(f"Git情報を取得できません: {result.stderr.strip()}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", choices=["SYS", "UTL", "DEV", "BO", "FX", "STK", "RES", "MISC"], default="UTL")
    parser.add_argument("--case-id", default="unknown")
    parser.add_argument("--input", action="append", default=[], help="入力ファイル。複数指定可")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("-- の後に実行コマンドが必要です")
    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"run-{datetime.now(JST):%Y%m%dT%H%M%S%z}-{uuid.uuid4().hex}.json"
    record = {
        "schema_version": 2,
        "started_at_jst": now(), "category": args.category, "case_id": args.case_id,
        "command": command, "cwd": str(ROOT),
        "wrapper_environment": {
            "python": sys.version, "executable": sys.executable,
            "prefix": sys.prefix, "platform": platform.platform(),
        },
        "command_environment": {
            "status": "unverified",
            "reason": "任意コマンドの環境は推測しない。対象側で版・依存を出力して確認すること。",
        },
        "git_commit": None, "git_status": None, "inputs": [],
        "status": "running", "phase": "preparing", "command_started": False,
        "raw_returncode": None, "termination_signal": None,
        "wrapper_exit_code": None, "exit_code": None, "stdout": "", "stderr": "",
    }

    def save():
        report_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 入力やGitの確認に失敗しても、開始記録が残る。
    with report_path.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    try:
        record["git_commit"] = require_git(["rev-parse", "HEAD"]).strip()
        record["git_status"] = require_git(["status", "--porcelain", "--untracked-files=all"])
        if record["git_status"]:
            raise ValueError("未コミットまたは未追跡の変更があります。正式ログ実行前にコミットしてください。")
        dependencies = capture([sys.executable, "-m", "pip", "freeze"])
        record["wrapper_environment"].update(
            dependencies=dependencies.stdout.splitlines(),
            dependencies_exit_code=dependencies.returncode,
            dependencies_stderr=dependencies.stderr,
        )
        if dependencies.returncode:
            raise ValueError("ラッパーの依存情報を取得できません")
        for name in args.input:
            entry = {"path": name, "sha256": None}
            record["inputs"].append(entry)
            try:
                with (ROOT / name).open("rb") as stream:
                    entry["sha256"] = hashlib.file_digest(stream, "sha256").hexdigest()
            except OSError as exc:
                entry["error"] = f"{type(exc).__name__}: {exc}"
                raise
        record.update(phase="command", command_started=True)
        save()
        result = capture(command)
        raw = result.returncode
        wrapper_code = 128 - raw if raw < 0 else raw
        record.update(raw_returncode=raw, termination_signal=-raw if raw < 0 else None,
                      wrapper_exit_code=wrapper_code, exit_code=wrapper_code,
                      stdout=result.stdout, stderr=result.stderr,
                      status="passed" if raw == 0 else "failed")
    except (OSError, ValueError) as exc:
        code = 127 if record["command_started"] else 2
        record.update(wrapper_exit_code=code, exit_code=code, status="failed",
                      error=f"{type(exc).__name__}: {exc}", stderr=str(exc))
    record["finished_at_jst"] = now()
    save()
    print(record["stdout"], end="")
    print(record["stderr"], end="", file=sys.stderr)
    print(f"ログ: {report_path}")
    return record["wrapper_exit_code"]


if __name__ == "__main__":
    sys.exit(main())
