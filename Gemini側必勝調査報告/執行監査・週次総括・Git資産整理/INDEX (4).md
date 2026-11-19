# BO-EA-Edge-Discovery 正本資産台帳（INDEX.md — GSR-2026W48 確定版）

- **最終更新日**: 2026-11-20 (JST)
- **更新レコード**: `GSR-202611-W4-FRI`（親案件: `GSR-2026W48` / 採用候補: `GSR-TKYFIX-002` IS全5ゲート完全合格 `PASS_CANDIDATE`）
- **ローカルGit正本**: `C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery`
- **Google Drive ミラー**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告`
- **Git除外対象（厳守）**: 生M1 CSV（`2026.10.16USDJPY(3)-M1-No Session.csv` 等）、機会台帳CSV（12列/27列）、全行勝敗CSV、ZIPアーカイブ

## 1. ガバナンス・統括ドキュメント（`00_Project_Control`）

| ファイル名 | 確認区分 | SHA256 | 用途・状態 |
| :--- | :--- | :--- | :--- |
| `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md` | 現行版確認済み | `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9` | 総監督ガバナンス規定 v1.2（正本） |
| `GSR-2026W48_decision.md` | 現行版確認済み | `550824ec4adca228ccf641ea5cd5c9e260085ad3cff1ab6ec86d2a6e8c5be640` | **GSR-TKYFIX-002 IS全5ゲートPASS裁定書・One-Shot OOS契約・MQL4 1対1仕様** |
| `GSR-2026W48_Executive_Audit_and_Weekly_Summary_2026-11-20.md` | 現行版確認済み | `03d08346783b06d73f45c32e02ff8d07549e0e2b5bd1d921d3497268be2311fc` | 第3工程 週次統合総括書（16:36 JST確定値統合） |
| `GSR-202611-W4-FRI_Stage3_to_Next_Monday_Stage1_Handover.md` | 現行版確認済み | `c0a320b6f5b97201c9dbc3e38822d5b97b566fcb8c3bb85b9de0581aaa8f3836` | 次週月曜（`GSR-2026W49`）第1工程 引き継ぎ指示書 |
| `git_commit_gsr_2026w48.ps1` | 静的確認済み | `35ee30316125ead073b57c2d3d7d682a4791024d2956759d9e6d5879ee9dc1cf` | CRLF警告安全設計・GDrive＆GitHub 2段階同期スクリプト |

## 2. GSR-2026W48 第1・第2工程 正本スクリプト・軽量集計CSV・マニフェスト（Git管理対象）

| 工程 | ファイル名 | 確認区分 | SHA256（ローカル実測正本） | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| 第1工程 | `profile_is_market_structure_gsr_2026w48_v1_0.py` | 実行確認済み | `2b2c6f7201f23ac1ec0f886468a8727355d423d51a3c07034e60671edf18603d` | USDJPY IS機会台帳生成（OOS完全遮断） |
| 第1工程 | `stage1_to_stage2_handover_manifest_gsr_2026w48.json` | 現行版確認済み | `120bba20aed68ec7181471a54ab83fcc7d0168121b6ccb87deadb3c625687274` | 第1→第2工程引き継ぎマニフェスト |
| 第2工程 | `gsr_2026w48_is_tkyfix002_verifier_v1_0.py` | 実行確認済み | `74f079f670a83cd0202ffb2b4e7e0057a1497d81884d248233b4c9f4d85a0669` | GSR-TKYFIX-002 統計・アブレーション・Plateau検証 |
| 第2工程 | `is_standalone_and_ablation_summary_gsr_2026w48.csv` | 実行確認済み | `d548e3daa590ed876d71548b224c084271508acc1b090a98e97d7c869defd7c7` | 実験A アブレーション集計（2.9KB） |
| 第2工程 | `is_non_cumulative_marginals_and_yearly_gsr_2026w48.csv` | 実行確認済み | `b213a8ee36fad174c3d0496e531777b8c30ce6648164a1d766560d4c7878236d` | 実験B/C 非累積Plateau＆年次集計（11.6KB） |
| 第2工程 | `spark_audit_handover_manifest_gsr_2026w48.json` | 現行版確認済み | `3b29debe08aa16dd8816ace61150a79b2f99373c21c467e397a18756f78f7746` | Spark独立監査引き継ぎマニフェスト |
| 第2工程 | `GSR-2026W48_Stage2_IS_Report.md` | 現行版確認済み | `35d0669cc2b605405706ed259ef5cd0c7a059ccabba8745907cb5b09596169e7` | 第2工程IS統計検証レポート（ローカル正本） |
| Spark監査 | `GSR-202611-W4-WED-SPARK.md` | 現行版確認済み | Google Doc（`1thf-MgFuB04cgw8Hw1-SAHPNhXKOT4N_ScUfSxV2kfo`） | 独立監査 `PASS` 確定ログ |

## 3. 大容量データ参照台帳（Git除外・ハッシュ照合専用）

| ファイル名 | サイズ / 行数 | SHA256 | 保護ステータス |
| :--- | :--- | :--- | :--- |
| `2026.10.16USDJPY(3)-M1-No Session.csv` | 258,871,846 B / 4,424,800行 | `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29` | Git除外 / 2022+ OOS 1,783,913行 **完全ロック** |
| `is_2015_2021_opportunity_ledger_gsr_2026w48.csv` | 106,097 B / 1,177行（12列） | `4bd7471194c5a534863a81216e73ccc4317bcd25ebead831bbaa7b82d4278cf2` | Git除外 / 第1工程主台帳 |
| `is_2015_2021_opportunity_ledger_gsr_2026w48_masked_v22.csv` | 373,959 B / 1,177行（27列） | `279992b79c510fb68ab8ac556543ec37908b4ffbc9d9a54d298e35b4ce942e23` | Git除外 / 第1工程マスク台帳 |
