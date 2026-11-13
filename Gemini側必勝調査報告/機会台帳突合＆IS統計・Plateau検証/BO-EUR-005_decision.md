# BO-EUR-005 Decision Record — M1境界再テストモデル（London Pre-Open Breakout → Re-entry → Boundary Retest）

* **Case ID**: `BO-EUR-005`
* **Decision Date**: `2026-11-05`
* **Final Status**: **棄却・凍結（REJECTED / CLOSED AT IN-SAMPLE GATE）**
* **Evaluated Scope**: In-Sample (`2015-01-07` .. `2021-12-31`, 2,551 calendar days / 1,050 valid opportunity instances)
* **Holdout Protection**: `VIEWED_EVAL` (`2022-01-01` .. `2026-09-09`, 748 rows) **Unopened / Masked (`viewed_eval_rows_masked: 748`)**

## 1. 4者合意・最終判定サマリ

| 役割 | 担当 | 判定 | 根拠要約 |
| :--- | :--- | :--- | :--- |
| 機会台帳・基準実装 | Scout / Codex | 完了 | `opportunity_ledger.csv`（SHA256: `029f97ab...`、4,264日）および `contract_v05.json`（SHA256: `b55657bc...`）に基づく10⁻⁵整数点・Label-free台帳・`Control I` 非破壊保持を完全実装。 |
| 統計検証・Plateau分析 | Gemini | **棄却** | IS単独成績で全群（`I`, `R`, `B`）が損益分岐勝率 `54.054%`（ペイアウト `1.85`）未満かつ Newey-West HAC 97.5%信頼下限（$\text{CLB}_{97.5\%}$）が負値（`NOT_ABOVE_ZERO`）。432セル×3ストレス水準でも $\text{CLB}_{97.5\%} > 0$ のセルは `0 / 432`。 |
| 独立性能・過剰適合監査 | Spark | **棄却（FAIL）** | 独立再計算で全指標が小数点以下12桁まで完全一致。`B - I` の正の差分は「`I` 保有中の逆行再ブレイク日における `I` の構造的惨敗（勝率 `26.27%`）」の裏返しであり、`R` の3セル `STABLE_PLATEAU` も `bars_to_reentry == 1`（$n=40$）の共有と `bars_to_retest == 2`（$n=8$、7勝1敗）の局所スパイクによる**擬似プラトー（Pseudo-Plateau）**であることを実証。 |
| 執行監査・週次総括 | Gemini | **開発終了承認** | 最終5ゲート確認を完了し、`VIEWED_EVAL`（2022–2026）を開封することなく `BO-EUR-005`（M1境界再テスト仮説）を正式棄却・凍結。 |

## 2. 最終5ゲート確認結果（Executive Gate Checklist）

1. **ゲート①：機会台帳（Opportunity Ledger）の一致・データ完全性 — `[PASS]`**
   * `opportunity_ledger.csv`（SHA256: `029f97ab3ac5c3d8084f30414422ce73d27f0fafc5e5ac2395bcd1fe4173e954`）の全4,264日・IS期間2,551日において、日付重複 `0`、未来ラベル混入 `0`（Label-free）、`Control I` 独立シグナル時刻の非破壊保持（全1,042件 / IS 604件）を確認。
   * 6分間連続性（欠損バー・重複時刻・OHLC整合性）の違反はIS全1,050件（`I`: 604, `R`: 210, `B`: 236）で `0件`（`valid = 100%`）。
   * ※監査注記：`impl1_cli/outcomes.csv`（1,798行・CRLF）の正規SHA256は `080dc7a36d0e32d7f00b0288eb06bf0f44db4d2710417edd56520e3d466b8687`（LF版は `540f3e11...`）であり、`bo_eur_005_is_plateau_verifier.py` v2.4 にて定数定義を正規ハッシュへ統一済み。

2. **ゲート②：IS期間（2015–2021）のHAC信頼下限 > 損益分岐54.054%（$\text{EV} > 0$） — `[FAIL（棄却決定因）]`**
   * **Control `I`（初回再侵入）**: $n=604$（285勝319敗）、勝率 `47.19%`（損益分岐比 `-6.87%pt`）、$\text{EV} = -0.127070$、$\text{SE}_{\text{HAC}} = 0.038077$、$\text{CLB}_{97.5\%} = -0.201850$（$t = -3.3371$, `NOT_ABOVE_ZERO`）
   * **Candidate `R`（再テスト反発）**: $n=210$（106勝104敗）、勝率 `50.48%`（損益分岐比 `-3.58%pt`）、$\text{EV} = -0.066190$、$\text{SE}_{\text{HAC}} = 0.060369$、$\text{CLB}_{97.5\%} = -0.185200$（$t = -1.0964$, `NOT_ABOVE_ZERO`）
   * **Candidate `B`（再テスト再ブレイク）**: $n=236$（101勝135敗）、勝率 `42.80%`（損益分岐比 `-11.26%pt`）、$\text{EV} = -0.208263$、$\text{SE}_{\text{HAC}} = 0.063513$、$\text{CLB}_{97.5\%} = -0.333391$（$t = -3.2791$, `NOT_ABOVE_ZERO`）
   * **同日ペア比較（`R - I` / `B - I`）**:
     * `R - I`（$n=210$）：$\Delta\text{EV} = +0.105714$、$\text{CLB}_{97.5\%} = -0.007942$（`NOT_ABOVE_ZERO`）。特に `bars_to_retest == 1`（$n=146$、`R` 全体の `69.5%`）では `I` と `R` が5分保有のうち4分間を共有し、勝率 `48.63%`（$\text{EV} = -0.1003$, $\Delta\text{EV} = 0.0000$）と完全同一。
     * `B - I`（$n=236$）：$\Delta\text{EV} = +0.305720$、$\text{CLB}_{97.5\%} = +0.108180$（`REFERENCE_POSITIVE`）。ただしこれは `B` の優位性ではなく、`I` の5分保有窓中に逆方向へ再ブレイクした日における `I` の構造的敗北（勝率 `26.27%`, $\text{EV} = -0.513983$；特に `bars_to_retest == 4, 5` では `I` の勝率 `0.00%`）との相対差に過ぎない。

