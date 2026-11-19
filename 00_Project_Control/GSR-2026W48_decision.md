# GSR-2026W48 Decision Record — GSR-TKYFIX-002（USDJPY M1 東京仲値 09:55 JST 純粋ヒゲ拒絶5分逆張り）IS全5ゲート完全合格（PASS_CANDIDATE）およびOne-Shot OOS開封・MQL4実装1対1仕様契約

- **Pipeline Case ID**: `GSR-2026W48`（第3工程レコードID: `GSR-202611-W4-FRI` / 親ライン: `Gemini側必勝調査報告`）
- **Evaluated Candidate ID**: **`GSR-TKYFIX-002`**（親候補: `GSR-TKYFIX-001`）
- **Upstream Audit References**:
  - 第1工程：`HANDOVER_GSR_2026W48_STAGE1.md` / `stage1_to_stage2_handover_manifest_gsr_2026w48.json`（SHA256: `120bba20aed68ec7181471a54ab83fcc7d0168121b6ccb87deadb3c625687274`、`LOCAL_FULL_258MB_VERIFIED`）
  - 第2工程：`GSR-2026W48_Stage2_IS_Report.md` / `spark_audit_handover_manifest_gsr_2026w48.json`（SHA256: `3b29debe08aa16dd8816ace61150a79b2f99373c21c467e397a18756f78f7746`）
  - Spark独立性能監査：**`GSR-202611-W4-WED-SPARK.md`**（`audit_verdict: PASS` / `decision: 採用候補 PASS_CANDIDATE`）
- **Decision Date**: `2026-11-20 JST`
- **Final Status**: **採用候補（`PASS_CANDIDATE` — IS全5ゲート完全合格・One-Shot OOS初回開封申請＆MQL4実装仕様凍結）**
- **Evaluated Scope**: USDJPY In-Sample（`2015-01-01 00:00:00` 〜 `2021-12-31 23:59:59 UTC`、生M1 `2,608,784` 行 / 全 `1,177` 営業日 / 主力コホート `PURE_STRONG` $n=360$）
- **Holdout Protection**: Out-of-Sample（`2022-01-01 00:00:00 UTC` 以降、`1,783,913` 行） **未開封ロック継続中（`oos_locked: true`）** — 初回一発検証（One-Shot OOS Evaluation）は中村さん／総監督の最終承認後のみ実施
- **Local Git Canonical Path**: `C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery\00_Project_Control\GSR-2026W48_decision.md`
- **Google Drive Mirror Path**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理\GSR-2026W48_decision.md`

---

## 0. 公式TRACE記録ブロック

```text
🏷️ [TRACE: GSR-202611-W4-FRI | 採用候補（PASS_CANDIDATE：IS全5ゲート完全合格・One-Shot OOS初回開封申請＆MQL4 1対1仕様確定） | GSR-2026W48（GSR-TKYFIX-002）第3工程 執行監査・週次総括・Git資産整理]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W48; GSR-202611-W4-WED; GSR-202611-W4-WED-SPARK; GSR-TKYFIX-002; GSR-TKYFIX-001; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md; QUANT_PYTHON_MASTER_CONTEXT.md (v2.2); GEMINI_DISCOVERY_TRACE_RULE.md; プログラム資産管理手順.txt; spark_audit_handover_manifest_gsr_2026w48.json
record_id: GSR-202611-W4-FRI
session_title: GSR-2026W48（GSR-TKYFIX-002）第3工程 執行監査・週次総括・Git資産整理
case_id: GSR-202611-W4-FRI
parent_case_id: GSR-2026W48
decision: 採用候補
target_market: USDJPY_M1 (BO_STANDARD / Tokyo Fixing 09:55 JST 5-min expiry)
attachment_file: GSR-2026W48_decision.md, GSR-202611-W4-FRI_Stage3_Executive_Audit_and_Next_Week_Handover.md, git_commit_gsr_2026w48.ps1, INDEX.md
part_info: 1/1
timestamp: 2026-11-20 05:37:09 JST
-->
所属プロジェクト: BO・EA Edge Discovery / Gemini側必勝調査報告 (edge-discovery)
TRACE区分: BOEA
専用案件コード: GSR-202611-W4-FRI（親案件: GSR-2026W48 / 合格候補: GSR-TKYFIX-002）
参照元: GSR-202611-W4-WED-SPARK.md、spark_audit_handover_manifest_gsr_2026w48.json、is_standalone_and_ablation_summary_gsr_2026w48.csv、is_non_cumulative_marginals_and_yearly_gsr_2026w48.csv

