# Champ / Scout指摘への修正・再レビュー記録

日時: 2026-10-20 17:19 JST（UTC+09:00）
case_id: unknown / parent_case_id: unknown
区分: DEV（Pythonログ修正）、UTL（環境・退避手順）
対象: PR #1 / 修正前コミット df06f85106d42e05c0e70452f5c5571628f3d178
目的: 実装に照合した指摘の解消。売買仕様・戦略・評価基準は変更しない。

## 照合結果と対応

| 指摘 | 確認事実・修正 | 対応ファイル/確認 |
| --- | --- | --- |
| 原本規則の継承不足（Champ高） | Git側16行に原本の全規則は含まれていなかった。Driveプロジェクト直下の原本と役割文書を実際に参照し、取得本文のスナップショット、日本語入口、全節対応表、同期・適用範囲を追加 | AGENTS.md、docs/governance/。原本更新日時2026-10-05 12:22:09.389 JST、明示版なし |
| ラッパーと対象環境の混同（Champ中） | sys.version/pip freezeはラッパーのものだった。wrapper_environmentへ明示的に分離し、command_environmentはunverifiedと記録 | 別venvのPythonを起動し、実際の対象prefixとラッパーprefixを区別するテスト |
| 未コミットコードの再現性（両者P2/中） | ファイル名だけではソース版を特定できなかった。正式ログはクリーンなGitコミットからの実行に限定 | 追跡済み変更・ステージ済み変更・未追跡コードの3経路でコマンド起動前の拒否を確認 |
| 入力失敗ログの欠落（両者P2/中） | 入力読込が開始記録より前だった。開始記録を先に作成し、入力ごとの例外・失敗フェーズ・未起動を残す | 存在しない入力、ディレクトリ入力、人工PermissionErrorの各テスト |
| シグナル終了コード不一致（Scout P3） | raw=-15をsys.exitへ渡すと241になっていた。raw_returncode、termination_signal、wrapper_exit_codeを分離 | 実際のCLI/子プロセスでSIGTERMを発生させ、raw=-15、signal=15、CLI終了値=ログ値=143を確認 |
| 証跡退避手順不足（両者） | Git対象外の証跡の永続先・復元手順がなかった。退避対象、manifest、転送後の読み戻し、復元照合、環境破棄前の条件を文書化 | docs/evidence-retention.md。人工2ファイルでtar/sha256sumの手順を実施、復元2/2一致。永続先への実退避は未実施 |
| DEV区分不足（Champ補足） | 原本16節でDEV/RES/MISCを確認し、原本に基づいて追加 | DEVのログテスト。推測による独自区分の追加なし |
| 未来データ改変テスト（原本11節） | 現行のCloseTime選別に対し、未来価格改変・未来行削除・未来行追加後も過去結果が不変であることを追加確認 | tests/test_time_boundary.py。選別ロジック自体の変更なし |

## 参照と変更範囲

参照資料: ユーザーが貼り付けたChamp/Scout指摘、Drive原本AGENTS.md、Codex役割v1.0、PR #1の実装・作業記録。
Driveの同名ファイルは親フォルダで識別。別コピーとの取得本文一致も確認。ハッシュはLF正規化した取得本文のもので、Drive原本バイト列や過去報告のSHAと一致したとは主張しない。取得元と対応表はdocs/governance/rules-provenance.md。

変更: scripts/run_logged.py、tests/test_run_logged.py、tests/test_time_boundary.py、AGENTS.md、README.md、docs/validation-logs.md、docs/data-intake.md、docs/governance/drive-agents.snapshot.md、docs/governance/rules-provenance.md、docs/evidence-retention.md、本記録。

## 実行コマンド・結果

- `.venv/bin/python -m pytest`: 22 passed in 2.61s。
- `bash scripts/check_clean_setup.sh`: 空のvenvで固定依存のインストール・pip check成功。22 passed in 2.39s。既存.venv保持。
- `.venv/bin/python -m pip check`: No broken requirements found。
- `bash -n scripts/setup.sh scripts/check_clean_setup.sh`: 成功。
- `git diff --check`: 成功。
- `git ls-remote origin refs/heads/setup/python-validation`: リモートも修正前df06f85であることを確認。他者の後続変更なし。
- 退避手順の人工リハーサル: 一時領域のreports/RUN.jsonとdata/raw/DATA.metadata.jsonをsha256sumでmanifest化し、tar -czfで格納、読み戻しSHA一致、tar -xzfで空ディレクトリへ復元しsha256sum -c成功、全2ファイルのバイト一致を確認。機械記録はGit対象外のreports/retention-rehearsal.json。
- 人工アーカイブSHA256: 68e42b4bfda3fb63a9442eb479782df52976332a312aade3923dbcf67108de5e。永続先はunknown、実退避実施フラグはfalse。

