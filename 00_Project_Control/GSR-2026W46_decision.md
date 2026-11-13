# GSR-2026W46 Decision Record — EURUSD 新規3候補（GSR-CLIMAX-001 / GSR-PULLBACK-001 / GSR-FAKEOUT-001）＆ 既存逆張りEA 8本監査（GSR-SURVEY-001）

- **Pipeline Case ID**: `GSR-2026W46`（親ライン: `Gemini側必勝調査報告`）
- **Evaluated Candidate IDs**: `GSR-CLIMAX-001`, `GSR-PULLBACK-001`, `GSR-FAKEOUT-001`, `GSR-SURVEY-001`
- **Prior Rejected Reference (`source_trace_refs`)**: `BO-EUR-004`, `BO-EUR-005`（再検証防止参照）
- **Decision Date**: `2026-11-09 JST`
- **Final Status**: **棄却・凍結（REJECTED / CLOSED AT IN-SAMPLE GATE — 他4通貨への展開中止）**
- **Evaluated Scope**: EURUSD In-Sample (`2015-01-01 22:00:00` .. `2021-12-31 21:59:00 UTC`, 2,610,900 M1 bars / 6,733 candidate signals / 6,732 valid 6-bar opportunities)
- **Holdout Protection**: Out-of-Sample (`2022-01-01 00:00:00` onward, 1,781,411 M1 rows) **Unopened / Strictly Blocked (`post_2021_oos_rows_blocked: 1,781,411`)**

## 0. 公式TRACE記録ブロック

```text
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
attachment_file: GSR-2026W46_decision.md, GSR-2026W46_Spark_Audit_and_Executive_Summary_2026-11-09.md, is_non_cumulative_marginal_3d_eurusd.csv, sync_gsr_2026w46_assets_and_git_commit.ps1, INDEX.md
part_info: 1/1
timestamp: 2026-11-09 15:25:17 JST
-->
所属プロジェクト: BO・EA Edge Discovery / Gemini側必勝調査報告 (edge-discovery)
TRACE区分: BOEA
専用案件コード: GSR-2026W46（候補コード: GSR-CLIMAX-001, GSR-PULLBACK-001, GSR-FAKEOUT-001, GSR-SURVEY-001）
参照元: GSR-202611-W2-WED-SPARK.md、spark_audit_handover_manifest_eurusd.json、is_2015_2021_opportunity_ledger_eurusd.csv

【最終決定要旨】
- 判定: 棄却・凍結（EURUSD ISゲートにて全3候補 GSR-CLIMAX-001 / GSR-PULLBACK-001 / GSR-FAKEOUT-001 および既存EA GSR-SURVEY-001 の不採用確定・他4通貨への展開中止）
- 最終5ゲート結果: ①台帳一致[PASS] / ②IS HAC下限>54.054%[FAIL] / ③近傍Plateau（非累積マージナル分解）[FAIL] / ④Spark監査[PASS（構造解明・6分満期バグ摘発）] / ⑤MT4 t+1約定・スプレッド耐性[FAIL]
- OOS保護状態: 2022〜2026年OOS期間（1,781,411行）完全未開封ロック維持
<!-- RESEARCH_TRACE_END -->
```

## 1. 工程別・独立監査 合意サマリ

