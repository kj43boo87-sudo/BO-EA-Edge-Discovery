🏷️ [TRACE: GSR-202611-W3-WED | 棄却 | GSR-2026W47 第2工程：機会台帳突合＆IS統計・非累積3D Plateau検証（GSR-EXHAUST-001 / GSR-SHOCKDECAY-001 / GSR-TKYFIX-001）]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W47; GSR-EXHAUST-001; GSR-SHOCKDECAY-001; GSR-TKYFIX-001; stage1_to_stage2_handover_manifest_gsr_2026w47.json; is_2015_2021_opportunity_ledger_gsr_2026w47.csv; gsr_2026w47_is_plateau_verifier_v1_0.py; spark_audit_handover_manifest_gsr_2026w47.json; QUANT_PYTHON_MASTER_CONTEXT.md (v2.2); GEMINI_DISCOVERY_TRACE_RULE.md; 比較参照アーカイブ: GSR-2026W46 / BO-EUR-005
record_id: GSR-202611-W3-WED
session_title: GSR-2026W47 第2工程：機会台帳突合＆IS統計・非累積3D Plateau検証（GSR-EXHAUST-001 / GSR-SHOCKDECAY-001 / GSR-TKYFIX-001）
case_id: GSR-202611-W3-WED
parent_case_id: GSR-2026W47
decision: 棄却
target_market: EURUSD_M1_M5 / USDJPY_M1_M5 (BO_STANDARD / 5-min expiry)
attachment_file: GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md, spark_audit_handover_manifest_gsr_2026w47.json, is_standalone_and_ablation_summary_gsr_2026w47.csv, is_disjoint_3d_grid_gsr_2026w47.csv, is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv
part_info: 1/1
timestamp: 2026-11-11 06:00:00 JST
-->

## 0. 第2工程 総括判定（Executive Verdict）

- **対象パイプライン案件**: `GSR-2026W47`（第2工程レコードID: `GSR-202611-W3-WED`）
- **対象ドメイン**: `BO_STANDARD`（固定5分満期バイナリーオプション：`Open[t+1]` 参入、`Open[t+6]` 厳密300秒満期判定、同値 Draw = LOSE、ペイアウト `1.85倍`［損益分岐勝率 `54.0541%`］、`+0.1 / +0.2 / +0.3 pip` 摩擦負荷）
- **第2工程 総合判定**: **`棄却（FAIL_NOT_ABOVE_ZERO）`**（全3候補5組において IS 期間の Newey-West HAC 97.5%片側信頼下限 $\text{CLB}_{97.5\%} > 0$ 未達、かつ非重複3D 239セル格子で合格セル `0 / 239` のため、2022–2026年OOS期間を未開封ロック維持のままISゲートにて棄却勧告）

---

## 1. 参照パスと台帳突合（Gate 1 審査：`PASS`）

### 1.1 第1工程・第2工程 資産および SHA256 ハッシュ照合表

| 工程区分 | ファイル名 / パス | 実測サイズ / 行数 | SHA256（実測照合値） | 確認状態区分 | 照合結果 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 共通上位正本 | `QUANT_PYTHON_MASTER_CONTEXT.md` (v2.2) | Master Spec | `89f9c215a02717b1057cd14fa9167b5b8cb7fbc37e60760dbe5f572c2bbb9d13` | `現行版確認済み` | **MATCH** |
| 第2工程標準骨格 | `templates/stage2_standard_validator.py` | Template | `a0c3a1233257248b17d3fff5c4a7012fba36f3d3f6cfb500800e8d8fb22a810e` | `静的確認済み` | **MATCH** |
| 第1工程生データ (EURUSD) | `2026.10.16EURUSD(5)-M1-No Session.csv` | 4,424,366 rows (IS: 2,610,900) | `029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d` | `実行確認済み` | **MATCH** (OOS 1,781,411行遮断) |
| 第1工程生データ (USDJPY) | `2026.10.16USDJPY(3)-M1-No Session.csv` | 4,424,800 rows (IS: 2,608,784) | `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29` | `実行確認済み` | **MATCH** (OOS 1,783,913行遮断) |
| 第1工程抽出スクリプト | `profile_is_market_structure_gsr_2026w47_v1_0.py` (v1.0.2) | 14,105 bytes | `d3f4ba214a79bb41e38313a1dbd307afff4a303ef836bee3d922ed77619bc5a1` | `実行確認済み` | **MATCH** |
| 第1工程引き継ぎJSON | `stage1_to_stage2_handover_manifest_gsr_2026w47.json` | 2,385 bytes | `37a8842b0d34471d3adeeafac241279c85ab19fcb099b28f9155128c990b969c` | `実行確認済み` | **MATCH** |
| 第1工程機会台帳 (Label-Free) | `is_2015_2021_opportunity_ledger_gsr_2026w47.csv` | 26,659,086 bytes / 99,945 rows | `7f8581b693da499064dd3d0aaee2f20c2babc84d8859dfd852c923b5f91c7d38` | `実行確認済み` | **MATCH** (`HOLD_LABEL_FREE`) |
| 第2工程検証スクリプト | `gsr_2026w47_is_plateau_verifier_v1_0.py` (v1.0.0) | 14,471 bytes | `0e888bc1e4926d6d41d7cbd16d46c78d01c4c2b1a2e21a2ad1fe5e08f439fc2f` | `実行確認済み` | **MATCH** |
| 第2工程Standalone集計 | `is_standalone_and_ablation_summary_gsr_2026w47.csv` | 2,671 bytes / 15 rows | `ba83b1a2a5e5c6543634d721bf5ab1e68d42e2bd3e0d7ecd3013c1d052ff375d` | `実行確認済み` | **MATCH** |
| 第2工程非重複3D格子 | `is_disjoint_3d_grid_gsr_2026w47.csv` | 33,065 bytes / 239 rows | `e2ed1b6edd958492541d9deb1e215ea4fec1cd3df26bd26517210e5bbea1926e` | `実行確認済み` | **MATCH** |
| 第2工程1Dマージナル＆年次 | `is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv` | 8,677 bytes / 108 rows | `0d9038e743d0af17643e1c191528be1bdca678cdfe3001c25d14bc2f85626bfb` | `実行確認済み` | **MATCH** |
| 第2工程監査マニフェスト | `spark_audit_handover_manifest_gsr_2026w47.json` | 10,363 bytes | `ad1b5c8b7b4b5ae430774c96f13e10759697de227f77e9e4edcf4fd62dc8e2eb` | `実行確認済み` | **MATCH** |

