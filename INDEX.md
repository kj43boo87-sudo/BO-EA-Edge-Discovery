# INDEX — 執行監査・週次総括・Git資産整理（Gemini側必勝調査報告：第3工程）

- **保管パス（第3工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理`
- **関連パス（第1工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検`
- **関連パス（第2工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証`
- **最終更新日**: `2026-11-06`

---

## 1. 今週の執行監査・最終ゲート判定サマリ（2026年11月第1週）

| Case ID / 提案ID | 対象通貨・時間足 | テーマ・検証段階 | 最終5ゲート判定 | 正式決定・次工程 |
| :--- | :--- | :--- | :--- | :--- |
| **`BO-EUR-005`** | `EURUSD` M1 | 東京箱ブレイク→再侵入（`Control I`）・境界再テスト反発（`R`）・再ブレイク（`B`）のIS期間（2015–2021）統計・432セルPlateau検証およびSpark独立監査 | ①台帳一致: **PASS**<br>②IS HAC下限: **FAIL**<br>③近傍Plateau: **FAIL**<br>④Spark監査: **PASS**<br>⑤MT4約定・摩擦耐性: **FAIL** | **棄却・凍結**<br>（`VIEWED_EVAL` 2022–2026年 748件は未開封のまま開発終了） |
| **`Proposal_A`** | `USDJPY` M1/M5 | 東京箱ブレイク失敗・即時実体再侵入（異市場比較・M5傾きフィルタ付）※EURUSD単純再侵入は `BO-EUR-005` 棄却により除外 | 第1工程スクリプト実装済み（Label-Free機会件数抽出待ち） | **追加検証**<br>（第1工程ローカル実行待ち） |
| **`Proposal_B`** | `USDJPY`, `EURJPY`, `AUDJPY` M1/M5 | 確定M5非トレンド環境限定・M1 BB 2.8σクライマックス逆張り（単発独立化・NYクローズ除外） | 第1工程スクリプト実装済み（Label-Free機会件数抽出待ち） | **追加検証**<br>（第1工程ローカル実行待ち） |
| **`Proposal_C`** | `EURUSD`, `USDJPY`, `GBPUSD` M1/M5 | 確定M5 PO同調 × M1ボラ収縮後のEMA20反発・前足高安ブレイク回復 | 第1工程スクリプト実装済み（Label-Free機会件数抽出待ち） | **追加検証**<br>（第1工程ローカル実行待ち） |
| **既存逆張りEA群** | 5通貨ペア（60 CSV） | `BO_BB3Sigma_Reversal_5M_*.csv` 直近成績・0.1pipストレス耐性・5分内重複・$t+1 \sim t+6$ 連続性一括点検 | 第1工程スクリプトに `--audit-reports-glob` 実装済み | **追加検証**<br>（ローカル一括点検待ち） |

---

## 2. 本フォルダ（第3工程：執行監査・週次総括・Git資産整理）保管ファイル一覧

| ファイル名 | 種別 | サイズ (bytes) | SHA256（実測値） | 内容・用途 |
| :--- | :--- | :--- | :--- | :--- |
| `WEEKLY_EXECUTIVE_AUDIT_AND_HANDOVER_20261106.md` | Markdown | 10,861 | `bfaa3f3a2f9696033614441f1d2362e9b27ecef6812abb486b6df06ecaf25e2c` | 2026年11月第1週 執行監査・最終5ゲート判定・週次総括・引き継ぎ指示書（公式TRACE付） |
| `BO-EUR-005_decision.md` | Markdown | 8,961 | `2d0e2e05b8dcd86c2993b2e0fea0f8c8505d609e654a5110ce49e7882c255109` | `BO-EUR-005` 最終決定記録（ISゲート棄却・凍結 / `VIEWED_EVAL` 748件未開封維持）※第2工程と同ハッシュ正本 |
| `BO-EUR-005_Spark_Audit_and_Handover_Log_2026-11-05.md` | Markdown | 7,077 | `6c663ad984c4f68f998a8a8ad0881f8787d082c7f321b2dc54bfe765a5a24fad` | `BO-EUR-005` Gemini引き継ぎ＋Spark独立性能監査（全文）＋執行監査統合ログ ※第2工程と同ハッシュ正本 |
| `DECISION_TEMPLATE.md` | Markdown | 8,138 | `261cd94bca5bdc91f757555742c614a4d09885cc2df2fa211adffa361cf4797f` | 判定結果（採用候補 / 棄却・凍結 / 保留 / 追加検証）を記録する公式TRACEおよび `decision.md` 標準テンプレート |
| `sync_weekly_assets_and_git_commit.ps1` | PowerShell | 12,643 | `be7baea3360aacd75ecba461803035e58c3e8e860d1f8202182ed814c1820fda` | 3工程の `.py` / `.md` 実ソースSHA256再計算・リポジトリ同期・`INDEX.md` 反映・大容量CSV除外Gitコミット自動化スクリプト |
| `INDEX.md` | Markdown | — | （本ファイル） | 第3工程および全3工程横断のプログラム・ドキュメント資産索引 |

---

## 3. 全3工程横断 検証スクリプト（`.py`）・主要証跡のSHA256対応表

| 保管工程 | ファイル名 | 版 / 規模 | SHA256（実測値） | 状態区分（手順書 規則4） |
| :--- | :--- | :--- | :--- | :--- |
| 第1工程 | `profile_is_market_structure_2015_2021_v1_2.py` | v1.2.0 (43,374 B) | `a7fa4ada92f47c5adb2d01db7e4c823bd8a5820fb06c23c2f13951027aaae2eb` | 静的確認済み（ゼロ引数自動探索版） |
| 第1工程 | `profile_is_market_structure_2015_2021.py` | v1.1.0 (39,704 B) | `e37a9e62626d76ae90b7013de9842bcca007906cabad4b7e5afe0ca08d0111ce` | 旧版保持（CLI引数指定版） |
| 第2工程 | `bo_eur_005_is_plateau_verifier.py` | v2.4 (45,367 B) | `7c125ea7c02db45a2e2af779f9dc7af530639cf900a3109296667207689703a9` | **実行確認済み**（`BO-EUR-005` IS/Plateau検証） |
| 第2工程 | `output_is_plateau_20261104_173018/spark_audit_handover_manifest.json` | JSON (19,797 B) | `2b5c704fa79db890ec8440e23778c1412cf6c63ca374ddec419f00bdf280c783` | **実行確認済み**（Git登録対象マニフェスト） |
| 第2工程 | `output_is_plateau_20261104_173018/is_standalone_summary.csv` | 3 rows (688 B) | `e1490cbc88dc3773bfca8c06978be5092f0612b2361aafe0990dc17ba854a736` | **実行確認済み**（Git登録対象サマリー） |
| 第2工程 | `output_is_plateau_20261104_173018/is_paired_summary.csv` | 2 rows (572 B) | `050b8b9a134d3a078c10b9f4dabca991479fbb95ef6a8f6b519a0598cde030ea` | **実行確認済み**（Git登録対象サマリー） |
| 第2工程 | `output_is_plateau_20261104_173018/is_yearly_breakdown.csv` | 21 rows (1,304 B) | `37b664de1fd57988012ac8c4a944f4ccd17a5945c60258bc374ddec419f00bd` | **実行確認済み**（Git登録対象サマリー） |
| 第2工程 | `output_is_plateau_20261104_173018/is_outcomes.csv` | 1,050 rows (143,954 B) | `b5e2550610707262c74211f9816764acd8affd3d8a177bf70601e6befce605a3` | Drive保管（Git除外：明細CSV） |
| 第2工程 | `output_is_plateau_20261104_173018/is_plateau_grid.csv` | 432 rows (107,400 B) | `cfed8beafda015dc542a3e53cc824329a5e36a786a4083f1dc97dce5683b514d` | Drive保管（Git除外：格子CSV） |
