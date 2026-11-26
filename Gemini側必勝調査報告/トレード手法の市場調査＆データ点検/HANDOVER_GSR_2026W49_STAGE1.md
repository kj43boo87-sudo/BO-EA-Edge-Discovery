# HANDOVER_GSR_2026W49_STAGE1 — 第1工程→第2工程 引き継ぎ書（ローカル全量実測確定版）

- **案件ID**: `GSR-2026W49`
- **実行日時 (JST)**: `2026-11-23T06:19:30+09:00`
- **スクリプト**: `profile_market_structure_gsr_2026w49_v1_0.py` (v1.0.2, SHA256: `f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b`)
- **Label-Free純度**: 勝敗列・リターン列を物理的に一切含まない純粋Label-Free出力
- **W48完全一致契約**: `is_cand = (wick_r >= 0.35 - 1e-9) or (bar_t_dir != move_dir)` により `NONE` / `PURE_STRONG` / `WEAK_SUB` を厳密分離

## 1. 生M1データ全量監査ログ
| 通貨ペア | Bytes | 総行数 | IS (2015–2021) 行数 | OOS (2022+) 行数 | SHA256 |
| :--- | ---: | ---: | ---: | ---: | :--- |
| USDJPY | 258,871,846 | 4,424,800 | 2,608,784 | 1,783,913 | `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29` |
| EURUSD | 258,932,307 | 4,424,366 | 2,610,900 | 1,781,411 | `029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d` |
| GBPUSD | 258,199,124 | 4,425,542 | 2,612,846 | 1,780,559 | `05468aa45b7e08a47fa7aff608af1d08d190fd6b5298534585f9c9554e7ab803` |

## 2. Track A (`GSR-TKYFIX-002` One-Shot OOS) 出力確定
- **ファイル**: `oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv` (SHA256: `3e5c583f8b8bb5bef00846c2048c90716cb01f071d2591b65998549359758d68`, 214,232 bytes)
- **プール総数**: 774 件 / **主契約 `PURE_STRONG`**: 256 件 / `NONE`: 428 件 / `EXCLUDED_TRAP06`: 90 件
- **6本連続性合格**: 774 件 / **除外ログ件数**: 3 件 ({'MISSING_ATR_HISTORY': 3})

## 3. Track B (マルチ・フィキシング IS専用 / `oos_locked: true`) 出力確定
- **ファイル**: `is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv` (SHA256: `0272871721a3e96b6ace75afaa72e13708c8d398355a2cc971459d8cdec1a1c1`, 1,760,257 bytes)
- **総抽出行数**: 5533 件 / **除外ログ件数**: 63 件 ({'MISSING_SIGNAL_BAR_HOLIDAY_OR_GAP': 51, 'MISSING_ATR_HISTORY': 10, 'MISSING_15M_WINDOW': 1, 'FAIL_GAP_T+6': 1})
- **候補別内訳**: `{"GSR-TKYFIX-003|USDJPY": {"total_rows": 1173, "continuity_pass_rows": 1173, "grade_counts": {"WEAK_SUB": 199, "NONE": 615, "PURE_STRONG": 359}, "exclusions": 12}, "GSR-LDNFIX-001|EURUSD": {"total_rows": 1127, "continuity_pass_rows": 1127, "grade_counts": {"NONE": 446, "PURE_STRONG": 420, "WEAK_SUB": 261}, "exclusions": 11}, "GSR-LDNFIX-001|GBPUSD": {"total_rows": 1157, "continuity_pass_rows": 1157, "grade_counts": {"NONE": 439, "PURE_STRONG": 462, "WEAK_SUB": 256}, "exclusions": 12}, "GSR-NYCUT-001|USDJPY": {"total_rows": 1028, "continuity_pass_rows": 1027, "grade_counts": {"NONE": 417, "PURE_STRONG": 399, "WEAK_SUB": 212}, "exclusions": 16}, "GSR-NYCUT-001|EURUSD": {"total_rows": 1048, "continuity_pass_rows": 1048, "grade_counts": {"NONE": 445, "PURE_STRONG": 392, "WEAK_SUB": 211}, "exclusions": 12}}`
- **DST変換確認**: `{"GSR-TKYFIX-003|USDJPY": ["JST(UTC+9)"], "GSR-LDNFIX-001|EURUSD": ["BST(UTC+1)", "GMT(UTC+0)"], "GSR-LDNFIX-001|GBPUSD": ["BST(UTC+1)", "GMT(UTC+0)"], "GSR-NYCUT-001|USDJPY": ["EDT(UTC-4)", "EST(UTC-5)"], "GSR-NYCUT-001|EURUSD": ["EDT(UTC-4)", "EST(UTC-5)"]}`

## 4. 行単位除外監査ログ
- **ファイル**: `exclusions_log_gsr_2026w49.csv` (SHA256: `951cd609d678ff05dc4a1b62daf398f0bd89966e80e8bcd29a130d835a149757`, 66 行)