### 1.2 Gate 1 母数フロー照合（`Raw件数 -> 除外理由別件数 -> 最終採用件数`）

- **OOSロック状態**: `LOCKED`（EURUSD 2022年以降 `1,781,411` 行、USDJPY 2022年以降 `1,783,913` 行を物理遮断。第2工程でも `dt_utc <= 2022-01-01 00:10:00` による2021年末満期参照のみに制限し、台帳内 `expected_entry_utc` 最大値がIS期間内であることを検証済み）。
- **Label-Free整合性**: 第1工程台帳の `win_loss_label` / `net_pips_result` 列は全99,945行で `"HOLD_LABEL_FREE"` にマスク済み。

| 案件コード (`case_id`) | 通貨ペア | コホート区分 | Raw抽出件数 | 除外件数 (`GAP_OR_INVALID_T1_T6`) | 最終採用件数 (`PASS`) | 6分間連続性有効率 |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: |
| `GSR-EXHAUST-001` | `EURUSD` | `ALL_POOLED` (`CTRL + CAND`) | 19,827 | 95 | **19,732** | 99.52% |
| `GSR-EXHAUST-001` | `EURUSD` | `CONTROL_ONLY` | 10,380 | 43 | **10,337** | 99.59% |
| `GSR-EXHAUST-001` | `EURUSD` | `CANDIDATE` | 9,447 | 52 | **9,395** | 99.45% |
| `GSR-EXHAUST-001` | `USDJPY` | `ALL_POOLED` (`CTRL + CAND`) | 22,396 | 110 | **22,286** | 99.51% |
| `GSR-EXHAUST-001` | `USDJPY` | `CONTROL_ONLY` | 12,087 | 64 | **12,023** | 99.47% |
| `GSR-EXHAUST-001` | `USDJPY` | `CANDIDATE` | 10,309 | 46 | **10,263** | 99.55% |
| `GSR-SHOCKDECAY-001` | `EURUSD` | `ALL_POOLED` (`CTRL + CAND`) | 28,036 | 659 | **27,377** | 97.65% |
| `GSR-SHOCKDECAY-001` | `EURUSD` | `CONTROL_ONLY` | 15,884 | 256 | **15,628** | 98.39% |
| `GSR-SHOCKDECAY-001` | `EURUSD` | `CANDIDATE` | 12,152 | 403 | **11,749** | 96.68% |
| `GSR-SHOCKDECAY-001` | `USDJPY` | `ALL_POOLED` (`CTRL + CAND`) | 28,509 | 981 | **27,528** | 96.56% |
| `GSR-SHOCKDECAY-001` | `USDJPY` | `CONTROL_ONLY` | 15,925 | 361 | **15,564** | 97.73% |
| `GSR-SHOCKDECAY-001` | `USDJPY` | `CANDIDATE` | 12,584 | 620 | **11,964** | 95.07% |
| `GSR-TKYFIX-001` | `USDJPY` | `ALL_POOLED` (`CTRL + CAND`) | 1,177 | 0 | **1,177** | 100.00% |
| `GSR-TKYFIX-001` | `USDJPY` | `CONTROL_ONLY` | 616 | 0 | **616** | 100.00% |
| `GSR-TKYFIX-001` | `USDJPY` | `CANDIDATE` | 561 | 0 | **561** | 100.00% |
| **全案件合計** | **2通貨計** | **全行合計 (`ALL_POOLED`)** | **99,945** | **1,845** | **98,100** | **98.15%** |

