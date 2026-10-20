#!/usr/bin/env python3
"""コマンドを実行し、JST・実測結果をGit対象外のJSONへ保存する。"""
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", choices=["SYS", "UTL", "BO", "FX", "STK"], default="UTL")
    parser.add_argument("--case-id", default="unknown")
    parser.add_argument("--input", action="append", default=[], help="入力ファイル。複数指定可")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("-- の後に実行コマンドが必要です")
    inputs = []
    for name in args.input:
        path = ROOT / name
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        inputs.append({"path": name, "sha256": digest})
    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"run-{datetime.now(JST):%Y%m%dT%H%M%S%z}-{uuid.uuid4().hex}.json"
    commit = capture(["git", "rev-parse", "HEAD"])
    status = capture(["git", "status", "--porcelain"])
    dependencies = capture([sys.executable, "-m", "pip", "freeze"])
    record = {
        "started_at_jst": now(), "category": args.category, "case_id": args.case_id,
        "command": command, "cwd": str(ROOT), "python": sys.version,
        "platform": platform.platform(), "git_commit": commit.stdout.strip(),
        "git_status": status.stdout, "git_status_exit_code": status.returncode,
        "dependencies": dependencies.stdout.splitlines(),
        "dependencies_exit_code": dependencies.returncode, "inputs": inputs,
        "status": "running", "exit_code": None,
    }
    with report_path.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    try:
        result = capture(command)
        record.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr,
                      status="passed" if result.returncode == 0 else "failed")
    except OSError as exc:
        record.update(exit_code=127, stdout="", stderr=str(exc), status="failed")
    record["finished_at_jst"] = now()
    report_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(record["stdout"], end="")
    print(record["stderr"], end="", file=sys.stderr)
    print(f"ログ: {report_path}")
    return record["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
