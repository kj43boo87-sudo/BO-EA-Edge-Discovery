🏷️ [TRACE: GSR-2026W46 | 棄却 | GSR-2026W46 執行監査・週次総括・最終5ゲート判定・非累積マージナルv1.1改修・Git資産整理（確定版）]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W46 / GSR-CLIMAX-001 / GSR-PULLBACK-001 / GSR-FAKEOUT-001 / GSR-SURVEY-001 / GSR-202611-W2-WED-SPARK、比較参照元: BO-EUR-004 / BO-EUR-005、GEMINI_DISCOVERY_TRACE_RULE.md、プログラム資産管理手順.txt
record_id: unknown
session_title: GSR-2026W46 執行監査・週次総括・最終5ゲート判定・非累積マージナルv1.1改修・Git資産整理（確定版）
case_id: GSR-2026W46
parent_case_id: root
decision: 棄却
target_market: EURUSD_M1_M5
attachment_file: GSR-2026W46_Spark_Audit_and_Executive_Summary_2026-11-09.md, GSR-2026W46_decision.md, is_non_cumulative_marginal_3d_eurusd.csv, sync_gsr_2026w46_assets_and_git_commit.ps1, INDEX.md
part_info: 1/1
timestamp: 2026-11-09 15:25:17 JST
-->
所属プロジェクト: BO・EA Edge Discovery / Gemini側必勝調査報告 (edge-discovery)
TRACE区分: BOEA
専用案件コード: `GSR-2026W46`（個別候補: `GSR-CLIMAX-001`, `GSR-PULLBACK-001`, `GSR-FAKEOUT-001`, `GSR-SURVEY-001`）
参照元: `GSR-202611-W2-WED-SPARK.md`、`HANDOVER_Stage1_to_Stage2_EURUSD_GSR-2026W46.md`、`spark_audit_handover_manifest_eurusd.json`、`GEMINI_DISCOVERY_TRACE_RULE.md`、`プログラム資産管理手順.txt`

# GSR-2026W46 執行監査・週次総括・Git資産整理 統合報告書（2026-11-09 確定版）

## 1. 週次総括結論とSpark独立監査（`GSR-202611-W2-WED-SPARK`）の完全受入

1. **EURUSD 新規3候補（`GSR-CLIMAX-001` / `GSR-PULLBACK-001` / `GSR-FAKEOUT-001`）の正式棄却と他4通貨への展開中止**:
   - In-Sample期間（2015–2021年、Dukascopy EURUSD M1生データ 2,610,900行、有効機会 6,732件）において、3候補すべてが単独IS勝率 `44.88%〜50.14%`（損益分岐 `54.054%` 割れ、$\text{CLB}_{97.5\%} < 0$）となり、192セルPlateau格子でも $\text{CLB}_{97.5\%} > 0$ を達成したセルは **`0 / 192`（皆無）**でした。
   - さらにSpark独立監査の非累積3Dマージナル分解により、`GSR-FAKEOUT-001` の局所黒字セルは単一コーナー（`2.0 <= atr < 2.5, bbw <= 15.0, |slope3| <= 1.0`, $n=67$, 勝率 `65.67%`）の勝ち星を累積不等号（`<=` / `>=`）で周辺へ重複計上した**擬似プラトー（Pseudo-Plateau）**であり、周辺の純増分スライスはすべて勝率 `25.00%〜50.00%` の赤字であることが実証されました。
   - 第1工程→第2工程引き継ぎ書の方針（「EURUSDで $\text{CLB}_{97.5\%} > 0$ かつ $+0.2\text{ pip}$ 耐性が確認できた手法のみ他通貨へ展開」）に従い、3候補は**EURUSD ISゲートにて正式棄却・開発終了**とし、他4通貨（USDJPY, GBPJPY, AUDJPY, GBPUSD）への検証展開および2022–2026年OOS期間（1,781,411行）の開封を完全阻止します。
2. **既存EURUSD逆張りEA 8本（`GSR-SURVEY-001`）の「6分満期バグ（`barsPassed > 5`）」摘発と執行仕様の刷新**:
   - 既存EAレポート8本（計206取引）で表面勝率 `60.00%〜72.73%` に見えていた原因は、`barsPassed > 5` 条件による6分満期（205件）・7分満期（1件）の決済ズレであり、Dukascopy M1生データの真の5分満期（`Open[t+6]`, `+0.1 pip` ストレス）で再計算すると8本すべてが勝率 `25.00%〜51.72%`（連続有効195件合算で勝率 **`40.51%`**, $\text{EV} = -0.2505$）へ崩壊することが確定しました。
   - 今後の新規EA・検証コードでは、`barsPassed > InpExpiryMinutes` およびM1欠損時の `iBarShift` 遅延を禁止し、`TimeCurrent() >= entryTime + InpExpiryMinutes * 60`（連続バー確認付き厳密300秒満期 `Open[t+6]`）を必須執行ゲートとします。
3. **第2工程検証スクリプト（v1.1.0）からの非累積3Dマージナル表の実生成・保管完了**:
   - Sparkが改修した `gsr_eurusd_is_plateau_verifier_v1_0.py`（v1.1.0, SHA256: `cbb38b9e...`）を `is_outcomes_eurusd.csv`（SHA256: `121f7b5c...`）に対して実行し、非累積3Dビン集計表 `is_non_cumulative_marginal_3d_eurusd.csv`（192行、SHA256: `2705bea4842ab7fb9f3713d11eba873d07e143154b115e349286c0af16ca03aa`）および `PSEUDO_PLATEAU_WARNING` 判定付き `is_plateau_grid_eurusd_v1_1.csv`（192行、SHA256: `263ab56dc9ea57cbc53095bdffa0325a5d4ccf5c9389d8d60e17e715a73cb195`）を生成して第2工程出力フォルダ（`output_eurusd_is_plateau_20261109_060458`）および第3工程フォルダへ格納しました。
<!-- RESEARCH_TRACE_END -->