---

## 2. ドメイン別・一次統計検証と摩擦ストレス負荷（Gate 2 & Gate 5 審査：`FAIL`）

### 2.1 IS期間（2015–2021）Standalone & Control アブレーション検証テーブル（`BO_STANDARD`）

- **評価仕様**: 参入 `Open[t+1]`、満期 `Open[t+6]`（厳密5分）、同値 `LOSE`（`signed_move_pips > stress_pips` のみ勝ち）、ペイアウト `1.85倍`（損益分岐勝率 `54.0541%`）、Newey-West HAC（Bartlett kernel, `max_lag=5`, 小標本補正 $n/(n-1)$ 適用）片側97.5%信頼下限 $\text{CLB}_{97.5\%}$。

| 案件コード | 通貨 | コホート | 有効数 $n$ | 0.0p勝率 (同値LOSE) | +0.1p 勝数 / 敗数 | +0.1p 勝率 (%) | +0.1p EV | $\text{SE}_{\text{HAC}}$ | $\text{CLB}_{97.5\%}$ (EV) | $t$ 値 | +0.2p 勝率 / EV | +0.3p 勝率 / EV | 順行幅中央値 | Control比増分 ($\Delta\text{WR}$ / $\Delta\text{EV}$) | Gate 2 判定 |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- | :--- |
| `GSR-EXHAUST-001` | `EURUSD` | `ALL_POOLED` | 19,732 | 51.63% | 10,090 / 9,642 | 51.14% | -0.05400 | 0.00663 | -0.06700 | -8.1418 | 49.27% / -0.0885 | 47.45% / -0.1223 | +0.20p | — | `FAIL_NOT_ABOVE_ZERO` |
| `GSR-EXHAUST-001` | `EURUSD` | `CONTROL_ONLY` | 10,337 | 52.71% | 5,404 / 4,933 | 52.28% | -0.03285 | 0.00918 | -0.05085 | -3.5770 | 50.48% / -0.0661 | 48.72% / -0.0987 | +0.30p | 基準群 | `FAIL_NOT_ABOVE_ZERO` |
| **`GSR-EXHAUST-001`** | **`EURUSD`** | **`CANDIDATE`** | **9,395** | **50.44%** | **4,686 / 4,709** | **49.88%** | **-0.07727** | **0.00958** | **-0.09603** | **-8.0697** | **47.94% / -0.1131** | **46.05% / -0.1482** | **+0.10p** | **-2.40%pt / -0.0444** (逆効果) | **`FAIL_NOT_ABOVE_ZERO`** |
| `GSR-EXHAUST-001` | `USDJPY` | `ALL_POOLED` | 22,286 | 51.15% | 11,274 / 11,012 | 50.59% | -0.06413 | 0.00623 | -0.07633 | -10.2958 | 48.44% / -0.1039 | 47.85% / -0.1148 | +0.10p | — | `FAIL_NOT_ABOVE_ZERO` |
| `GSR-EXHAUST-001` | `USDJPY` | `CONTROL_ONLY` | 12,023 | 52.25% | 6,215 / 5,808 | 51.69% | -0.04369 | 0.00824 | -0.05983 | -5.3029 | 49.85% / -0.0777 | 49.28% / -0.0883 | +0.20p | 基準群 | `FAIL_NOT_ABOVE_ZERO` |
| **`GSR-EXHAUST-001`** | **`USDJPY`** | **`CANDIDATE`** | **10,263** | **49.86%** | **5,059 / 5,204** | **49.29%** | **-0.08807** | **0.00917** | **-0.10603** | **-9.6097** | **46.78% / -0.1346** | **46.17% / -0.1459** | **0.00p** | **-2.40%pt / -0.0444** (逆効果) | **`FAIL_NOT_ABOVE_ZERO`** |
| `GSR-SHOCKDECAY-001` | `EURUSD` | `ALL_POOLED` | 27,377 | 52.11% | 14,021 / 13,356 | 51.21% | -0.05253 | 0.00556 | -0.06343 | -9.4437 | 47.78% / -0.1161 | 44.90% / -0.1693 | +0.10p | — | `FAIL_NOT_ABOVE_ZERO` |
| `GSR-SHOCKDECAY-001` | `EURUSD` | `CONTROL_ONLY` | 15,628 | 52.25% | 8,025 / 7,603 | 51.35% | -0.05002 | 0.00741 | -0.06455 | -6.7493 | 48.13% / -0.1097 | 45.33% / -0.1614 | +0.10p | 基準群 | `FAIL_NOT_ABOVE_ZERO` |
| **`GSR-SHOCKDECAY-001`** | **`EURUSD`** | **`CANDIDATE`** | **11,749** | **51.92%** | **5,996 / 5,753** | **51.03%** | **-0.05587** | **0.00861** | **-0.07273** | **-6.4925** | **47.32% / -0.1245** | **44.34% / -0.1798** | **+0.10p** | **-0.32%pt / -0.0058** (逆効果) | **`FAIL_NOT_ABOVE_ZERO`** |
| `GSR-SHOCKDECAY-001` | `USDJPY` | `ALL_POOLED` | 27,528 | 52.21% | 14,147 / 13,381 | 51.39% | -0.04926 | 0.00556 | -0.06016 | -8.8589 | 48.07% / -0.1106 | 47.26% / -0.1257 | +0.10p | — | `FAIL_NOT_ABOVE_ZERO` |
| `GSR-SHOCKDECAY-001` | `USDJPY` | `CONTROL_ONLY` | 15,564 | 52.41% | 8,029 / 7,535 | 51.59% | -0.04564 | 0.00743 | -0.06020 | -6.1432 | 48.43% / -0.1040 | 47.60% / -0.1195 | +0.10p | 基準群 | `FAIL_NOT_ABOVE_ZERO` |
| **`GSR-SHOCKDECAY-001`** | **`USDJPY`** | **`CANDIDATE`** | **11,964** | **51.95%** | **6,118 / 5,846** | **51.14%** | **-0.05397** | **0.00837** | **-0.07037** | **-6.4502** | **47.61% / -0.1192** | **46.82% / -0.1339** | **+0.10p** | **-0.45%pt / -0.0083** (逆効果) | **`FAIL_NOT_ABOVE_ZERO`** |
| `GSR-TKYFIX-001` | `USDJPY` | `ALL_POOLED` | 1,177 | 56.50% | 657 / 520 | 55.82% | +0.03267 | 0.02824 | -0.02267 | +1.1570 | 54.12% / +0.0012 | 53.87% / -0.0035 | +0.50p | — | `FAIL_NOT_ABOVE_ZERO` |
| `GSR-TKYFIX-001` | `USDJPY` | `CONTROL_ONLY` | 616 | 55.19% | 335 / 281 | 54.38% | +0.00609 | 0.03835 | -0.06907 | +0.1588 | 52.76% / -0.0239 | 52.60% / -0.0269 | +0.45p | 基準群 | `FAIL_NOT_ABOVE_ZERO` |
| **`GSR-TKYFIX-001`** | **`USDJPY`** | **`CANDIDATE`** | **561** | **57.93%** | **322 / 239** | **57.40%** | **+0.06185** | **0.04126** | **-0.01902** | **+1.4991** | **55.62% / +0.0289** | **55.26% / +0.0223** | **+0.50p** | **+3.01%pt / +0.0558** (CLB負) | **`FAIL_NOT_ABOVE_ZERO`** |