| 工程 / 担当 | 対象コード | 判定 | 根拠要約 |
| :--- | :--- | :--- | :--- |
| **第1工程：市場調査＆データ点検**<br>（Gemini） | `GSR-2026W46`<br>`GSR-SURVEY-001` | **完了** | Dukascopy M1生データ（`029bc12c...`、4,424,366行）から2022年以降OOS（1,781,411行）を完全遮断し、EURUSD IS機会台帳（`a45156cf...`、6,733行）をLabel-Freeで抽出。既存EURUSD逆張りEA 8本（206取引）で100%の `Settle != 5m`（`barsPassed > 5` による6分満期バグ）を検出。 |
| **第2工程：機会台帳突合＆IS統計・Plateau検証**<br>（Gemini） | `GSR-CLIMAX-001`<br>`GSR-PULLBACK-001`<br>`GSR-FAKEOUT-001` | **棄却** | ペイアウト1.85倍（損益分岐 `54.054%`）・`+0.1 pip` ストレス・同値LOSE下で3候補すべてが単独IS勝率 `44.88%〜50.14%`（`FAIL_NOT_ABOVE_ZERO`）。192セルPlateau格子でも $\text{CLB}_{97.5\%} > 0$ は **`0 / 192`（0.0%）**。 |
| **第2工程：独立性能・過剰適合監査**<br>（Spark：`GSR-202611-W2-WED-SPARK`） | 全候補・既存EA | **棄却（FAIL）** | 全指標・母数フローの完全一致を確認。`GSR-FAKEOUT-001` の局所黒字セルは単一コーナー（`2.0<=atr<2.5, bbw<=15, |slope3|<=1.0`, $n=67$, 44勝23敗）を累積不等号（`<=` / `>=`）で使い回した**擬似プラトー（Pseudo-Plateau）**であり、周辺純増分はすべて勝率 `25.00%〜50.00%` の赤字であることを実証。検証スクリプトを非累積3Dマージナル対応版（v1.1.0）へ改修。 |
| **第3工程：執行監査・週次総括**<br>（Gemini） | `GSR-2026W46` | **開発終了承認** | 最終5ゲート審査（1/5通過・4/5不通過）を確定。引き継ぎ方針に従い他4通貨（USDJPY, GBPJPY, AUDJPY, GBPUSD）への展開を中止し、2022–2026年OOS未開封のまま全3候補を正式棄却・凍結。 |

## 2. 最終5ゲート確認結果（Executive Gate Checklist）

1. **ゲート①：機会台帳（Opportunity Ledger）の一致・6分間連続性 — `[PASS]`**
   - `is_2015_2021_opportunity_ledger_eurusd.csv`（SHA256: `a45156cfc29cec249a538d3b81b85b74e02817c0cf0ae67ac783b6d57c72c327`、6,733行）とDukascopy EURUSD M1生データ（SHA256: `029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d`、IS採用 2,610,900行 / OOS遮断 1,781,411行）の100%一致を確認。
   - 母数フロー：`GSR-CLIMAX-001`（Raw 734 → 有効 734、除外 0）、`GSR-PULLBACK-001`（Raw 4,598 → 有効 4,597、除外 1：`GAP_T2_T5`）、`GSR-FAKEOUT-001`（Raw 1,401 → 有効 1,401、除外 0）。必要M1タイムスタンプ `40,183` 点中 `40,182` 点存在（欠損1点は `GAP_T2_T5` 除外1件と完全一致）。
2. **ゲート②：IS期間（2015–2021）のHAC信頼下限 > 損益分岐54.054%（$\text{EV} > 0$） — `[FAIL（棄却決定因）]`**
   - **`GSR-CLIMAX-001`（`Proposal_B_BBClimaxReversal`）**: $n=734$（368勝366敗、0pt同値6件、1pt転落14件）、勝率 `50.14%`（BE比 `-3.92%pt`）、$\text{EV} = -0.072480$、$\text{SE}_{\text{HAC}} = 0.033197$、$\text{CLB}_{97.5\%} = -0.137653$（$t = -2.1833$, `FAIL_NOT_ABOVE_ZERO`）
   - **`GSR-PULLBACK-001`（`Proposal_C_M5TrendPullback`）**: $n=4,597$（2,063勝2,534敗、0pt同値65件、1pt転落50件）、勝率 `44.88%`（BE比 `-9.18%pt`）、$\text{EV} = -0.169774$、$\text{SE}_{\text{HAC}} = 0.013575$、$\text{CLB}_{97.5\%} = -0.196387$（$t = -12.5063$, `FAIL_NOT_ABOVE_ZERO`）
   - **`GSR-FAKEOUT-001`（`Proposal_A_FakeoutReentry`）**: $n=1,401$（684勝717敗、0pt同値20件、1pt転落12件）、勝率 `48.82%`（BE比 `-5.23%pt`）、$\text{EV} = -0.096788$、$\text{SE}_{\text{HAC}} = 0.025094$、$\text{CLB}_{97.5\%} = -0.146013$（$t = -3.8571$, `FAIL_NOT_ABOVE_ZERO`）
