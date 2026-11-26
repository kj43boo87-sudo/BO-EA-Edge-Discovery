# BO-EA-Edge-Discovery 正本資産台帳（INDEX.md — GSR-2026W49 確定版）

- **最終更新日**: 2026-11-27 (JST)
- **更新レコード**: `GSR-202611-W5-FRI`（`GSR-2026W49`: `GSR-TKYFIX-002` / `GSR-NYCUT-001` 永久凍結、`GSR-LDNFIX-001` → `GSR-LDNFIX-002` 次週W50最優先昇格、`GSR-TKYFIX-003` 低優先待機）
- **ローカルGit正本**: `C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery`
- **OOS保護**: EURUSD / GBPUSD 2022-01-01以降 完全未開封ロック（`oos_locked: true`）
- **Git除外対象（厳守）**: 生M1 CSV 3通貨（計775MB）、`oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv`（`3e5c583f...`）、`is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv`（`02728717...`）、旧クラウド先行版（3,109 B マニフェスト・`gsr_2026w49_stage2_multifix_and_oos_verifier_v1_0.py`）、ZIP、`.gdoc`

## 1. ガバナンス・統括ドキュメント（`00_Project_Control`）

| ファイル名 | 確認区分 | SHA256 | 用途・状態 |
| :--- | :--- | :--- | :--- |
| `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md` | 現行版確認済み | `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9` | 総監督ガバナンス規定 v1.2 |
| `GSR-2026W49_decision.md` | 現行版確認済み | `3608870163082dbee805400b06b9d22c398a85fc1305347b43723c144a0dc110` | W49 総監督確定最終裁定書 |
| `GSR-2026W49_Executive_Audit_and_Weekly_Summary_2026-11-27.md` | 現行版確認済み | `5611387c6a89ff02111f6ecdab16a965e15bb218a683c0c5eef62f26ee8b88a1` | W49 週次統合総括書（第1・第2・Aegis監査統合） |
| `GSR-202611-W5-FRI_Stage3_to_Next_Monday_Stage1_Handover.md` | 現行版確認済み | `029167c9a73a6bcba91f9cac8c3815bbaf098834517efde3658f8330728c8e47` | 次週W50（`GSR-LDNFIX-002`）引き継ぎ書 |
| `git_commit_gsr_2026w49.ps1` | 静的確認済み | `5860bb49a263d2eb6f8919dfbfe0be975a559b6be570648f1aa6c6d75870aa6e` | 2段階同期スクリプト（UTF-8 BOM・PS5.1対応） |

## 2. GSR-2026W49 正本スクリプト・軽量集計CSV・マニフェスト（`LOCAL_775MB_FULL_VERIFIED`）

| 工程 | ファイル名 | 確認区分 | SHA256 |
| :--- | :--- | :--- | :--- |
| 第1工程 | `profile_market_structure_gsr_2026w49_v1_0.py` (v1.0.2) | 実行確認済み | `f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b` |
| 第1工程 | `exclusions_log_gsr_2026w49.csv` (66行) | 実行確認済み | `951cd609d678ff05dc4a1b62daf398f0bd89966e80e8bcd29a130d835a149757` |
| 第2工程 | `gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py` | 実行確認済み | `2b9c5017abd9f723536f05bd4f362888642af6b9cc53e0e107a412407a9ca479` |
| 第2工程 | `oos_tkyfix002_standalone_and_diagnostics_gsr_2026w49.csv` | 実行確認済み | `1483b04b0f6f5e2c09e6d9aa36b5829534eee6d6385eff560f52acbf294190f1` |
| 第2工程 | `is_multifix_standalone_and_ablation_gsr_2026w49.csv` | 実行確認済み | `63e602fbe2b21321d85adb299299db82b0319ab33262c81efbf564b4e2884a8a` |
| 第2工程 | `is_multifix_disjoint_slices_and_yearly_gsr_2026w49.csv` | 実行確認済み | `80cad076b09fb835356f838074307e1295edaf4e95729eb9d80534528f5ab164` |
| 第2工程 | `spark_audit_handover_manifest_gsr_2026w49.json` (25,846 B) | 現行版確認済み | `e50c86b03a3acd954175101297495378e3e541352a909b1b7d5e3ff87aed5354` |