### 2.2 Gate 2 & Gate 5 審査要点

1. **`GSR-EXHAUST-001`（前足BB 2.5σ到達後の高安未更新・実体反転フィルタ）**:
   - `EURUSD`（$n=9,395$, 勝率 `49.88%`, $\text{CLB}_{97.5\%}=-0.0960$）および `USDJPY`（$n=10,263$, 勝率 `49.29%`, $\text{CLB}_{97.5\%}=-0.1060$）ともに損益分岐を大きく下回る。
   - **アブレーション逆効果の検出**: 実体反転比率（`body_rev_ratio >= 0.30`）とM5傾き制限（`<= 2.5p`）を課した `CANDIDATE` 群は、フィルタなしの `CONTROL_ONLY` 群よりも両通貨で勝率が **`-2.40%pt` 悪化**している（反転初動で実体を大きく消費した足ほど、次足 `Open[t+1]` 参入時点では平均回帰余地が剥落しているため）。
2. **`GSR-SHOCKDECAY-001`（大実体ショック直後のレンジ急収縮減衰逆張り）**:
   - `EURUSD`（$n=11,749$, 勝率 `51.03%`, $\text{CLB}_{97.5\%}=-0.0727$）および `USDJPY`（$n=11,964$, 勝率 `51.14%`, $\text{CLB}_{97.5\%}=-0.0704$）ともに損益分岐未達。`CONTROL_ONLY` 比の増分も `-0.32%pt` / `-0.45%pt` とマイナスであり、5分順行幅中央値はわずか `+0.10 pip` に張り付いているため、`+0.2 pip` 負荷で勝率 `47%` 台へ急落する。
