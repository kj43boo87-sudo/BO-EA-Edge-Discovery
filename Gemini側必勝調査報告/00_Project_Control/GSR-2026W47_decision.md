# GSR-2026W47 Decision Record — 第2工程監査裁定確定・最終5ゲート判定および GSR-TKYFIX-002（IS内追加検証）差配契約

- **Pipeline Case ID**: `GSR-2026W47`（親ライン: `Gemini側必勝調査報告`）
- **Evaluated Candidate IDs**:
  - `GSR-EXHAUST-001`（EURUSD / USDJPY M1）：**棄却・凍結（FAIL）**
  - `GSR-SHOCKDECAY-001`（EURUSD / USDJPY M1）：**棄却・凍結（FAIL）**
  - `GSR-TKYFIX-001`（USDJPY M1）：**保留・IS内追加検証（HOLD → `GSR-TKYFIX-002` へ継承）**
- **Upstream Audit Reference**: `GSR-202611-W3-WED`（Gemini第2工程報告） / `GSR-202611-W3-WED-SPARK`（Aegis / Spark独立性能監査）
- **Prior Rejected Archive (`source_trace_refs`)**: `GSR-2026W46` (`GSR-CLIMAX-001`, `GSR-PULLBACK-001`, `GSR-FAKEOUT-001`, `GSR-SURVEY-001`), `BO-EUR-004`, `BO-EUR-005`
- **Decision Date**: `2026-11-13 JST`（総監督裁定日: `2026-11-12 JST`）
- **Evaluated Scope**: In-Sample (`2015-01-01 00:00:00` .. `2021-12-31 23:59:59 UTC` — EURUSD M1 `2,610,900` rows / USDJPY M1 `2,608,784` rows / 台帳総数 `99,945` rows / 有効PASS `98,100` rows)
- **Holdout Protection**: Out-of-Sample (`2022-01-01 00:00:00` onward — EURUSD `1,781,411` rows / USDJPY `1,783,913` rows) **Unopened / Strictly Locked (`oos_locked: true`)**

---

## 0. 公式TRACE記録ブロック

```text
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
attachment_file: GSR-2026W47_decision.md, GSR-2026W47_Executive_Audit_and_Weekly_Summary_2026-11-13.md, sync_gsr_2026w47_assets_and_git_commit.ps1, INDEX.md
part_info: 1/1
timestamp: 2026-11-13 05:15:51 JST
-->
所属プロジェクト: BO・EA Edge Discovery / Gemini側必勝調査報告 (edge-discovery)
TRACE区分: BOEA
専用案件コード: GSR-2026W47（派生追加検証コード: GSR-TKYFIX-002）
参照元: GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md、GSR-202611-W3-WED-SPARK、spark_audit_handover_manifest_gsr_2026w47.json

【最終裁定要旨】
1. Gate 1（OOS遮断・台帳整合）: PASS（SHA256: 7f8581b6...7d38 完全一致、総数99,945件＝PASS 98,100件＋除外1,845件、oos_locked: true）
2. GSR-EXHAUST-001（EURUSD / USDJPY M1）: 棄却・凍結（FAIL）— 逆アブレーション（-2.40%pt）、CLB97.5% < 0（-0.0960 / -0.1060）、値幅中央値0.0〜0.1pipによる摩擦崩壊（TRAP-05）。再検証・延命厳禁。
3. GSR-SHOCKDECAY-001（EURUSD / USDJPY M1）: 棄却・凍結（FAIL）— 逆アブレーション（-0.32%pt / -0.45%pt）、CLB97.5% < 0（-0.0727 / -0.0704）、値幅中央値0.1pipによる摩擦崩壊（TRAP-05）。再検証・延命厳禁。
4. GSR-TKYFIX-001（USDJPY M1）: 保留・IS内追加検証（HOLD → GSR-TKYFIX-002 へ差配）— 値幅中央値0.50pip、+0.1p勝率57.40%（CONTROL比+3.02%pt）、+0.2p勝率55.62%、+0.3p勝率55.26%と全摩擦水準で黒字維持。OR条件による弱ヒゲ層混入（TRAP-06）および日次イベントの64分割過分割（TRAP-07）を除去するIS（2015–2021）内追加検証 GSR-TKYFIX-002 を実施（OOS 2022–2026 未開封ロック維持）。
<!-- RESEARCH_TRACE_END -->
```

---

## 1. 案件別 最終ステータス＆総監督最終裁定一覧

