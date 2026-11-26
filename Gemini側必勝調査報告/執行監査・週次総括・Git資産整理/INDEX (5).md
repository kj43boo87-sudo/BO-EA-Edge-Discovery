# BO-EA-Edge-Discovery 正本資産台帳（INDEX.md — GSR-2026W49 確定版）

- **最終更新日**: 2026-11-27 (JST)
- **更新レコード**: `GSR-202611-W5-FRI`（`GSR-2026W49`: Track A `GSR-TKYFIX-002` OOS棄却 / Track B `GSR-NYCUT-001`・`GSR-LDNFIX-001` 棄却 / `GSR-TKYFIX-003` HOLD）
- **ローカルGit正本**: `C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery`
- **Git除外対象（厳守）**: 生M1 CSV（3通貨計775MB）、機会台帳CSV（OOS 214KB / MultiFix 1.76MB）、全行勝敗CSV、ZIP、`.gdoc`

## 1. ガバナンス・統括ドキュメント（`00_Project_Control`）

| ファイル名 | 確認区分 | SHA256 | 用途・状態 |
| :--- | :--- | :--- | :--- |
| `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md` | 現行版確認済み | `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9` | 総監督ガバナンス規定 v1.2 |
| `GSR-2026W49_decision.md` | 現行版確認済み | `36fb16fd5d67026078c8a667692bfa3191bfcbd330dbfaf7c618cf690271c73c` | W49 最終5ゲート裁定書（Track A/B） |
| `GSR-2026W49_Executive_Audit_and_Weekly_Summary_2026-11-27.md` | 現行版確認済み | `01164baadd945a6f3f077f897e4a93c706d30b4003996024aa8d22cc058970cb` | W49 週次統合総括書 |
| `GSR-202611-W5-FRI_Stage3_to_Next_Monday_Stage1_Handover.md` | 現行版確認済み | `503480bb58434c2cc4a6fd6415ff2d05bf64b8ebaa9b02dccd3b6b7b79b77b66` | 次週月曜（`GSR-2026W50`）引き継ぎ書 |
| `git_commit_gsr_2026w49.ps1` | 静的確認済み | `3a921cded49bff6f5bb6b71d50dc764bb2d0292b5c9a6409e55b8cf8b837c126` | 2段階同期スクリプト（PowerShell 5.1対応） |

## 2. GSR-2026W49 第1・第2工程 正本スクリプト・軽量集計CSV・マニフェスト（Git管理対象）

| 工程 | ファイル名 | 確認区分 | SHA256 |
| :--- | :--- | :--- | :--- |
| 第1工程 | `profile_market_structure_gsr_2026w49_v1_0.py` | 実行確認済み | `f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b` |
| 第1工程 | `exclusions_log_gsr_2026w49.csv` | 実行確認済み | `951cd609d678ff05dc4a1b62daf398f0bd89966e80e8bcd29a130d835a149757` |
| 第2工程 | `gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py` | 実行確認済み | `2b9c5017abd9f723536f05bd4f362888642af6b9cc53e0e107a412407a9ca479` |
| 第2工程 | `spark_audit_handover_manifest_gsr_2026w49.json` | 現行版確認済み | `e50c86b03a3acd954175101297495378e3e541352a909b1b7d5e3ff87aed5354` |
| 第2工程 | `oos_tkyfix002_standalone_and_diagnostics_gsr_2026w49.csv` | 実行確認済み | `1483b04b0f6f5e2c09e6d9aa36b5829534eee6d6385eff560f52acbf294190f1` |
| 第2工程 | `is_multifix_standalone_and_ablation_gsr_2026w49.csv` | 実行確認済み | `63e602fbe2b21321d85adb299299db82b0319ab33262c81efbf564b4e2884a8a` |
| 第2工程 | `is_multifix_disjoint_slices_and_yearly_gsr_2026w49.csv` | 実行確認済み | `80cad076b09fb835356f838074307e1295edaf4e95729eb9d80534528f5ab164` |
| 第2工程 | `GSR-2026W49_Stage2_OOS_and_MultiFix_Report.md` | 静的確認済み | `50744a7fddd5afbe76244ef3d4eadb81b8e7c177d64ae7cafdcad322654c3f96` |