【最終決定要旨】
- 判定: 採用候補（PASS_CANDIDATE — 本プロジェクト初のIS全5ゲート完全合格）
- 最終5ゲート結果: Gate 1[PASS] / Gate 2[PASS: +0.1p WR 60.56%, CLB97.5% +0.0222 > 0; +0.2p WR 59.72%, CLB97.5% +0.0057 > 0] / Gate 3[PASS: 非累積3区間すべて+0.3pまでBE超過] / Gate 4[PASS: Spark独立監査PASS、対NONE増分+6.98%pt] / Gate 5[PASS: 値幅中央値+0.75p、+0.3p WR 58.06%]
- OOS保護状態: 2022–2026年OOS（1,783,913行）は現在も未開封ロック（oos_locked: true）。次週One-Shot OOS一発検証はPURE_STRONG全体（両方向・事後フィルタ追加厳禁）を一次評価契約とし、SELL vs BUY方向別内訳を事前登録済み副次診断として実施。
<!-- RESEARCH_TRACE_END -->
```

---

## 1. 最終5ゲート合否判定テーブル（`GSR-TKYFIX-002` — 2026-11-20 確定）

| ゲート項目 | 審査基準（`QUANT_PYTHON_MASTER_CONTEXT.md` v2.2 / `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md`） | `GSR-TKYFIX-002`（`PURE_STRONG`: `wick >= 0.25`, $n=360$）実測結果 | 判定 |
| :--- | :--- | :--- | :--- |
| **Gate 1**<br>機会台帳一致・連続性・OOS遮断 | SHA256完全一致、件数フロー一致、6分間M1連続性・OHLC矛盾ゼロ、`oos_locked: true` | 全正本資産のSHA256一致、1,177行保存則（`PURE_STRONG 360 + WEAK_SUB 201 + NONE 616 = 1,177`）、`unknown` 0件、`wick_rejection_ratio` 469ユニーク値（Proxyゼロ）、6分間連続率 `100.0%`、2022年以降OOS `1,783,913` 行物理遮断。 | **PASS** |
| **Gate 2**<br>HAC統計下限（`CLB_97.5% > 0`） | ペイアウト `1.85`（損益分岐 `54.054054%`）、同値 `LOSE`、Newey-West HAC（lag=5）片側97.5%信頼下限 $> 0$ | **`+0.1 pip`**: 勝率 **`60.5556%`**（218勝142敗）、$\text{EV} = +0.120278$、$\text{SE}_{\text{HAC}} = 0.050061$、**$\text{CLB}_{97.5\%} = +0.022160 > 0$**（$t = +2.4026$）。<br>**`+0.2 pip`**: 勝率 **`59.7222%`**（215勝145敗）、$\text{EV} = +0.104861$、**$\text{CLB}_{97.5\%} = +0.005748 > 0$**（小標本 $t_{0.975,359}$ 再検算でも `+0.005412 > 0`）。 | **PASS** |
| **Gate 3**<br>真のPlateau広さ（非累積Disjoint） | 累積不等号の重複・局所スパイクを排した非累積区間での高原安定性・単一年非依存 | `PURE_STRONG` 内の非累積3区間 `[0.25, 0.40)`（$n=97$: `+0.1p` `61.86%`, `+0.3p` `60.82%`）、`[0.40, 0.55)`（$n=135$: `+0.1p` `60.74%`, `+0.3p` `57.78%`）、`[0.55, 1.00]`（$n=128$: `+0.1p` `59.38%`, `+0.3p` `56.25%`）がすべて全摩擦水準でBE超過。最良年（2016年 `71.70%`）除外の6年間（$n=307$）でも勝率 `58.63%`（$\text{EV}=+0.0847$）を維持。 | **PASS** |
| **Gate 4**<br>Spark独立監査・選択バイアス排除 | Control群に対する正のアブレーション、年次・粗視化整合性、p-hacking・未来参照の不在 | Spark独立監査（`GSR-202611-W4-WED-SPARK`）にて `audit_verdict: PASS`。対 `NONE`（CONTROL `53.57%`）比 **`+6.98%pt`**（$\Delta\text{EV}=+0.1292$）、除外した `WEAK_SUB`（`49.75%`）比 **`+10.80%pt`** の正のアブレーションを実証。7年中5年黒字・2年微損（2017年 `52.38%`, 2020年 `53.97%`）、崩壊年ゼロ。 | **PASS** |
| **Gate 5**<br>MT4執行・微細摩擦ストレス耐性 | `Open[t+1]` 参入、`Open[t+6]` 厳密5分満期、`+0.1〜+0.3 pip` 摩擦での生残性と順行中央値 | 順行値幅中央値 **`+0.75 pips`**（従来棄却群 `0.0〜0.1 pip` の7.5倍）。`+0.1p` `60.56%` / `+0.2p` `59.72%` / **`+0.3p` `58.06%`**（209勝151敗, $\text{EV}=+0.0740$）と全摩擦水準で損益分岐を超過。 | **PASS** |

---

## 2. One-Shot OOS 初回開封・一発検証契約（2022-01-01 〜 2026-10-16）

本決定書および中村さん／総監督の最終承認をもって解禁される **One-Shot OOS Evaluation（一発検証）** の不変契約は以下の通りとする（事後カーブフィッティング厳禁）：

1. **一次評価契約（Primary Contract — 変更厳禁）**:
   - 対象：`PURE_STRONG` 全体（`wick_rejection_ratio >= 0.25`、**`SELL`・`BUY` 両方向合算**）。
   - 禁止事項：IS監査で見つかった「BUY側の弱さ（`+0.2p` 勝率 `52.94%`）」「Move 2.6〜3.5 ATR の窪地（`52.75%`）」「木曜日の微割れ（`53.75%`）」を理由に、OOS開封前に条件を後付けで追加・除外することを一切禁ずる。
   - OOS合格基準：`+0.1 pip` および `+0.2 pip` 負荷において損益分岐（`54.054%`）を超過し、かつ順行値幅中央値が `+0.40 pip` 以上を維持すること（望ましくは `+0.1p` で $\text{CLB}_{97.5\%} > 0$）。
2. **事前登録済み副次診断（Pre-Registered Diagnostic Breakdown）**:
   - 一次判定に影響させない診断出力として、①売買方向別（`SELL` vs `BUY`）、②ゴトー日区分（`gotobi_1` vs `gotobi_0`）、③年次別（2022 / 2023 / 2024 / 2025 / 2026）の内訳を併記する。
3. **OOS消費規定**:
   - OOS期間を1度でも開封して結果を確認した後、その結果をもとにパラメータや方向フィルタを変更した場合は、当該2022–2026区間は「探索済み（`VIEWED_EVAL`）」へ降格し、実運用採用には別期間の完全未使用データまたはフォワードデモ検証を要求する。

---

## 3. Champ / Codex 実装引き継ぎ：Python検証コード ⇔ MQL4 1対1対応仕様書（`BO_USDJPY_TKYFIX002_5M_v1.0.mq4`）

※本仕様書は IS 全5ゲート合格に基づく **事前凍結実装仕様** であり、実弾投入は One-Shot OOS 合格および MT4 ストラテジーテスター実Tick監査完了後とする。

| 処理フェーズ | Python検証コード正本（ファイル名・行番号） | Python実装ロジック（実測確定済み） | MQL4実装 1対1対応仕様（`shift >= 1` 確定足・厳密300秒満期・連打防止） |
| :--- | :--- | :--- | :--- |
| **1. 対象銘柄・時間足・Point換算** | `gsr_2026w48_is_tkyfix002_verifier_v1_0.py`<br>L40–L44 | `SYMBOL = "USDJPY"`, `PIP_SIZE = 0.01`, `PAYOUT = 0.85` | `Symbol() == "USDJPY"`（サフィックス対応）、`Period() == PERIOD_M1`。`double pipSize = (Digits == 3 \|\| Digits == 5) ? Point * 10.0 : Point;`（USDJPY 3桁で `0.01`）。 |
| **2. サーバー時刻 ⇔ UTC/JST 変換＆新足確定検知** | `profile_is_market_structure_gsr_2026w48_v1_0.py`<br>L23–L24, L30 | `w15 = 00:40..00:54 UTC`, `entry = 00:55 UTC (09:55 JST)`, `expiry = 01:00 UTC (10:00 JST)` | `OnTick()` 冒頭で `static datetime lastBarTime = 0; if(Time[0] == lastBarTime) return; lastBarTime = Time[0];` により **M1新足始値（`Open[0]` = `Open[t+1]`）の初回ティックでのみ判定**。`TimeGMT()`（夏時間自動追従・ブローカーUTCオフセット非依存）で `TimeHour(gmtNow) == 0 && TimeMinute(gmtNow) == 55` の時のみ発火。 |
| **3. 6分間バー連続性・欠損ガード（Gate 1）** | `profile_is_market_structure_gsr_2026w48_v1_0.py`<br>L36–L39, L50 | `00:40..00:54 UTC` の15本確定足と `00:55 UTC` 始値の存在確認 | 確定足 `shift = 1` が `00:54 UTC`（`Time[0] - Time[1] == 60`）、かつ `shift = 15` が `00:40 UTC`（`Time[1] - Time[15] == 840`）であることを厳密照合。欠損バーがあれば即見送り（`return;`）。 |
| **4. 仲値直前15分間の値幅・方向・ATR14算出** | `profile_is_market_structure_gsr_2026w48_v1_0.py`<br>L39–L42, L50 | `bod15 = abs(Close[00:54] - Open[00:40]) / 0.01`<br>`atr14 = mean((High - Low)/0.01 for 00:41..00:54)`<br>`mv = bod15 / atr14 >= 1.5` | **必ず `shift >= 1` の確定足のみ参照**：<br>`double open40 = Open[15]; double close54 = Close[1];`<br>`double bod15 = MathAbs(close54 - open40) / pipSize;`<br>`double sumRng = 0.0; for(int i = 1; i <= 14; i++) sumRng += (High[i] - Low[i]) / pipSize;`<br>`double atr14 = sumRng / 14.0;`<br>`if(atr14 <= 1e-9 \|\| (bod15 / atr14) < 1.5) return;`<br>`int dir = (close54 > open40) ? OP_SELL : OP_BUY;`（15分急伸なら `SELL`、急落なら `BUY`）。 |
| **5. 09:54確定足 純粋ヒゲ拒絶比率（TRAP-06排除）** | `profile_is_market_structure_gsr_2026w48_v1_0.py`<br>L43–L46 | `r54 = High[00:54] - Low[00:54]`<br>`SELL`: `(High - max(O,C)) / r54`<br>`BUY`: `(min(O,C) - Low) / r54`<br>`PURE_STRONG`: `wk >= 0.25` | `double r54 = High[1] - Low[1]; if(r54 <= 1e-9) return;`<br>`double wk = (dir == OP_SELL) ? (High[1] - MathMax(Open[1], Close[1])) / r54 : (MathMin(Open[1], Close[1]) - Low[1]) / r54;`<br>`if(wk < 0.25 - 1e-9) return;`（**OR条件・弱ヒゲ層は完全排除**）。 |
| **6. 1日1回単発ロック＆BO連打防止・スプレッド上限** | `profile_is_market_structure_gsr_2026w48_v1_0.py`<br>L33（1営業日1行） | 1日1回単発・マーチン厳禁・最大摩擦耐性 `+0.3 pip` 確認済み | `static int lastTradeDay = -1; int today = TimeYear(gmtNow)*10000 + TimeMonth(gmtNow)*100 + TimeDay(gmtNow); if(today == lastTradeDay) return;`<br>さらに現在スプレッドチェック：`double curSpreadPips = (Ask - Bid) / pipSize; if(curSpreadPips > InpMaxSpreadPips) return;`（既定 `InpMaxSpreadPips = 0.3`）。発注成功時に `lastTradeDay = today;` を記録し同日再参入・同時保有を物理遮断。 |
| **7. 厳密5分満期判定（6分バグ TRAP-04 根絶）** | `gsr_2026w48_is_tkyfix002_verifier_v1_0.py`<br>L108, L123–L125 | `Open[00:55 UTC]` 参入 ➔ `Open[01:00 UTC]`（厳密300秒後）満期、同値 `LOSE` | **旧バグ `barsPassed > 5`（実質6分満期）を絶対禁止**。BOバックテスト用内部決済では `if(TimeCurrent() >= entryTime + 300)`（または `Time[0] >= entryBarTime + 300` の初回ティック `Open[0]`）で厳密300秒満期判定を実行し、`signedMove <= 0`（同値含む）はすべて `LOSE` として記録する。 |
| **8. FX拡張時のリスク計算（参考仕様）** | `QUANT_PYTHON_MASTER_CONTEXT.md` v2.2 | BOは固定単発ベット（マーチン厳禁）。FX拡張時は1トレード1.0%リスク正規化 | 本案件は `BO_STANDARD` 固定ベット（`InpFixedBet`）が一次仕様。将来 `EA_FX` へ移植する場合のみ `AccountBalance() * 0.01 / (slPips * tickValuePerPip)` による1%リスクロット計算と同一足SL/TP同時到達時の「SL先行判定」を適用する。 |