3. **ゲート③：近傍パラメーターPlateauの広さ — `[FAIL（擬似プラトー・孤立ピークと判定）]`**
   * 432セル中、$\text{CLB}_{97.5\%} > 0$ を満たすセルは全群・全ストレス水準で **`0 / 432`（0.0%）**。
   * `R` 群の `range [200, 350] × max_retest <= 2` に出現した3個の `STABLE_PLATEAU` セルは、Sparkのマージナル（増分）分解により累積条件（`<=`）の入れ子構造が生んだ擬似プラトー（Pseudo-Plateau）と判明：
     * `bars_to_reentry == 1` 単体（$n=40$）：勝率 `60.00%`（$\text{EV} = +0.1100$, $\text{CLB}_{97.5\%} = -0.0568$）
     * `bars_to_reentry == 2` 増分（$n=15$）：勝率 `53.33%`（$\text{EV} = -0.0133$、損益分岐割れ）
     * `bars_to_reentry == 3` 増分（$n=12$）：勝率 `50.00%`（$\text{EV} = -0.0750$、損益分岐割れ）
     * さらに同領域（$n=67$）の `bars_to_retest == 1` 単体（$n=59$、標本の88%）は勝率 `52.54%`（$\text{EV} = -0.0280$）と損益分岐を下回り、`bars_to_retest == 2` 単体（$n=8$、7勝1敗、勝率 `87.50%`）の極小サンプルスパイクによって全体の見かけ勝率が押し上げられていた。
   * また、無条件 `R` が2019–2020年にプラスだった主因は小レンジ帯（`range < 200 pt`: $n=49$, 勝率 `61.22%`）にあり、`range [200, 350] × retest <= 2` 領域自体は2019–2020年に勝率 `50.00%〜53.33%`（損益分岐割れ）であった（Spark監査による年次×レンジ交差検証で確定）。

4. **ゲート④：Spark監査での未来参照・選択バイアス有無 — `[PASS（未来参照なし／コホート選択構造を完全解明）]`**
   * `opportunity_ledger.csv` および `outcomes.csv` における未来参照（Look-ahead bias）は一切なし。
   * 一方で、`I` の全604日を事後の再テスト状態で層別すると、`NO_RETEST / BOUNDARY_DRAW / OPPOSITE_BREAK` の158日では `I` の勝率が `81.65%`（$\text{EV} = +0.5104$）に達する一方、`R` 日（$n=210$）では `44.76%`、`B` 日（$n=236$）では `26.27%` に急落する（エントリー後の価格経路による事後トートロジー）。エントリー時点（$t_0$）で「その後5分間に境界へ戻らない日」を識別する事前情報は存在しないため、実運用上のエッジには変換できない。

5. **ゲート⑤：MT4での $t+1$ 分Open約定・スプレッド耐性（`+0.1`〜`+0.3 pip`） — `[FAIL（微細摩擦で完全崩壊）]`**
   * `+0.1 pip`（1 pt）ストレス下ですでに全群の単独EVがマイナスであるうえ、`+0.2 pip`（2 pt）では `R` 群の損益分岐超えセルが192セル中 `6セル`、`+0.3 pip`（3 pt）では **`0セル`（完全消滅）**。
   * `R` 群の5分後価格変化の中央値は `+1.0 pt`（`+0.1 pip`）に張り付いており、わずか `1〜2 pt`（`0.1〜0.2 pip`）のスプレッド・スリッページで 22件（`+0.2 pip` 時）〜 38件（`+0.3 pip` 時）の勝ちトレードが負けへ転落するため、実機MT4 / BO約定環境での生存性は皆無。

## 3. アーカイブ・資産整理記録

* **指定保管フォルダ（正本）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\`
* **検証スクリプト**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\bo_eur_005_is_plateau_verifier.py` (v2.4)
* **出力証跡フォルダ**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\output_is_plateau_20261104_173018\`
* **決定文書**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\BO-EUR-005_decision.md`
* **引き継ぎ・独立監査ログ**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\BO-EUR-005_Spark_Audit_and_Handover_Log_2026-11-05.md`