| 案件コード (`case_id`) | 対象市場・時間足 | 戦略・モデル概要 | Spark監査判定 | 総監督 最終裁定 | 次工程処置・ロック状態 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`GSR-EXHAUST-001`** | `EURUSD` / `USDJPY` M1 | M1 BB $\pm 2.5\sigma$ 到達後の高安未更新・実体反転（5分満期逆張り） | `FAIL` | **棄却・凍結 (`FAIL`)** | 即時開発凍結・再検証およびパラメータ調整による延命厳禁 |
| **`GSR-SHOCKDECAY-001`** | `EURUSD` / `USDJPY` M1 | M1大陽線・大陰線（$\ge 2.2\text{ ATR}$）直後の値幅収縮減衰（5分満期逆張り） | `FAIL` | **棄却・凍結 (`FAIL`)** | 即時開発凍結・再検証およびパラメータ調整による延命厳禁 |
| **`GSR-TKYFIX-001`** | `USDJPY` M1 | 東京仲値（09:55 JST）直前15分偏り＋09:54確定足ヒゲ拒絶（5分満期逆張り） | `HOLD` | **保留・IS内追加検証 (`HOLD`)** | OOS（2022年以降）未開封ロック維持のまま、IS内追加検証 **`GSR-TKYFIX-002`** へ差配 |

---

## 2. 最終5ゲート確認リスト（Executive 5-Gate Verification）

| ゲート項目 | 審査基準（`QUANT_PYTHON_MASTER_CONTEXT.md` v2.2） | `GSR-EXHAUST-001` (EURUSD / USDJPY) | `GSR-SHOCKDECAY-001` (EURUSD / USDJPY) | `GSR-TKYFIX-001` (USDJPY) | ゲート合否 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **① 機会台帳の一致・OOS完全遮断** | 台帳SHA256一致、母数フロー（Raw→除外→PASS）完全一致、`oos_locked: true` | **PASS**<br>EURUSD: Raw 19,827 → PASS 19,732 (除外95)<br>USDJPY: Raw 22,396 → PASS 22,286 (除外110) | **PASS**<br>EURUSD: Raw 28,036 → PASS 27,377 (除外659)<br>USDJPY: Raw 28,509 → PASS 27,528 (除外981) | **PASS**<br>USDJPY: Raw 1,177 → PASS 1,177 (除外0、有効率100.0%)<br>全99,945行 SHA256 `7f8581b6...7d38` 一致 | **`PASS`（全案件）** |
| **② IS期間のHAC信頼下限 > 損益分岐54.054%** | ペイアウト1.85倍（BE `54.0541%`）、`+0.1 pip` ストレス、同値LOSE下で $\text{CLB}_{97.5\%} > 0$ | **FAIL**<br>・EURUSD ($n=9,395$): 勝率 `49.88%`, $\text{EV}=-0.0773$, $\text{CLB}_{97.5\%}=-0.0960$<br>・USDJPY ($n=10,263$): 勝率 `49.29%`, $\text{EV}=-0.0881$, $\text{CLB}_{97.5\%}=-0.1060$ | **FAIL**<br>・EURUSD ($n=11,749$): 勝率 `51.03%`, $\text{EV}=-0.0559$, $\text{CLB}_{97.5\%}=-0.0727$<br>・USDJPY ($n=11,964$): 勝率 `51.14%`, $\text{EV}=-0.0540$, $\text{CLB}_{97.5\%}=-0.0704$ | **HOLD（TRAP-06汚染分離へ）**<br>・CANDIDATE ($n=561$): 勝率 **`57.40%`** (+3.34%pt超), $\text{EV}=+0.0619$, $\text{SE}_{\text{HAC}}=0.0413$, $\text{CLB}_{97.5\%}=-0.0190$ ($t=+1.4991$)<br>※OR条件混入の弱ヒゲ層 `B1_sub0.25` ($n=207$, 勝率 `50.72%`) が足を引っ張った結果であり、純粋ヒゲ拒絶層（$n=353$）では勝率 **`61.19%`**。 | `EXHAUST`: **FAIL**<br>`SHOCK`: **FAIL**<br>`TKYFIX`: **HOLD** |
| **③ 近傍Plateauの広さ（非重複3D＆1Dマージナル）** | 非重複（Disjoint）格子および1Dマージナルでの安定性・過分割排除 | **FAIL**<br>EURUSD 0/37セル、USDJPY 0/45セル。局所BE超え2セルもL1近傍合格 `0/4` の孤立ピーク。 | **FAIL**<br>EURUSD 0/48セル、USDJPY 0/48セル。EURUSDの局所黒字座標はUSDJPYで赤字転落し再現性なし。 | **HOLD（TRAP-07過分割排除へ）**<br>年約80件の日次イベントに4×4×4=64分割を適用したため全61セルが $n < 50$（平均9.2件/セル）に細分化。1Dマージナルでは `B2_2.0_2.6` ($n=114$, `62.28%`) が $\text{CLB}_{97.5\%}=+0.0071 > 0$ を達成。 | `EXHAUST`: **FAIL**<br>`SHOCK`: **FAIL**<br>`TKYFIX`: **HOLD** |
| **④ Spark監査での未来参照・アブレーション・選択バイアス** | 未来参照ゼロ、CONTROL群に対する正のアブレーション増分、年次安定性 | **FAIL（逆アブレーション）**<br>CONTROL群に対し両通貨で勝率が **`-2.40%pt` 悪化**。7年中7年すべてで損益分岐割れ。 | **FAIL（逆アブレーション）**<br>CONTROL群に対し勝率が `-0.32%pt` / `-0.45%pt` 悪化。7年中7年すべてで損益分岐割れ。 | **PASS（正のアブレーション）**<br>未来参照なし。CONTROL群（`54.38%`）に対し **`+3.02%pt`（$\Delta\text{EV}=+0.0558$）の明確な正の増分**。7年中5年（2015, 2016, 2018, 2020, 2021）で黒字。 | `EXHAUST`: **FAIL**<br>`SHOCK`: **FAIL**<br>`TKYFIX`: **PASS** |
| **⑤ MT4での $t+1$ 分Open約定・微細摩擦耐性（+0.1〜+0.3p）** | `Open[t+1]` 参入・`Open[t+6]` 厳密5分満期、`+0.2` / `+0.3 pip` ストレス耐性、順行値幅中央値 | **FAIL（TRAP-05 摩擦崩壊）**<br>値幅中央値 `0.0〜0.1 pip`。`+0.2 pip` で勝率 `47.94%` / `46.78%`、`+0.3 pip` で `46.05%` / `46.17%` へ崩壊。 | **FAIL（TRAP-05 摩擦崩壊）**<br>値幅中央値 `0.1 pip`。`+0.2 pip` で勝率 `47.32%` / `47.61%`、`+0.3 pip` で `44.34%` / `46.82%` へ崩壊。 | **PASS（強靭な摩擦耐性）**<br>値幅中央値 **`+0.50 pip`** を確保。`+0.1 pip` 勝率 **`57.40%`**、`+0.2 pip` 勝率 **`55.62%`**（$\text{EV}=+0.0289$）、`+0.3 pip` 勝率 **`55.26%`**（$\text{EV}=+0.0223$）と全摩擦水準で損益分岐超えを維持。 | `EXHAUST`: **FAIL**<br>`SHOCK`: **FAIL**<br>`TKYFIX`: **PASS** |

