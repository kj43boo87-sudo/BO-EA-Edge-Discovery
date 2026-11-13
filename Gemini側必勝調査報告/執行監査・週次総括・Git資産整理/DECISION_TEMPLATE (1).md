# {GSR_CASE_ID} Decision Record — {MODEL_TITLE}

- **Pipeline Case ID**: `{GSR_WEEKLY_ID}`（例: `GSR-2026W46` / 親ライン: `Gemini側必勝調査報告`）
- **Candidate Case ID(s)**: `{GSR_CANDIDATE_ID}`（例: `GSR-CLIMAX-001`, `GSR-PULLBACK-001`, `GSR-FAKEOUT-001`, `GSR-SURVEY-001`）
- **Prior Rejected Reference (`source_trace_refs`)**: `{PRIOR_REJECTED_IDS}`（過去棄却案件は比較参照元としてのみ記載し、`case_id` には流用しない）
- **Decision Date**: `{YYYY-MM-DD JST}`
- **Final Status**: **{採用候補 (ADOPT_CANDIDATE) / 棄却・凍結 (REJECTED_FROZEN) / 保留 (HOLD) / 追加検証 (FURTHER_VERIFICATION)}**
- **Evaluated Scope**: In-Sample (`2015-01-01` .. `2021-12-31`, `{IS_M1_ROWS}` M1 bars / `{VALID_N}` valid 6-bar opportunities)
- **Holdout Protection**: Out-of-Sample (`2022-01-01` .. `2026-12-31`, `{OOS_ROWS}` rows) **{Unopened / Strictly Blocked}**

## 0. 公式TRACE記録ブロック（専用コード `GSR-*` 準拠）

```text
🏷️ [TRACE: {GSR_CASE_ID} | {採用 / 棄却 / 保留 / 追加検証} | {SESSION_TITLE}]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: {GSR_WEEKLY_ID} / {GSR_CANDIDATE_ID}、比較参照元: {PRIOR_REJECTED_IDS}、GEMINI_DISCOVERY_TRACE_RULE.md、プログラム資産管理手順.txt
record_id: unknown
session_title: {SESSION_TITLE}
case_id: {GSR_CASE_ID}
parent_case_id: {GSR_PARENT_ID}
decision: {採用 / 棄却 / 保留 / 追加検証}
target_market: {PAIR_TIMEFRAME}
attachment_file: {GSR_CASE_ID}_decision.md
part_info: 1/1
timestamp: {YYYY-MM-DD HH:MM:SS JST}
-->
所属プロジェクト: BO・EA Edge Discovery / Gemini側必勝調査報告 (edge-discovery)
TRACE区分: BOEA
専用案件コード: {GSR_CASE_ID}
参照元: {LEDGER_FILE}, {MANIFEST_FILE}, {SPARK_AUDIT_FILE}

【最終決定要旨】
- 判定: {採用候補 / 棄却・凍結 / 保留 / 追加検証}
- 最終5ゲート結果: ①台帳一致[{PASS/FAIL/HOLD}] / ②IS HAC下限>54.054%[{PASS/FAIL/HOLD}] / ③近傍Plateau（非累積3Dマージナル）[{PASS/FAIL/HOLD}] / ④Spark監査[{PASS/FAIL/HOLD}] / ⑤MT4 t+1約定・スプレッド耐性[{PASS/FAIL/HOLD}]
- 2022年以降（OOS）保護状態: {未開封ロック維持 / 展開中止}
<!-- RESEARCH_TRACE_END -->
```

## 1. 最終5ゲート確認結果（Executive Gate Checklist）

1. **ゲート①：機会台帳（Opportunity Ledger）の一致・6分間連続性 — `[{PASS / FAIL / HOLD}]`**
   - 第1工程Label-Free機会台帳（SHA256: `{LEDGER_SHA256}`）と参照M1生データ（SHA256: `{M1_SHA256}`、2022年以降OOS完全遮断）のハッシュ・行数一致を確認。
   - 判断足 $t$ から満期足 $t+6$（`Open[t+1]` エントリー、`Open[t+6]` 300秒満期判定）の1分刻み6本連続性と欠損隔離（`GAP_T2_T5` 等）の完全一致を確認。
2. **ゲート②：IS期間（2015–2021）のHAC信頼下限 > 損益分岐54.054%（$\text{EV} > 0$） — `[{PASS / FAIL / HOLD}]`**
   - ペイアウト `1.85倍`（損益分岐勝率 `54.054%`）、同値 `LOSE`、`+0.1 pip` ストレス控除後における勝率、期待値 $\text{EV}$、Newey-West HAC標準誤差 $\text{SE}_{\text{HAC}}$、片側97.5%信頼下限 $\text{CLB}_{97.5\%} > 0$ の合否。
3. **ゲート③：近傍パラメーターPlateauの広さ（非累積3Dマージナル分解必須） — `[{PASS / FAIL / HOLD}]`**
   - パラメーター格子における $\text{CLB}_{97.5\%} > 0$ 達成セル数とL1近傍生残率。
   - **非累積3Dマージナル（Disjoint Slice `[low, high)`）監査**：累積不等号（`<=` / `>=`）によるコーナーセルの使い回し（`PSEUDO_PLATEAU_WARNING`）や小標本スパイク（`ISOLATED_SPIKE_WARNING`）を排除し、純増分スライス自体が損益分岐を超えているかを確認。
4. **ゲート④：Spark監査での未来参照・選択バイアス・既存EAバグ有無 — `[{PASS / FAIL / HOLD}]`**
   - 上位足確定条件（`M5_CloseTime <= M1_CloseTime`）、5分以内の重複連打排除、事後コホート選別バイアス有無、および年次・セッション・ATR帯別の頑健性。
5. **ゲート⑤：MT4での $t+1$ 分Open約定・スプレッド耐性（`+0.1`〜`+0.3 pip`）＆厳密5分満期仕様 — `[{PASS / FAIL / HOLD}]`**
   - `+0.1 pip` / `+0.2 pip` / `+0.3 pip` 負荷での勝率・EV推移。
   - MQL4実装における `barsPassed > InpExpiryMinutes`（6分満期バグ）の排除と、`TimeCurrent() >= entryTime + InpExpiryMinutes * 60`（連続バー確認付き厳密5分満期 `Open[t+6]`）の遵守。
