# 環境整備の確認記録

- 日時: 2026-10-20 15:47 JST（UTC+09:00）
- 区分: UTL / 案件ID: unknown
- 対象: BO-EA-Edge-Discovery
- 開始時点の実測: 初期コミット ee5c679、追跡ファイルは README.md と .gitignore のみ。作業ツリーはクリーン。
- 実測環境: Linux x86_64、Python 3.12.14、pip 25.0.1。
- 依存: pandas 3.0.6、numpy 2.5.4、pytest 9.1.1。推移依存を含め requirements.lock に固定。

## 変更内容

日本語AGENTS.md、.venv、固定依存、セットアップスクリプト、src/、tests/、docs/、data/sample/、reports/を整備。既存READMEと.gitignoreは保持して追記した。
人工データだけを用いた確定足選択のユーティリティとテストを追加した。

## 実行コマンドと確認結果

- `python3 --version`: Python 3.12.14。
- `git status --short --branch` / `git log -5 --oneline` / `git ls-files`: 上記開始状態を確認。
- `git switch -c setup/python-validation`: レビュー用ブランチ作成。
- `bash scripts/setup.sh`: 初回はサンドボックスからプロキシへの接続が拒否され、pipが終了コード1で失敗。パッケージが存在しないことを示す失敗ではない。
- ネットワークアクセス付きで `bash scripts/setup.sh` を再実行: インストール成功、`pip check` 成功、7 tests passed。
- `.venv/bin/python -m pip freeze > requirements.lock`: 実測した全依存バージョンを固定。
- `bash scripts/setup.sh`: 固定後も成功。既存.venvの再利用であり、別OSや空の環境での再構築確認ではない。
- `bash -n scripts/setup.sh`: 成功。
- `git diff --check`: 成功。
- `git check-ignore .venv/pyvenv.cfg .env.production credentials/account.json data/raw/prices.csv data/tick_data/ticks.csv reports/result.csv`: 全例が除外対象。
- `git status --short --untracked-files=all`: 人工サンプル・テスト・コード・文書が管理可能であることを確認。

テスト結果: 7 passed（固定後の実行 0.24秒）。未来足の除外、同時刻足の許可、利用可能な足がない場合の空結果、同一時刻のUTC/JST比較、タイムゾーンなし入力の拒否、CloseTime欠損の拒否を確認。

## 未実施・未解決事項

- 売買戦略実装、実市場データの取得・成績検証、パラメータ探索は実施していない。
- MQLコンパイル、MT4実行は実施していない。
- Python 3.12以外、Windowsネイティブ、macOSは未検証。
- pipキャッシュの権限警告は残るが、キャッシュ無効のままインストールとテストは成功した。
- 実データの生成元・配信遅延・タイムゾーン・足定義はデータ導入時に確認が必要。
- Git保存は作業ブランチのローカルコミット。リモートへのpush、PR作成、mainへの直接push、自動マージは行わない。