---

## 3. 次工程（IS内追加検証：`GSR-TKYFIX-002`）実験契約（Experiment Contract）

- **派生案件コード**: `GSR-TKYFIX-002`（親案件: `GSR-TKYFIX-001` / パイプラインコード: `GSR-2026W47`）
- **対象データ・期間制約**: USDJPY Dukascopy M1生データ（SHA256: `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29`）の **In-Sample期間（`2015-01-01` 〜 `2021-12-31`）のみに厳格限定**。**2022年1月1日以降のOOS期間（1,783,913行）の開封・参照、および他通貨への展開は一切厳禁とする**。
- **検証すべき3つの事前固定実験**:
  1. **実験A（TRAP-06 排除：OR条件汚染の除去と純粋ヒゲ拒絶層の単体検定）**
     - **目的**: `GSR-TKYFIX-001` において OR 条件（`stall_or_wick`）で混入していた弱いヒゲ拒絶層 `B1_sub0.25`（$n=207$, `+0.1pip` 勝率 `50.72%`, $\text{EV}=-0.0616$）を除外し、09:54 JST（00:54 UTC）確定足の純粋な反対ヒゲ拒絶層（`wick_ratio >= 0.25`：既存マージナル `B2_0.25_0.40` + `B3_0.40_0.55` + `B4_0.55_up`、合算 $n=353$、点推定 `+0.1pip` 勝率 `61.19%` / `+0.2pip` 勝率 `59.77%`）単体で通年 Newey-West HAC 片側97.5%信頼下限 $\text{CLB}_{97.5\%} > 0$ を達成するか検証する。
     - **事前固定境界**: `wick_ratio >= 0.25`（主力検証）および `wick_ratio >= 0.40`（高強度拒絶確認）の2水準のみとし、事後的な小数点閾値探索を行わない。
  2. **実験B（ボラティリティ減衰分離：仲値直前15分変動幅およびATR下限の分離検証）**
     - **目的**: 低ボラティリティ年（2017年：勝率 `53.03%`、2019年：勝率 `52.81%`）における優位性減衰が、仲値直前15分間（09:40〜09:54 JST）の絶対変動幅（`|move_15m_pips|`）または `ATR14` の絶対値不足に起因するかを分離検証する。
     - **事前固定境界**: 既存の `15m_move / ATR14 >= 1.5` に加え、絶対変動幅 `|move_15m_pips| >= 3.0 pips`（および `>= 4.0 pips`）の下限フィルタを単一変更として適用し、2017年・2019年を含む通年安定性と順行幅中央値（`>= 0.50 pip`）の推移を検証する。
  3. **実験C（TRAP-07 排除：64セル過分割グリッドの廃止と非重複粗視化スライス検証）**
     - **目的**: 年間約50〜80件の日次イベントに対して標本崩壊（1セル平均5〜9件）を引き起こす4×4×4＝64セルグリッドを廃止し、1スライスあたり十分な標本数（目標 $n \ge 80$）を確保する非重複粗視化スライス（Disjoint Coarse Slices）で構造安定性を検証する。
     - **事前固定スライス軸**:
       - ① **売買方向別（2区分）**: 仲値買い需要過多後の `SHORT`（`direction == -1`）vs 仲値売り先行後の `LONG`（`direction == +1`）
       - ② **曜日・決済集中日区分（2〜3区分）**: ゴトー日（5・10日および直前営業日）/ 月末営業日 vs 通常営業日、または曜日別（月〜金）
       - ③ **ボラティリティ粗視化（2区分）**: `ATR14` 中央値（または `2.0 pips`）による Low / High 2分割

