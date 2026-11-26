# 第1工程「トレード手法の市場調査＆データ点検」INDEX（GSR-2026W49 更新版）

- **最新更新日**: 2026-11-23 JST
- **最新アクティブ案件ID**: `GSR-2026W49`
- **準拠ガバナンス**: `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md`（SHA256: `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9`）

---

## 1. 週次アクティブ成果物（GSR-2026W49）
| 種別 | ファイル名 | 状態 | 備考 / SHA256 |
| :--- | :--- | :--- | :--- |
| 生成スクリプト | `profile_market_structure_gsr_2026w49_v1_0.py` | クラウド検証済み・ローカル実行待ち | `725c54a0977083ba09d3c052ec3eece9cf79d040c6f962a763346d9fbef8f288` |
| 引き継ぎ書 | `HANDOVER_GSR_2026W49_STAGE1.md` | クラウド先行版作成済み | Proxy定数ゼロ・未取得全量値は `unknown` 明記 |
| マニフェスト | `stage1_to_stage2_handover_manifest_gsr_2026w49.json` | クラウド先行版作成済み | ローカル実行時に全量SHA256・行数で自動更新 |
| Track A 台帳 | `oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv` | ローカル実行待ち (`unknown`) | `GSR-TKYFIX-002` One-Shot OOS (2022+) |
| Track B 台帳 | `is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv` | ローカル実行待ち (`unknown`) | `GSR-TKYFIX-003` / `GSR-LDNFIX-001` / `GSR-NYCUT-001` (IS 2015–2021) |

---

## 2. 永久再検証禁止・凍結案件リスト（Permanent Exclusion List）
- `GSR-CLIMAX-001` / `GSR-PULLBACK-001` / `GSR-FAKEOUT-001` / `GSR-SURVEY-001`（`GSR-2026W46_decision.md` により棄却）
- `GSR-EXHAUST-001` / `GSR-SHOCKDECAY-001`（`GSR-2026W47_decision.md` により凍結）
- `BO-EUR-004` / `BO-EUR-005`（旧比較参照元・棄却済み）
- `GSR-TKYFIX-001` の `WEAK_SUB`（`0 <= wick_rejection_ratio < 0.25`, `TRAP-06` により無効・除外固定）
