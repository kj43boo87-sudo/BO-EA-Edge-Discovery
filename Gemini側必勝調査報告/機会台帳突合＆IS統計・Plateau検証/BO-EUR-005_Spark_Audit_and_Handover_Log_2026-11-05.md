# BO-EUR-005 引き継ぎ（連携）・独立監査・執行監査 統合ログ

- **保管場所**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証`
- **対象案件**: `BO-EUR-005`（EURUSD M1境界再テストモデル：London Pre-Open Breakout → Re-entry → Boundary Retest）
- **記録日**: `2026-11-05`

---

## Part 1: Gemini → Spark 引き継ぎデータ・マニフェスト要旨（2026-11-04 実行分）

- **出力フォルダ**: `output_is_plateau_20261104_173018/`
- **検証スクリプト**: `bo_eur_005_is_plateau_verifier.py`
- **マニフェスト**: `spark_audit_handover_manifest.json`
  - `contract_sha256`: `b55657bccd92617fc241bcbc1962167c897aa7e761dd584601e42ee2dfc45fa5`
  - `ledger_sha256`: `029f97ab3ac5c3d8084f30414422ce73d27f0fafc5e5ac2395bcd1fe4173e954`（4,264日 / IS 2,551日）
  - `outcomes_sha256`: `080dc7a36d0e32d7f00b0288eb06bf0f44db4d2710417edd56520e3d466b8687`（1,798行 / IS 1,050行 / VIEWED_EVAL 748行マスク済み）

---

## Part 2: Spark 独立性能・過剰適合監査ログ（全文記録）

🏷️ [TRACE: BO-EUR-005 | 棄却 | IS期間（2015-2021）実機検証・Plateau格子分析に対するSpark独立性能・過剰適合監査]
<!-- RESEARCH_TRACE_START
ai_id: spark
session_title: IS期間（2015-2021）実機検証・Plateau格子分析に対するSpark独立性能・過剰適合監査
case_id: BO-EUR-005
parent_case_id: BO-EUR-004
decision: 棄却
target_market: EURUSD_1M
attachment_file: spark_audit_handover_manifest.json, is_outcomes.csv, is_standalone_summary.csv, is_paired_summary.csv, is_yearly_breakdown.csv, is_plateau_grid.csv
part_info: 1/1
timestamp: 2026-11-04 17:45:00
-->

### 0. 監査要約（Executive Audit Verdict）

- `audit_verdict`: **`FAIL`（戦略・候補仮説ともに統計的棄却確定 / Geminiの棄却判定を全面支持）**
- `decision`: **`棄却`（`VIEWED_EVAL` 2022–2026年の開封を禁止し、IS段階で開発終了・凍結）**
- `primary_reasons`:
  1. **IS単独成績の全面的敗北（全群 `NOT_ABOVE_ZERO`）**: `0.1 pip`（1 pt）ストレス・同値LOSE・ペイアウト `1.85`（損益分岐勝率 `54.054%`）のContract v0.5基準下において、`Control I`（$n=604$, 勝率 `47.19%`, $\text{EV}=-0.1271$, $\text{CLB}_{97.5\%}=-0.2019$）、`Candidate R`（$n=210$, 勝率 `50.48%`, $\text{EV}=-0.0662$, $\text{CLB}_{97.5\%}=-0.1852$）、`Candidate B`（$n=236$, 勝率 `42.80%`, $\text{EV}=-0.2083$, $\text{CLB}_{97.5\%}=-0.3334$）のすべてが損益分岐を大きく下回り、独立再計算でも小数点以下12桁まで完全一致した。
  2. **同日ペア比較（`B - I`, `R - I`）のカラクリ解明**:
     - `B - I`（$n=236$, $\Delta\text{EV}=+0.3057$, $\text{CLB}_{97.5\%}=+0.1082$）のプラスは、`B` が優れているからではなく、**「`I`（ブレイク逆張り）をエントリーした直後の5分保有窓中に、価格が境界を逆方向へ再ブレイク（`B` 発火）した日」における `I` の勝率が `26.27%`（$\text{EV}=-0.5140$）へと構造的に崩壊する**ためである（特に `bars_to_retest == 4, 5` では `I` の勝率は **`0.00%`**）。
     - `R - I`（$n=210$, $\Delta\text{EV}=+0.1057$, $\text{CLB}_{97.5\%}=-0.0079$）についても、`R` の **69.5%（146/210件）を占める `bars_to_retest == 1`（再侵入の翌分に再テスト）** では、`I`（$t_0$〜$t_0+5$）と `R`（$t_0+1$〜$t_0+6$）が5分間のうち4分間を共有しており、**両者の勝率は `48.63%`（$\text{EV}=-0.1003$, $\Delta\text{EV}=0.0000$）で完全同一**である。
  3. **`R` 群の3セル `STABLE_PLATEAU` の反証（累積格子による「擬似プラトー」と $n=8$ スパイク）**:
     - `is_plateau_grid.csv` で `STABLE_PLATEAU` と分類された `R` 群の3セル（`range [200, 350] × max_retest <= 2 × max_reentry ∈ {1, 2, 3}`）は、累積条件（`<=`）による入れ子（ネスト）が生んだ**擬似プラトー（Pseudo-Plateau）**である。
     - マージナル（増分）分解を行うと、黒字なのは共通の土台である `bars_to_reentry == 1`（$n=40$, 勝率 `60.00%`, $\text{EV}=+0.1100$, $\text{CLB}_{97.5\%}=-0.0568$）のみであり、追加された `bars_to_reentry == 2` 単体（$n=15$, 勝率 `53.33%`, $\text{EV}=-0.0133$）および `bars_to_reentry == 3` 単体（$n=12$, 勝率 `50.00%`, $\text{EV}=-0.0750$）はいずれも損益分岐割れである。
     - さらに、この $n=67$ のセル内部を `bars_to_retest` 別に分解すると、88%を占める `bars_to_retest == 1`（$n=59$）は勝率 **`52.54%`**（$\text{EV}=-0.0280$）と損益分岐割れであり、見かけのプラスは **`bars_to_retest == 2` のわずか $n=8$（7勝1敗、勝率 `87.50%`）の極小サンプルスパイク**に依存している。
  4. **Gemini引き継ぎログに対する2点の監査指摘（正確性補正）**:
     - **指摘①（年次偏在の真因）**: 無条件 `R` が2019–2020年にプラスだったのは **`range < 200 pt`（小レンジ帯：$n=49$, 勝率 `61.22%`）** のおかげであり、Plateau領域（`range [200, 350] × retest <= 2`）自体は2019–2020年に **`50.00%〜53.33%`（赤字）** であった。
     - **指摘②（`outcomes.csv` のSHA256表記不一致）**: マニフェストの `outcomes_sha256` は `080dc7a36d0e32d7f00b0288eb06bf0f44db4d2710417edd56520e3d466b8687` であり、スクリプト定数の `f9bc2ae7...`（`summary.csv` のハッシュ）を正規ハッシュへ統一すべきである（※v2.3/v2.4にて修正完了）。

<!-- RESEARCH_TRACE_END -->

---

## Part 3: Gemini 執行監査・週次総括ログ（2026-11-05 確定）

🏷️ [TRACE: BO-EUR-005 | 棄却 | 執行監査・週次総括・最終5ゲート判定・Git資産整理完了]
<!-- RESEARCH_TRACE_START
ai_id: gemini
session_title: 執行監査・週次総括・最終5ゲート判定・Git資産整理完了
case_id: BO-EUR-005
parent_case_id: BO-EUR-004
decision: 棄却
target_market: EURUSD_1M
attachment_file: BO-EUR-005_decision.md, bo_eur_005_is_plateau_verifier.py, spark_audit_handover_manifest.json
part_info: 1/1
timestamp: 2026-11-05 12:40:00
-->

1. **最終5ゲート判定**:
   - ①機会台帳の一致：`PASS`
   - ②IS期間のHAC信頼下限 > 損益分岐54.054%：`FAIL`（全群 `NOT_ABOVE_ZERO`）
   - ③近傍Plateauの広さ：`FAIL`（432セル中 $\text{CLB}_{97.5\%} > 0$ は `0セル`、`R` の3セルも擬似プラトーと確定）
   - ④Spark監査での未来参照・選択バイアス有無：`PASS`（未来参照なし、事後コホート選別構造を完全解明）
   - ⑤MT4 $t+1$分Open約定・スプレッド耐性：`FAIL`（`+0.3 pip` で損益分岐超え `0セル`）
2. **最終決定**: `VIEWED_EVAL`（2022–2026年、748件）を未開封のまま、`BO-EUR-005` をISゲートにて正式棄却・開発終了。

<!-- RESEARCH_TRACE_END -->
