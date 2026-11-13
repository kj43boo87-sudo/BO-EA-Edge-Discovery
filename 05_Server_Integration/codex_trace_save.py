"""Validate and append one official Codex TRACE; standard library only."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

DEFAULT_ROOT = Path(r"G:\マイドライブ\AIトレーサビリティ\AI4者会談\進行中\Codex")
START = "<!-- RESEARCH_TRACE_START"
END = "<!-- RESEARCH_TRACE_END -->"


def validate(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("Exactly one complete TRACE block is required")
    if text.splitlines()[-1] != END:
        raise ValueError("END must be the final standalone line")
    header = re.fullmatch(r"🏷️ \[TRACE: ([A-Za-z0-9_.-]+) \| (採用|棄却|保留|追加検証) \| (.+)\]", text.splitlines()[0])
    if not header:
        raise ValueError("Invalid official TRACE header")
    start = text.index(START) + len(START)
    stop = text.find("-->", start)
    if stop < start or not text[stop + 3:text.index(END)].strip():
        raise ValueError("Metadata or body is incomplete")
    meta = {}
    for line in text[start:stop].strip().splitlines():
        key, sep, value = line.partition(":")
        if not sep or key.strip() in meta:
            raise ValueError("Invalid or duplicate metadata key")
        meta[key.strip()] = value.strip()
    required = {"ai_id", "session_title", "case_id", "parent_case_id", "decision", "target_market", "attachment_file", "part_info", "timestamp"}
    if not required.issubset(meta) or any(not meta[k] for k in required):
        raise ValueError("Required metadata is missing")
    if meta["ai_id"] != "codex" or meta["case_id"] != header[1] or meta["decision"] != header[2] or meta["session_title"] != header[3]:
        raise ValueError("Codex metadata does not match the header")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST", meta["timestamp"]):
        raise ValueError("Timestamp must explicitly use JST")
    stamp = datetime.strptime(meta["timestamp"], "%Y-%m-%d %H:%M:%S JST")
    if not re.fullmatch(r"[1-9]\d*/[1-9]\d*", meta["part_info"]):
        raise ValueError("Invalid part_info")
    part, total = map(int, meta["part_info"].split("/"))
    if part > total:
        raise ValueError("Part exceeds total")
    if "<!--" in text[start:stop] or text[:text.index(START)].strip() != text.splitlines()[0]:
        raise ValueError("Unexpected content before metadata")
    return text.encode("utf-8"), meta, stamp


def save_trace(text, root=DEFAULT_ROOT):
    data, meta, stamp = validate(text)
    digest = hashlib.sha256(data).hexdigest()
    name = f'{stamp:%Y%m%d_%H%M%S}_codex_{meta["case_id"]}_{meta["part_info"].replace("/", "of")}_{digest}.md'
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / name
    try:
        with path.open("xb") as output:
            output.write(data)
        state = "saved"
    except FileExistsError:
        if path.read_bytes() != data:
            raise RuntimeError("Existing evidence differs; refusing overwrite")
        state = "already_saved"
    if path.read_bytes() != data:
        raise RuntimeError("Read-back verification failed")
    return {"status": state, "path": str(path.resolve()), "sha256": digest, "bytes": len(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    try:
        result = save_trace(args.input.read_text(encoding="utf-8-sig"), args.root)
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f"TRACE_SAVE_FAILED: {error}\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