3. **`GSR-TKYFIX-001`（USDJPY 09:55 JST 東京仲値15分間急伸・急落後の失速逆張り）**:
   - `CANDIDATE` 群（$n=561$）は点推定で勝率 `57.40%`（$\text{EV}=+0.0619$）、`CONTROL_ONLY` 比でも `+3.01%pt`（$\Delta\text{EV}=+0.0558$）、順行幅中央値 `+0.50 pip`、`+0.3 pip` 負荷でも勝率 `55.26%`（$\text{EV}=+0.0223$）を維持する唯一のプラス期待値候補である。
   - しかし、1日最大1回（09:55 JST固定）のイベント戦略であるため7年間の有効母数が $n=561$ に限られ、標準誤差 $\text{SE}_{\text{HAC}} = 0.041261$ に対して片側97.5%信頼下限は **$\text{CLB}_{97.5\%} = -0.019016 < 0$（$t = +1.4991 < 1.960$）** にとどまり、Gate 2 通過基準（$\text{CLB}_{97.5\%} > 0$）を満たさない（7年間で `54.054%` に対する統計的有意差を立証するには $\text{WR} \ge 58.25\%$ またはより大きなサンプルサイズが必要）。

---

## 3. 近傍Plateau（高原）検証と擬似プラトー排除（Gate 3 & Gate 4 準備：`FAIL`）

### 3.1 非重複（Disjoint）3D パラメータ格子（全239セル）全体サマリ

累積不等号（`<=` / `>=`）によるコーナーセルの重複カウントを完全に排除し、直積の非重複区間スライス `[low, high)`（4×4×4＝最大64セル/組）で評価した結果は下表の通りである。

| 案件コード | 通貨 | 実在セル数 | $n \ge 50$ セル数 | $n \ge 30$ セル数 | +0.1p 損益分岐超え ($n \ge 50$) | +0.2p 損益分岐超え ($n \ge 50$) | +0.3p 損益分岐超え ($n \ge 50$) | `DISJOINT_CELL_CLB_PASS` ($n \ge 50$ & $\text{CLB}>0$) | 全セル中 $\text{CLB}>0$ ($n$ 不問) | Gate 3 判定 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| `GSR-EXHAUST-001` | `EURUSD` | 37 | 28 | 32 | 2 / 28 | 2 / 28 | 2 / 28 | **0 / 37** | 0 / 37 | **FAIL** |
| `GSR-EXHAUST-001` | `USDJPY` | 45 | 29 | 33 | 0 / 29 | 0 / 29 | 0 / 29 | **0 / 45** | 0 / 45 | **FAIL** |
| `GSR-SHOCKDECAY-001` | `EURUSD` | 48 | 30 | 41 | 9 / 30 | 7 / 30 | 4 / 30 | **0 / 48** | 0 / 48 | **FAIL** |
| `GSR-SHOCKDECAY-001` | `USDJPY` | 48 | 32 | 41 | 7 / 32 | 4 / 32 | 3 / 32 | **0 / 48** | 0 / 48 | **FAIL** |
| `GSR-TKYFIX-001` | `USDJPY` | 61 | 0 | 1 | 0 / 0 | 0 / 0 | 0 / 0 | **0 / 61** | 2 / 61 ($n=11$ 極小スパイク) | **FAIL** |
| **全体合計** | **5組計** | **239** | **119** | **148** | **18 / 119** | **13 / 119** | **9 / 119** | **`0 / 239` (0.0%)** | **2 / 239 ($n=11$ のみ)** | **FAIL** |

### 3.2 損益分岐超え18セル（`BE_EXCEEDED_CLB_UNPROVEN`, $n \ge 50$）および $n=11$ 局所スパイクのL1近傍安定性監査

1. **`GSR-EXHAUST-001` (`EURUSD`) の2セル**:
   - `B3_3.1_3.5 × B2_0.30_0.50 × B3_1.6_2.5`（$n=105$, 勝率 `58.10%`, $\text{CLB}_{97.5\%}=-0.0657$）：L1隣接4セルのうち損益分岐（`54.054%`）超えは **`0 / 4`（0.0%）** の完全孤立ピーク。
   - `B4_3.5_up × B2_0.30_0.50 × B2_0.8_1.6`（$n=58$, 勝率 `60.34%`, $\text{CLB}_{97.5\%}=-0.0525$）：L1隣接4セル中、$n \ge 50$ で損益分岐超えは **`0 / 4`（0.0%）** の孤立ピーク。
