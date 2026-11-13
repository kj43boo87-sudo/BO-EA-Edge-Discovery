🏷️ [TRACE: GSR-2026W47 | 棄却・凍結 (GSR-EXHAUST-001, GSR-SHOCKDECAY-001) / 保留・追加検証 (GSR-TKYFIX-001 -> GSR-TKYFIX-002) | GSR-2026W47 最終5ゲート判定・週次総括・Git資産整理およびGSR-TKYFIX-002差配登録]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W47; GSR-202611-W3-WED; GSR-202611-W3-WED-SPARK; GSR-EXHAUST-001; GSR-SHOCKDECAY-001; GSR-TKYFIX-001; GSR-TKYFIX-002; stage1_to_stage2_handover_manifest_gsr_2026w47.json; is_2015_2021_opportunity_ledger_gsr_2026w47.csv; spark_audit_handover_manifest_gsr_2026w47.json; QUANT_PYTHON_MASTER_CONTEXT.md (v2.2); GEMINI_DISCOVERY_TRACE_RULE.md; プログラム資産管理手順.txt
record_id: GSR-202611-W3-FRI
session_title: GSR-2026W47 最終5ゲート判定・週次総括・Git資産整理およびGSR-TKYFIX-002差配登録
case_id: GSR-2026W47
parent_case_id: root
decision: 保留
target_market: EURUSD_M1 / USDJPY_M1 (BO_STANDARD / 5-min expiry)
attachment_file: GSR-2026W47_Executive_Audit_and_Weekly_Summary_2026-11-13.md, GSR-2026W47_decision.md, sync_gsr_2026w47_assets_and_git_commit.ps1, INDEX.md
part_info: 1/1
timestamp: 2026-11-13 05:15:51 JST
-->
所属プロジェクト: BO・EA Edge Discovery / Gemini側必勝調査報告 (edge-discovery)
TRACE区分: BOEA
専用案件コード: `GSR-2026W47`（派生追加検証コード: `GSR-TKYFIX-002`）
参照元: `GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md`、`GSR-202611-W3-WED-SPARK`、`spark_audit_handover_manifest_gsr_2026w47.json`、`QUANT_PYTHON_MASTER_CONTEXT.md` (v2.2)、`プログラム資産管理手順.txt`

# GSR-2026W47 週次総括・執行監査・GSR-TKYFIX-002 差配指示書（2026-11-13 JST）

## 1. 総監督最終裁定に基づく案件処分と構造的知見の総括

1. **`GSR-EXHAUST-001`（M1 BB $\pm 2.5\sigma$ 到達後の切り下げ反転）— 棄却・永久凍結（`FAIL`）**:
   - EURUSD（$n=9,395$, 勝率 `49.88%`, $\text{CLB}_{97.5\%}=-0.0960$）・USDJPY（$n=10,263$, 勝率 `49.29%`, $\text{CLB}_{97.5\%}=-0.1060$）ともに損益分岐（`54.054%`）を大きく下回り、CONTROL群と比較して勝率が **`-2.40%pt` 劣化する逆アブレーション**が発生。
   - 5分順行値幅の中央値が `0.0〜0.1 pip` に過ぎず、`+0.2 pip` ストレスで勝率 `47.94%` / `46.78%` へ崩壊（`TRAP-05`：摩擦崩壊）したため、即時棄却・永久凍結とする。
2. **`GSR-SHOCKDECAY-001`（M1大陽線・大陰線 $\ge 2.2\text{ ATR}$ 直後の値幅収縮逆張り）— 棄却・永久凍結（`FAIL`）**:
   - EURUSD（$n=11,749$, 勝率 `51.03%`, $\text{CLB}_{97.5\%}=-0.0727$）・USDJPY（$n=11,964$, 勝率 `51.14%`, $\text{CLB}_{97.5\%}=-0.0704$）ともに損益分岐未達かつ逆アブレーション（`-0.32%pt` / `-0.45%pt`）。
   - 値幅中央値 `0.1 pip` により `+0.2 pip` ストレスで勝率 `47.32%` / `47.61%` へ崩壊（`TRAP-05`）したため、即時棄却・永久凍結とする。
3. **`GSR-TKYFIX-001`（USDJPY 東京仲値 09:55 JST 直前15分偏り＋09:54ヒゲ拒絶5分逆張り）— 保留・IS内追加検証 `GSR-TKYFIX-002` へ差配（`HOLD`）**:
   - これまで検証したすべてのM1汎用テクニカル候補が順行値幅中央値 `0.0〜0.1 pip` で摩擦崩壊したのに対し、東京仲値（09:55 JST）の制度的フロー終了タイミングを狙う `GSR-TKYFIX-001`（`CANDIDATE` $n=561$）は**順行値幅中央値 `+0.50 pip`** を確保し、`+0.1 pip` 勝率 **`57.40%`**（CONTROL比 `+3.02%pt` の正のアブレーション）、`+0.2 pip` 勝率 **`55.62%`**、`+0.3 pip` 勝率 **`55.26%`** と全摩擦水準で黒字を維持した。
   - 通年 $\text{CLB}_{97.5\%} = -0.0190$ にとどまった原因は、①OR条件による弱いヒゲ拒絶層 `B1_sub0.25`（$n=207$, 勝率 `50.72%`, $\text{EV}=-0.0616$）の混入（`TRAP-06`）と、②日次イベントへの64分割グリッド適用による過分割（`TRAP-07`）にあることが1D非累積マージナル分解（`is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv`）から裏付けられた。
   - よって、OOS（2022年以降）未開封ロックを完全維持したまま、IS期間（2015–2021年）内で **実験A（OR条件排除・純粋ヒゲ拒絶単体検証）・実験B（15分変動幅下限による低ボラ減衰分離）・実験C（64分割廃止・方向／曜日／ボラによる非重複粗視化スライス検証）** を行う **`GSR-TKYFIX-002`** へ正式移行する。
<!-- RESEARCH_TRACE_END -->
