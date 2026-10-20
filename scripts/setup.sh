#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" -c 'import sys; assert sys.version_info[:2] == (3, 12), "Python 3.12を指定してください"'
VENV_DIR="${VENV_DIR:-.venv}"
"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install -r requirements.lock
"$VENV_DIR/bin/python" -m pip check
"$VENV_DIR/bin/python" -m pytest
