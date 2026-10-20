# 追加環境整備の確認記録

日時: 2026-10-20 15:58 JST（UTC+09:00）
区分: UTL / 案件ID: unknown
環境: Linux x86_64 / Python 3.12.14

## 変更内容

1. scripts/setup.sh に VENV_DIR を追加。既存.venvを保持して一時環境で再構築できる scripts/check_clean_setup.sh とGitHub Actionsを追加した。
2. docs/data-intake.md と docs/templates/data-metadata.json を追加。生成元・時刻仕様・品質・ハッシュを記録し、未確認のデータを初期状態で除外する手順を定めた。
3. scripts/run_logged.py、docs/validation-logs.md、tests/test_run_logged.py を追加。JST日時、コマンド、依存、Git状態、入力ハッシュ、実測終了コードを記録する。READMEに各手順を追記した。

## 実行コマンド・実測結果

- `bash scripts/check_clean_setup.sh`: 固定依存を空の仮想環境にインストール成功。pip check成功。追加前7テスト、追加後10テストとも成功。最終結果は10 passed in 0.83s。一時環境は終了時に削除し、既存.venvは保持した。
- `.venv/bin/python scripts/run_logged.py --category UTL --case-id unknown --input data/sample/bars.csv -- .venv/bin/python -m pytest`: 10 passed in 0.85s、終了コード0。reports/にJSTログを生成した。
- ログ機能のテストで終了コード0、3、起動不能127を確認。JSTオフセット・入力ハッシュ・既定案件IDも確認した。
- `bash -n scripts/setup.sh scripts/check_clean_setup.sh`: 成功。
- `git diff --check`: 成功。
- Pythonのjson読込みでメタデータひな形の構文と初期excludedを確認し、生成ログのpassed/終了コード0/+09:00を確認した。
- `git check-ignore reports/run-example.json data/raw/example.metadata.json`: 両方Git対象外。

## 未実施・制約

- GitHub上のCIは未実行。設定ファイルをローカル追加した段階で、push後にGitHub側の実行確認が必要。
- クリーン確認は現在のクラウドOS上の空のvenvで実施。OS全体の新規構築や他OSでの確認ではない。
- pipキャッシュの権限警告は継続するが、キャッシュ無効でインストール・テストは成功。
- データ受入は手動手順。実データの取得・受入判定・戦略実装・成績検証は未実施。
- ログは標準出力をメモリに収集するため、大容量データを直接出力する用途は対象外。認証情報を含むコマンドや出力は記録しない。
- MQLコンパイル・MT4実行は未実施。
- 作業ブランチでローカルコミットし、リモートへのpush、mainへの直接push、自動マージは行わない。
