# HANDOVER_GSR_2026W49_STAGE1 — 第1工程→第2工程 引き継ぎ書（v1.2準拠）

- **案件ID**: `GSR-2026W49`
- **作成日時**: `2026-11-23 JST`（クラウド先行ステージング版 / ローカル全量実行で自動上書き更新対象）
- **準拠規定**: `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md`（SHA256: `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9`）、`GSR-2026W48_decision.md`（SHA256: `550824ec4adca228ccf641ea5cd5c9e260085ad3cff1ab6ec86d2a6e8c5be640`）
- **生成スクリプト**: `profile_market_structure_gsr_2026w49_v1_0.py`（SHA256: `725c54a0977083ba09d3c052ec3eece9cf79d040c6f962a763346d9fbef8f288`）

---

## 1. 絶対防壁および運用ステータス
1. **Proxy定数・ビン逆算の完全排除**: 全特徴量（`wick_rejection_ratio`, `pre_15m_body_pips`, `pre_15m_range_pips`, `atr14_pips`, `move15m_atr`, `eta_range`, `theta_peak`, `psi_reject`, `phi_urp`）は生M1 OHLC（`available_at <= t`）のみから直接計算。クラウドAPIの容量制限により未取得の258MB全量データについては推測値で埋めず、すべて `unknown` として記録。
2. **Label-Free 厳守**: 両トラックのCSVともに `win_loss_label = HOLD_LABEL_FREE`, `net_pips_result = HOLD_LABEL_FREE` に固定。勝敗・未来価格リターン計算は一切含まない。
3. **トラック分離**:
   - **Track A（One-Shot OOS）**: `GSR-TKYFIX-002`（USDJPY, `2022-01-01+`）のみOOS解放。
   - **Track B（IS探索専用）**: `GSR-TKYFIX-003`, `GSR-LDNFIX-001`, `GSR-NYCUT-001` は `2015-01-01 〜 2021-12-31` 限定（`oos_locked: true`）。

---

## 2. 生M1データ台帳・SHA256照合表
| 通貨ペア | 生M1ファイル名 | サイズ (Bytes) | 期待SHA256 | 全量行数 |
| :--- | :--- | ---: | :--- | :--- |
| **USDJPY** | [`2026.10.16USDJPY(3)-M1-No Session.csv`](https://drive.google.com/file/d/1CjCXrVsAs-x9cC1e7UL16HNEfYHb-nNO/view?usp=drivesdk) | 258,871,846 | `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29` | `unknown` |
| **EURUSD** | [`2026.10.16EURUSD(5)-M1-No Session.csv`](https://drive.google.com/file/d/1ptHcllOr9M4_EsXswLmQ2KQh19RevpfV/view?usp=drivesdk) | 258,932,307 | `029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d` | `unknown` |
| **GBPUSD** | [`2026.10.16GBPUSD(3)-M1-No Session.csv`](https://drive.google.com/file/d/1tE67R8CLc7rpmEDO6HhxxI_xaL_56hM0/view?usp=drivesdk) | 258,199,124 | `unknown` | `unknown` |

---

## 3. Track A（`GSR-TKYFIX-002` One-Shot OOS）契約仕様＆部分実測検証
- **出力CSV**: `oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv`（全量行数・SHA256: `unknown` ※ローカル実行で確定）
- **固定契約**: `00:54:00 UTC`（`09:54 JST`）判定 → `00:55:00 UTC` Entry → `01:00:00 UTC` Expiry、プール条件 `move15m_atr >= 1.5`、主契約 `wick_rejection_ratio >= 0.25`（`PURE_STRONG`、両方向）。
- **クラウド実測テスト（2022年1月先頭998,755 bytes / 16,608行）**: プール抽出 **7行**（`PURE_STRONG` 6行 / `WEAK_SUB(EXCLUDED_TRAP06)` 1行 / 6本連続性 `PASS_6BAR_COMPLETE` 7/7）。

---

## 4. Track B（マルチ・フィキシングIS専用）設計＆DST検証結果
- **出力CSV**: `is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv`（全量行数・SHA256: `unknown` ※ローカル実行で確定）
- **対象候補**:
  - `GSR-TKYFIX-003`（USDJPY, `Asia/Tokyo`, `09:54` 判定 / `09:55` Entry）
  - `GSR-LDNFIX-001`（EURUSD / GBPUSD, `Europe/London`, `15:59` 判定 / `16:00` Entry）
  - `GSR-NYCUT-001`（USDJPY / EURUSD, `America/New_York`, `09:59` 判定 / `10:00` Entry）
- **DST境界単体検証**: 欧米非重複週（例: `2019-03-11`, `2019-10-28`）を含め `Europe/London`（`GMT+0` / `BST+1`）および `America/New_York`（`EST-5` / `EDT-4`）が `ZoneInfo` により正確にUTC変換されることを確認済み。

---

## 5. ローカルPC PowerShell 実行コマンド（全量生成用）
```powershell
python "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検\profile_market_structure_gsr_2026w49_v1_0.py"
```
上記コマンドを実行すると、両トラックの完全実測CSVおよび `stage1_to_stage2_handover_manifest_gsr_2026w49.json` が全量SHA256・実測行数付きで出力されます。