2. **`GSR-SHOCKDECAY-001` (`EURUSD` 9セル / `USDJPY` 7セル)**:
   - 全16セルで $\text{CLB}_{97.5\%}$ は `-0.1994 〜 -0.0190` とすべて負値。
   - `EURUSD` では `bin_axis_2 == B2_0.25_0.35` かつ `bin_axis_3 ∈ {B2_1.5_2.5, B3_2.5_3.5, B4_3.5_up}` に黒字セルが並ぶように見えるが、同じ座標を `USDJPY` に当てはめると `B1_2.2_2.6 × B2_0.25_0.35 × B2_1.5_2.5`（$n=393$, 勝率 `51.15%`, $\text{EV}=-0.0538$）や `B2_2.6_3.2 × B2_0.25_0.35 × B2_1.5_2.5`（$n=258$, 勝率 `48.84%`, $\text{EV}=-0.0965$）と軒並み赤字に転落し、通貨間での構造再現性が存在しない。
   - また、`USDJPY` で最高勝率を示した `B3_3.2_4.0 × B2_0.25_0.35 × B2_1.5_2.5`（$n=110$, 勝率 `62.73%`, $\text{CLB}_{97.5\%}=-0.0190$）は、L1隣接6セルの損益分岐超え数が **`0 / 6`（0.0%）** の完全な孤立スパイクである。
3. **`GSR-TKYFIX-001` (`USDJPY`) の3D細分化と1D非累積マージナル監査**:
   - 3D格子（61セル）で $\text{CLB}_{97.5\%} > 0$ となった2セル（`B2_2.0_2.6 × B2_1.5_2.5 × B3_0.40_0.55`: $n=11$, 9勝2敗; `B4_3.5_up × B1_sub1.5 × B2_0.25_0.40`: $n=11$, 8勝3敗）はいずれも **$n=11 < 30$ の極小サンプルスパイク（`LOW_SAMPLE_UNDER_50`）** であり、Gate 3 規定により即座に棄却される。
   - 1次元非累積マージナル（`is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv`）では、唯一 `bin_axis_1 == B2_2.0_2.6`（$n=114$, 勝率 `62.28%`, $\text{EV}=+0.1522$）が $\text{CLB}_{97.5\%}=+0.0071 > 0$ となったものの、すぐ隣の非累積スライス `B3_2.6_3.5`（$n=151$）で勝率 **`50.33%`（$\text{EV}=-0.0689$, $\text{CLB}_{97.5\%}=-0.2003$）へと急落（谷落ち）**しており、単調性および隣接±1ステップの安定性を欠いている。

### 3.3 1D 非累積マージナル分布および年次安定性（2015–2021）分解テーブル

#### (A) 1次元非累積マージナル分布（全3候補・5組）

| 案件コード | 通貨 | 軸 (`dimension`) | 非累積スライス (`slice_value`) | 有効数 $n$ | +0.1p 勝率 (%) | +0.1p EV | $\text{CLB}_{97.5\%}$ (EV) | +0.2p 勝率 (%) | BE超え | $\text{CLB}>0$ |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| `GSR-EXHAUST-001` | `EURUSD` | `bin_axis_1` (\|prev_z\|) | `B1_2.5_2.8` / `B2_2.8_3.1` / `B3_3.1_3.5` / `B4_3.5_up` | 5,598 / 2,383 / 1,053 / 361 | 49.48% / 51.07% / 49.38% / 49.58% | -0.0846 / -0.0552 / -0.0864 / -0.0827 | 全て `< -0.091` | 47.29%–48.85% | 0 / 4 | 0 / 4 |
| `GSR-EXHAUST-001` | `USDJPY` | `bin_axis_1` (\|prev_z\|) | `B1_2.5_2.8` / `B2_2.8_3.1` / `B3_3.1_3.5` / `B4_3.5_up` | 6,085 / 2,633 / 1,177 / 368 | 49.56% / 49.68% / 46.81% / 50.00% | -0.0831 / -0.0810 / -0.1339 / -0.0750 | 全て `< -0.106` | 44.44%–47.55% | 0 / 4 | 0 / 4 |
| `GSR-SHOCKDECAY-001` | `EURUSD` | `bin_axis_1` (body/ATR) | `B1_2.2_2.6` / `B2_2.6_3.2` / `B3_3.2_4.0` / `B4_4.0_up` | 5,237 / 3,690 / 1,803 / 1,019 | 50.79% / 51.36% / 51.14% / 50.93% | -0.0603 / -0.0499 / -0.0540 / -0.0578 | 全て `< -0.079` | 46.86%–47.83% | 0 / 4 | 0 / 4 |
| `GSR-SHOCKDECAY-001` | `USDJPY` | `bin_axis_1` (body/ATR) | `B1_2.2_2.6` / `B2_2.6_3.2` / `B3_3.2_4.0` / `B4_4.0_up` | 5,279 / 3,726 / 1,779 / 1,180 | 50.48% / 50.51% / 53.91% / 51.86% | -0.0661 / -0.0656 / -0.0027 / -0.0405 | 全て `< -0.045` | 46.96%–50.08% | 0 / 4 | 0 / 4 |
| `GSR-TKYFIX-001` | `USDJPY` | `bin_axis_1` (15m/ATR) | `B1_1.5_2.0` | 112 | 59.82% | +0.1067 | -0.0421 | 58.93% | Yes | No |
| `GSR-TKYFIX-001` | `USDJPY` | `bin_axis_1` (15m/ATR) | `B2_2.0_2.6` | 114 | 62.28% | +0.1522 | **+0.0071** | 59.65% | Yes | **Yes** (隣接B3で崩壊) |
| `GSR-TKYFIX-001` | `USDJPY` | `bin_axis_1` (15m/ATR) | `B3_2.6_3.5` | 151 | **50.33%** | **-0.0689** | **-0.2003** | **47.68%** | **No** | **No** |
| `GSR-TKYFIX-001` | `USDJPY` | `bin_axis_1` (15m/ATR) | `B4_3.5_up` | 184 | 58.70% | +0.0859 | -0.0480 | 57.61% | Yes | No |
| `GSR-TKYFIX-001` | `USDJPY` | `bin_axis_2` (ATR14) | `B1_sub1.5` / `B2_1.5_2.5` / `B3_2.5_4.0` / `B4_4.0_up` | 193 / 239 / 102 / 27 | 59.59% / **53.97%** / 58.82% / 66.67% | +0.1023 / **-0.0015** / +0.0882 / +0.2333 | 全て `< -0.041` | 51.88%–66.67% | 3 / 4 | 0 / 4 |
| `GSR-TKYFIX-001` | `USDJPY` | `bin_axis_3` (stall) | `B1_sub0.25` / `B2_0.25_0.40` / `B3_0.40_0.55` / `B4_0.55_up` | 207 / 95 / 130 / 128 | **50.72%** / 62.11% / 62.31% / 59.38% | **-0.0616** / +0.1489 / +0.1527 / +0.0984 | 全て `< -0.042` | 48.31%–61.05% | 3 / 4 | 0 / 4 |