---

## 4. 第1〜第3工程 検証スクリプト・ドキュメント・軽量集計証跡のSHA256一覧

| 工程 | ファイル名 | 種別・規模 | SHA256（実測照合値） | 確認状態区分（手順書8原則） |
| :--- | :--- | :--- | :--- | :--- |
| 共通正本 | `QUANT_PYTHON_MASTER_CONTEXT.md` (v2.2) | Markdown (7,518 B) | `89f9c215a02717b1057cd14fa9167b5b8cb7fbc37e60760dbe5f572c2bbb9d13` | `現行版確認済み` |
| 共通規約 | `GEMINI_DISCOVERY_TRACE_RULE.md` | Markdown (3,082 B) | `fd70c9e64015404b8c324a03a62135a4b1f3229f5f8100d157d139c25517a4d6` | `現行版確認済み` |
| 第1工程 | `profile_is_market_structure_gsr_2026w47_v1_0.py` (v1.0.2) | Python (14,105 B) | `d3f4ba214a79bb41e38313a1dbd307afff4a303ef836bee3d922ed77619bc5a1` | **`実行確認済み`** |
| 第1工程 | `stage1_to_stage2_handover_manifest_gsr_2026w47.json` | JSON (2,385 B) | `37a8842b0d34471d3adeeafac241279c85ab19fcb099b28f9155128c990b969c` | **`実行確認済み`**（Git登録対象） |
| 第1工程 | `is_2015_2021_opportunity_ledger_gsr_2026w47.csv` | CSV (26,659,086 B / 99,945 rows) | `7f8581b693da499064dd3d0aaee2f20c2babc84d8859dfd852c923b5f91c7d38` | **`実行確認済み`**（Drive保管 / **Git除外**） |
| 第2工程 | `gsr_2026w47_is_plateau_verifier_v1_0.py` (v1.0.0) | Python (14,471 B) | `0e888bc1e4926d6d41d7cbd16d46c78d01c4c2b1a2e21a2ad1fe5e08f439fc2f` | **`実行確認済み`** |
| 第2工程 | `GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md` | Markdown (25,996 B) | `1acd59bbe6223985aaa8335dc7b27be7287703a484ce1ae890c9d1240a410118` | **`実行確認済み`** |
| 第2工程 | `spark_audit_handover_manifest_gsr_2026w47.json` | JSON (10,363 B) | `ad1b5c8b7b4b5ae430774c96f13e10759697de227f77e9e4edcf4fd62dc8e2eb` | **`実行確認済み`**（Git登録対象） |
| 第2工程 | `is_standalone_and_ablation_summary_gsr_2026w47.csv` | CSV (2,671 B / 15 rows) | `ba83b1a2a5e5c6543634d721bf5ab1e68d42e2bd3e0d7ecd3013c1d052ff375d` | **`実行確認済み`**（Git登録対象） |
| 第2工程 | `is_disjoint_3d_grid_gsr_2026w47.csv` | CSV (33,065 B / 239 rows) | `e2ed1b6edd958492541d9deb1e215ea4fec1cd3df26bd26517210e5bbea1926e` | **`実行確認済み`**（Git登録対象） |
| 第2工程 | `is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv` | CSV (8,677 B / 108 rows) | `0d9038e743d0af17643e1c191528be1bdca678cdfe3001c25d14bc2f85626bfb` | **`実行確認済み`**（Git登録対象） |
