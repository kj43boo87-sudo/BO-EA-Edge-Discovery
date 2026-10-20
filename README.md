# BO-EA-Edge-Discovery

BO用EA・サインツール開発のPython検証基盤です。今回の範囲は環境整備と人工データの時刻境界テストのみです。売買戦略・成績検証は含みません。

## 環境の再構築

Python 3.12 と Bash を用意し、リポジトリのルートで実行してください（Linux/macOS/WSL）。動作確認環境は docs/setup-validation.md に記録します。

```bash
bash scripts/setup.sh
# Pythonを指定する場合
PYTHON_BIN=python3.12 bash scripts/setup.sh
```

スクリプトは .venv を作成し、requirements.lock の固定依存をインストールして依存整合性とテストを確認します。既存の .venv がある場合は再利用します。完全に作り直す場合は既存 .venv を別名へ退避してから実行してください。他のPythonバージョン・OSは未検証です。

## テスト実行

```bash
.venv/bin/python -m pytest
.venv/bin/python -m pip check
```

src/bo_validation/time_boundary.py はタイムゾーン付き CloseTime と判定時刻を比較し、確定足だけを返します。未来の足による穴埋めはしません。人工サンプルは実市場データではありません。

## データの配置

- data/sample/: Git管理する人工サンプルと生成元の説明のみ。
- data/raw/: 原本の実データ（Git対象外）。原本を上書きしないでください。
- data/processed/: 派生データ（Git対象外）。
- reports/: 生成レポート・検証ログ（Git対象外）。

実データごとに生成元、取得日時、銘柄、時刻基準、タイムゾーン、OpenTime/CloseTimeの意味、加工履歴をローカルのメタデータに記録してください。生成元不明のデータは検証から除外し、理由を記録します。固定時差を推測して補正しないでください。実データの配信遅延等の確認は未実施です。

## コードと実データの管理方針

コード・テスト・文書・固定依存・小さな人工サンプルをGit管理します。仮想環境、認証情報、実データ、大容量Tickデータ、生成レポートはGit管理しません。実データは必ず data/sample/ の外へ置きます。.gitignore は既に追跡済みのファイルには効かないため、コミット前に `git status` と `git diff --cached` を確認してください。

作業ルールは AGENTS.md を参照してください。ログ日時はJST、環境整備の区分はUTL、案件ID不明時はunknownです。市場検証時はBO/FX/STKを区別します。mainへ直接push・自動マージせず、作業ブランチでレビューします。

## 追加の再現性確認とCI

```bash
bash scripts/check_clean_setup.sh
```

既存の .venv を保持し、一時ディレクトリに空の仮想環境を作って固定依存・依存整合性・全テストを確認します。一時環境は終了時に削除します。これはOS全体の再構築ではありません。
GitHub Actions（.github/workflows/python-validation.yml）でもpush・PR・手動実行時に同じ確認を行います。CIは読み取り権限のみで、pushやマージは行いません。GitHub上の実行結果はリモートに反映後に確認してください。

## 実データの受入とJSTログ

- 受入手順: [docs/data-intake.md](docs/data-intake.md)
- メタデータひな形: [docs/templates/data-metadata.json](docs/templates/data-metadata.json)。初期状態は検証対象外です。
- ログの実行方法と記録ひな形: [docs/validation-logs.md](docs/validation-logs.md)

```bash
.venv/bin/python scripts/run_logged.py --category UTL --case-id unknown --input data/sample/bars.csv -- .venv/bin/python -m pytest
```

## 再レビュー向け補足

正式ログはクリーンな作業ブランチのコミットから実行してください。ラッパー自身のPython/依存と対象コマンドの環境は区別して記録します。対象環境は自動確定せず、対象側の版出力で確認します。
Drive原本の規則継承と同期方法は [規則継承記録](docs/governance/rules-provenance.md)、入力失敗・シグナル終了の記録仕様は [JSTログ手順](docs/validation-logs.md) を参照してください。
通常ログ・受入メタデータの永続保存先は未確定です。[証跡の退避・復元手順](docs/evidence-retention.md) に従い、環境破棄前に保存先の確定と読み戻しを実施してください。
