#!/usr/bin/env bash
# 既存.venvを保持し、一時ディレクトリの空のvenvで確認する。
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
validation_tmp="$(mktemp -d)"
trap 'rm -rf -- "$validation_tmp"' EXIT
VENV_DIR="$validation_tmp/venv" bash scripts/setup.sh