#### (B) 年次別（2015–2021）安定性分解テーブル（`CANDIDATE` 群、`+0.1 pip` ストレス下）

| 案件コード | 通貨 | 2015年 | 2016年 | 2017年 | 2018年 | 2019年 | 2020年 | 2021年 | 損益分岐超え年数 | $\text{CLB}_{97.5\%}>0$ 年数 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `GSR-EXHAUST-001` | `EURUSD` | 48.65% ($n=1591$) | 50.83% ($n=1450$) | 52.19% ($n=1439$) | 49.83% ($n=1483$) | 48.48% ($n=1089$) | 51.88% ($n=1303$) | 46.25% ($n=1040$) | **0 / 7年** | **0 / 7年** |
| `GSR-EXHAUST-001` | `USDJPY` | 51.64% ($n=1615$) | 48.25% ($n=1712$) | 47.07% ($n=1791$) | 50.33% ($n=1649$) | 50.60% ($n=1249$) | 47.29% ($n=1142$) | 50.14% ($n=1105$) | **0 / 7年** | **0 / 7年** |
| `GSR-SHOCKDECAY-001` | `EURUSD` | 49.95% ($n=2078$) | 52.61% ($n=1800$) | 51.99% ($n=1656$) | 53.01% ($n=1462$) | 50.20% ($n=1731$) | 49.59% ($n=1335$) | 50.03% ($n=1687$) | **0 / 7年** | **0 / 7年** |
| `GSR-SHOCKDECAY-001` | `USDJPY` | 52.70% ($n=1721$) | 51.28% ($n=1675$) | 49.62% ($n=1560$) | 52.10% ($n=1783$) | 50.57% ($n=1764$) | 52.14% ($n=1521$) | 49.69% ($n=1940$) | **0 / 7年** | **0 / 7年** |
| `GSR-TKYFIX-001` | `USDJPY` | **59.09%** ($n=66$) | **61.18%** ($n=85$) | 53.03% ($n=66$, 赤字) | **58.57%** ($n=70$) | 52.81% ($n=89$, 赤字) | **58.43%** ($n=89$) | **58.33%** ($n=96$) | **5 / 7年** | **0 / 7年** |

---

## 4. 金曜・第3工程およびSpark独立監査への引き継ぎマニフェスト（`spark_audit_handover_manifest_gsr_2026w47.json`）