3. **ゲート③：近傍パラメーターPlateauの広さ（192セル＋非累積3Dマージナル分解） — `[FAIL（擬似プラトー・孤立スパイク）]`**
   - 192セル全体で $\text{CLB}_{97.5\%} > 0$ を満たすセルは **`0 / 192`（0.0%）**。
   - `GSR-FAKEOUT-001` で見かけ上損益分岐を超えた9セル（うち旧v1.0分類で `CANDIDATE_PLATEAU_CLB_UNPROVEN` 2セル、`MODERATE_REGION` 2セル）を非累積3Dマージナル（`is_non_cumulative_marginal_3d_eurusd.csv`, SHA256: `2705bea4842ab7fb9f3713d11eba873d07e143154b115e349286c0af16ca03aa`）で分解すると、黒字は単一コーナー `2.0 <= atr < 2.5, bbw <= 15.0, |slope3| <= 1.0`（$n=67$, 44勝23敗, 勝率 `65.67%`, $\text{EV}=+0.2149$）および小標本 `atr >= 2.5`（$n=42$, 勝率 `57.14%`）のみであり、隣接する周辺純増分スライス（`1.6 <= atr < 2.0`: 勝率 `47.37%`、`1.2 <= atr < 1.6`: `44.21%`、`15 < bbw <= 20`: `48.21%`、`20 < bbw <= 28`: `44.44%`、`1.0 < |slope3| <= 1.8`: `45.21%`、`1.8 < |slope3| <= 2.8`: `25.00%`）はすべて損益分岐割れの赤字（`PSEUDO_PLATEAU_WARNING`）であった。
   - `GSR-CLIMAX-001` 唯一のBE超えセル（`atr >= 1.2, bbw <= 10.0, |slope3| <= 0.6`, $n=110$, 勝率 `58.18%`, $\text{CLB}_{97.5\%} = -0.0922$）も、`1.2 <= atr < 1.5` の小標本（$n=40$, 29勝11敗）にのみ依存し、`atr >= 1.5`（$n=70$, 勝率 `50.00%`）や隣接 `0.6 < |slope3| <= 1.0`（$n=53$, 勝率 `43.40%`）、`10.0 < bbw <= 12.5`（$n=47$, 勝率 `40.43%`）で即座に崩壊する孤立スパイク（`ISOLATED_SPIKE_WARNING`）と確定。
4. **ゲート④：Spark監査での未来参照・選択バイアス有無＆既存EA 6分バグ監査 — `[PASS（未来参照なし／既存EAの6分満期バグを完全解明）]`**
   - 新規3候補の機会台帳・特徴量計算（`M5_CloseTime <= M1_CloseTime`）に未来参照は一切なし。
   - `GSR-SURVEY-001`（既存EURUSD逆張りEA 8本・全206取引）において、MQL4の `barsPassed > 5` 条件により全取引が6分満期（205件）または7分満期（1件）で決済されていた実装バグを特定。Dukascopy M1生データの真の5分満期（`Open[t+6]`, `+0.1 pip` ストレス）で再計算した結果、8本すべて（8 / 8）が勝率 `25.00%〜51.72%`（連続有効195件合算で79勝116敗、勝率 **`40.51%`**, $\text{EV} = -0.2505$）へ転落し、見かけ上の高勝率（旧 `60.00%〜72.73%`）が満期ズレの産物であったことを解明。