## 未確定・未実施・限界

- 通常ログ・メタデータの永続保存先、保存担当、期間、バックアップ頻度・第二保管先は未確定。Gドライブ配下は候補であり、本作業で確定・作成・転送していない。正式な運用開始・環境破棄前に決定が必要。
- 対象コマンドの実行環境は自動認定しない。wrapper_environmentの依存を対象のものとして使わず、対象側の版出力等で別途確認する。
- クリーンコミットは追跡済みコードの再現性を補う。ignored/外部コード、可変外部サービス、実行中の入力やコード変更は保全しない。正式検証では使用コードを追跡し、全入力を宣言・固定する。
- 対象プロセスのシグナル終了はテスト済み。ラッパー自身へのシグナル転送やタイムアウト制御は未実装。強制終了時のrunningは成功扱いしない。
- スキーマv2で環境フィールドを分離。exit_codeはwrapper_exit_codeの別名とし、シグナル時のv1との意味の差を文書化。旧ログは書き換えない。
- 受入は手動。excludedデータを自動拒否する機能は追加していない。
- available_atによる配信遅延、特徴量生成、MTF結合、戦略全体の漏洩監査は未実装/未実施。最小選別テストの成功を戦略全体へ拡張しない。
- 実市場データ・戦略成績・OOS・MQLコンパイル・MT4実行は未実施。
- 公式TRACEは発行していない。通常JSONログや本記録を公式TRACE保存済みとは扱わない。
- pipキャッシュ権限警告は残るが、キャッシュなしの依存導入・テストは成功。

engineering_status: REGRESSION_PASSED（上記ローカル試験範囲）
decision: 追加検証（運用採用や戦略採用の判定ではない）
next_owner: Champ / Scout
next_action: PR更新後の差分・試験・原本対応を再レビュー。永続保存先等はユーザーが確定する。

## コミット後の実行確認

- 修正コミットb7be793のクリーン状態から `.venv/bin/python scripts/run_logged.py --category DEV --case-id unknown --input data/sample/bars.csv -- .venv/bin/python -m pytest` を実行。22 passed in 2.06s、対象終了コード0・wrapper終了コード0。実行ログ: reports/run-20261020T171908+0900-9d13a3d70c694eb69b543d97d53d939a.json（ローカル、未退避）。
- 最初のステージ済み差分検査では、原本スナップショットの末尾空行を検出した。本文は変更せず末尾改行1個へ正規化し、スナップショットハッシュと正規化方法の記録を更新した。最終差分検査を再実行する。
- リモートのCI結果はPRのChecksを参照。旧df06f85の成功を修正後コードのCI成功として扱わない。

## Champ再レビュー追加指摘：起動試行と成功の分離

日時: 2026-10-20 17:30 JST / 区分: DEV / case_id・parent_case_id: unknown
対象: 043fa0bへのChamp/Scout再レビュー。前回主要指摘の解消確認は受領したが、Champの新規指摘は実装上も妥当だった。

確認事実: 旧実装はcapture前にcommand_started=trueとしていたため、実行ファイル不存在でも起動成功のように記録された。
修正: command_attemptedを起動試行、command_startedをPopenの生成成功確認として分離。成功後だけPIDとstarted=trueを保存して終了を待つ。起動失敗はattempted=true/started=false/PID=null/raw_returncode=null/終了コード127。準備失敗は両フラグfalse・終了コード2を維持する。

変更ファイル: scripts/run_logged.py、tests/test_run_logged.py、docs/validation-logs.md、本記録。
実行: `.venv/bin/python -m pytest` → 23 passed in 2.45s。`git diff --check` → 成功。
回帰確認: 実行ファイル不存在・実行権限なしの両方で起動なしを確認。正常/非正常の通常終了時には起動成功とPIDありを確認。入力失敗、クリーンコミット制限、SIGTERMの既存試験も成功。

旧ログは変更しない。started=trueはプロセス生成の成功だけを示し、プログラムの初期化・正常終了は保証しない。強制終了時に最後の記録から起動結果を推測しない。対象環境unverifiedなど既存の制約は維持する。

永続保存先・担当・期間・バックアップ頻度・第二保管先、実退避と読み戻しは依然未確定/未実施。環境整備のコード修正とは分けて残件管理し、正式検証の運用開始前に完了が必要。実市場データ評価、配信遅延/特徴量/MTFの監査、MQLコンパイル・MT4実行は未実施。
engineering_status: REGRESSION_PASSED（ローカル23テスト） / decision: 追加検証 / next_owner: Champ・Scout / next_action: 起動状態修正の差分を再確認。mainへはマージしない。