```json
{
  "schema_version": "2.2",
  "pipeline_case_id": "GSR-2026W47",
  "stage2_record_id": "GSR-202611-W3-WED",
  "script_version": "1.0.0",
  "generated_at_jst": "2026-11-10 07:05:59",
  "audited_at_jst": "2026-11-11 06:00:00",
  "verification_status": "実行確認済み",
  "gate1_audit": {
    "stage1_profiler_script": "profile_is_market_structure_gsr_2026w47_v1_0.py",
    "stage1_profiler_sha256": "d3f4ba214a79bb41e38313a1dbd307afff4a303ef836bee3d922ed77619bc5a1",
    "stage1_manifest_json": "stage1_to_stage2_handover_manifest_gsr_2026w47.json",
    "stage1_manifest_sha256": "37a8842b0d34471d3adeeafac241279c85ab19fcb099b28f9155128c990b969c",
    "ledger_csv": "is_2015_2021_opportunity_ledger_gsr_2026w47.csv",
    "ledger_sha256": "7f8581b693da499064dd3d0aaee2f20c2babc84d8859dfd852c923b5f91c7d38",
    "sha256_match": true,
    "total_ledger_rows": 99945,
    "valid_pass_rows": 98100,
    "excluded_gap_rows": 1845,
    "oos_locked": true
  },
  "output_files": {
    "output_dir": "output_gsr_2026w47_is_plateau_20261110_070559",
    "standalone_csv": "is_standalone_and_ablation_summary_gsr_2026w47.csv",
    "standalone_sha256": "ba83b1a2a5e5c6543634d721bf5ab1e68d42e2bd3e0d7ecd3013c1d052ff375d",
    "disjoint_3d_grid_csv": "is_disjoint_3d_grid_gsr_2026w47.csv",
    "disjoint_3d_grid_sha256": "e2ed1b6edd958492541d9deb1e215ea4fec1cd3df26bd26517210e5bbea1926e",
    "marginals_yearly_csv": "is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv",
    "marginals_yearly_sha256": "0d9038e743d0af17643e1c191528be1bdca678cdfe3001c25d14bc2f85626bfb",
    "verifier_script": "gsr_2026w47_is_plateau_verifier_v1_0.py",
    "verifier_script_sha256": "0e888bc1e4926d6d41d7cbd16d46c78d01c4c2b1a2e21a2ad1fe5e08f439fc2f",
    "manifest_json": "spark_audit_handover_manifest_gsr_2026w47.json",
    "manifest_sha256": "ad1b5c8b7b4b5ae430774c96f13e10759697de227f77e9e4edcf4fd62dc8e2eb"
  },
  "grid_overview": {
    "total_evaluated_disjoint_cells": 239,
    "clb975_positive_cells_n50plus": 0,
    "clb975_positive_cells_any_n": 2,
    "breakeven_exceeded_cells_n50plus": 18
  },
  "candidate_decisions": [
    {
      "case_id": "GSR-EXHAUST-001",
      "symbols": ["EURUSD", "USDJPY"],
      "gate1": "PASS",
      "gate2": "FAIL_NOT_ABOVE_ZERO",
      "gate3": "FAIL_ISOLATED_PEAKS_ONLY",
      "gate5": "FAIL_MEDIAN_MOVE_01_TO_00_PIP",
      "ablation_vs_control": "NEGATIVE (-2.40%pt on both EURUSD and USDJPY)",
      "stage2_recommendation": "REJECT_AND_FREEZE"
    },
    {
      "case_id": "GSR-SHOCKDECAY-001",
      "symbols": ["EURUSD", "USDJPY"],
      "gate1": "PASS",
      "gate2": "FAIL_NOT_ABOVE_ZERO",
      "gate3": "FAIL_NO_CLB_POSITIVE_CELLS_AND_NO_CROSS_PAIR_REPRODUCIBILITY",
      "gate5": "FAIL_MEDIAN_MOVE_01_PIP",
      "ablation_vs_control": "NEGATIVE (-0.32%pt EURUSD, -0.45%pt USDJPY)",
      "stage2_recommendation": "REJECT_AND_FREEZE"
    },
    {
      "case_id": "GSR-TKYFIX-001",
      "symbols": ["USDJPY"],
      "gate1": "PASS",
      "gate2": "FAIL_NOT_ABOVE_ZERO (WR=57.40%, EV=+0.0619, CLB97.5=-0.0190, t=+1.4991 on n=561)",
      "gate3": "FAIL_B3_VALLEY_DROP_AND_3D_UNDER_50",
      "gate5": "PASS_POINT_ESTIMATE_ONLY (WR_03pip=55.26%, MedMove=+0.50p)",
      "ablation_vs_control": "POSITIVE (+3.01%pt WR, +0.0558 EV vs CONTROL_ONLY, but CLB97.5 < 0)",
      "stage2_recommendation": "REJECT_AS_STANDALONE_BO_KEEP_OOS_LOCKED"
    }
  ]
}
```
<!-- RESEARCH_TRACE_END -->