5. **ゲート⑤：MT4での $t+1$ 分Open約定・スプレッド耐性（`+0.1`〜`+0.3 pip`） — `[FAIL]`**
   - `+0.1 pip` 時点で全3候補が負期待値であるうえ、`+0.2 pip` → `+0.3 pip` 負荷でさらに悪化（`GSR-CLIMAX-001`: 勝率 `50.14%` → `48.23%` → `46.87%`、`GSR-PULLBACK-001`: `44.88%` → `43.48%` → `42.55%`、`GSR-FAKEOUT-001`: `48.82%` → `47.39%` → `46.32%`）。
   - 今後の新規EA・検証コードでは `barsPassed > InpExpiryMinutes`（6分満期バグ）およびM1欠損時の `iBarShift` 遅延を防ぐため、`TimeCurrent() >= entryTime + InpExpiryMinutes * 60`（連続バー確認付き厳密300秒満期 `Open[t+6]`）を標準執行仕様として固定する。

## 3. 主要検証スクリプト・入出力証跡のSHA256一覧

| 区分 | ファイル名 | 規模 | SHA256（実測値） | 確認状態区分 |
| :--- | :--- | :--- | :--- | :--- |
| 第1工程スクリプト | `profile_is_market_structure_2015_2021_v1_4.py` | 43,857 B | `809ec0ec9c5623dd369814c238ec2b344f2ab9f83ae9e11d1df718e495ad732a` | **実行確認済み**（v1.4.0 Dukascopy M1対応） |
| 第1工程台帳（EURUSD） | `is_2015_2021_opportunity_ledger_eurusd.csv` | 6,733 rows | `a45156cfc29cec249a538d3b81b85b74e02817c0cf0ae67ac783b6d57c72c327` | **実行確認済み**（Label-Free完全一致） |
| 第1工程既存EA監査 | `existing_reports_continuity_audit_auto.csv` | 18,836 B | `f4dbb3b6d58f61fd4dcfc5aa1cc1cd205b3abe3ca557211eff506184ac58cdc3` | **実行確認済み**（60レポート連続性点検） |
| 第2工程スクリプト（改修正本） | `gsr_eurusd_is_plateau_verifier_v1_0.py` (v1.1.0) | 48,204 B | `cbb38b9e9776d8215899c460d20d12ce02eca74b9e9c227a97559419d64dee21` | **実行確認済み**（非累積3Dマージナル＆`PSEUDO_PLATEAU_WARNING`対応） |
| 第2工程スクリプト（別名保存） | `gsr_eurusd_is_plateau_verifier_v1_1.py` (v1.1.0) | 44,408 B | `98a75ba95ff26e3b702bbbfa4b450f2eb195e6bec1588e41ef3a8429e5be02c9` | 静的確認済み（v1.1別名版） |
| 第2工程スクリプト（旧版保全） | `gsr_eurusd_is_plateau_verifier_v1_0_old_cumulative.py` | 42,846 B | `e10faa06c2f665c1cc732fab433b6d52daf9d598205c7d53a6c8707126a9a077` | 旧版保持（v1.0.0 累積格子版） |
| 第2工程マニフェスト | `spark_audit_handover_manifest_eurusd.json` | 25,969 B | `fab0d40108e65a08c8f4e8ef0c8fd82fecd5c8aa0b180a5bbc6f63d1f58b7019` | **実行確認済み** |
| 第2工程Standalone集計 | `is_standalone_summary_eurusd.csv` | 945 B | `23a7dcc17a5adc428ebad237564307ec1f67280e07c35ff1a37af48b955947e1` | **実行確認済み** |
| 第2工程非累積3Dビン表 | `is_non_cumulative_marginal_3d_eurusd.csv` | 29,516 B | `2705bea4842ab7fb9f3713d11eba873d07e143154b115e349286c0af16ca03aa` | **実行確認済み**（192非重複スライス） |
| 第2工程v1.1 Plateau表 | `is_plateau_grid_eurusd_v1_1.csv` | 42,572 B | `263ab56dc9ea57cbc53095bdffa0325a5d4ccf5c9389d8d60e17e715a73cb195` | **実行確認済み**（`PSEUDO_PLATEAU_WARNING` 判定付） |
| 第2工程既存EA再計算表 | `existing_eurusd_reports_m1_audit.csv` | 1,005 B | `d24d4b64f323141cc211f9bef8931a1e81ae463f7bf3795cf087c5a43f7d14c1` | **実行確認済み**（EURUSD 8本 真の5分満期再計算） |
