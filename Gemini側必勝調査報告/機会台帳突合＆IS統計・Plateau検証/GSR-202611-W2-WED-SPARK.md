🏷️ [TRACE: GSR-2026W46 | 棄却 | GSR-2026W46 第2工程（EURUSD IS期間2015-2021・3候補統計＆192セルPlateau検証・既存EA監査・非累積マージナル改修v1.1）に対するSpark独立性能・過剰適合監査（確定版）]
<!-- RESEARCH_TRACE_START
ai_id: spark
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W46; GSR-202611-W2-WED-SPARK; GSR-CLIMAX-001; GSR-PULLBACK-001; GSR-FAKEOUT-001; GSR-SURVEY-001; is_2015_2021_opportunity_ledger_eurusd.csv; gsr_eurusd_is_plateau_verifier_v1_0.py (v1.1.0); BO-EUR-005 (comparison reference only)
record_id: GSR-202611-W2-WED-SPARK
session_title: GSR-2026W46 第2工程（EURUSD IS期間2015-2021・3候補統計＆192セルPlateau検証・既存EA監査・非累積マージナル改修v1.1）に対するSpark独立性能・過剰適合監査（確定版）
case_id: GSR-2026W46
parent_case_id: root
decision: 棄却
audit_verdict: FAIL
target_market: EURUSD (BO_STANDARD / M1 5-min expiry)
attachment_file: GSR-202611-W2-WED-SPARK.md
part_info: 1/1
timestamp: 2026-11-09 15:45:00 JST
-->

## 1. 監査結論と主要根拠
- audit_verdict: FAIL（GSR-2026W46 EURUSD 3候補 GSR-CLIMAX-001 / GSR-PULLBACK-001 / GSR-FAKEOUT-001、既存EA調査 GSR-SURVEY-001、および比較参照元 BO-EUR-005 の全候補において統計的棄却確定。2022〜2026年OOS期間の開封阻止および他4通貨への展開中止）
- decision: 棄却（全3候補ともISゲートにて不採用・凍結確定）
- 主要根拠:
  1. Standalone IS成績の全面的敗北: GSR-CLIMAX-001（n=734, 勝率 50.14%, EV=-0.0725, CLB97.5%=-0.1377）、GSR-PULLBACK-001（n=4,597, 勝率 44.88%, EV=-0.1698, CLB97.5%=-0.1964）、GSR-FAKEOUT-001（n=1,401, 勝率 48.82%, EV=-0.0968, CLB97.5%=-0.1460）のすべてが損益分岐点（54.054%）未満。
  2. 192格子Plateau分析において CLB97.5% > 0 を満たすセルは 0 / 192（皆無）。GSR-FAKEOUT-001 の上位セルも単一コーナー（2.0 <= atr < 2.5, bbw <= 15.0, |slope3| <= 1.0, n=67, 44勝23敗）の勝ち星を累積不等号で周辺へ重複計上した擬似プラトー（PSEUDO_PLATEAU_WARNING）であり、周辺純増分はすべて赤字（勝率 25.00%〜50.00%）。
  3. 既存EURUSD逆張りEA 8本（GSR-SURVEY-001）も6分満期バグ（barsPassed > 5）を修正して真の5分満期（Open[t+6]）で再計算すると、全8本が損益分岐割れ（勝率 25.00%〜51.72%、連続有効195件合算で勝率 40.51%, EV=-0.2505）へ崩壊。

<!-- RESEARCH_TRACE_END -->