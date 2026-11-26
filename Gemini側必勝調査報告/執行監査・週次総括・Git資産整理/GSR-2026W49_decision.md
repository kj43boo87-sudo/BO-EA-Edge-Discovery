# GSR-2026W49 Decision Record — Track A（GSR-TKYFIX-002 One-Shot OOS）正式棄却（REJECTED）＆ Track B（マルチ・フィキシングIS探索）5ゲート裁定書

- **Pipeline Case ID**: `GSR-2026W49`（第3工程レコードID: `GSR-202611-W5-FRI` / 親ライン: `Gemini側必勝調査報告`）
- **Decision Date**: `2026-11-27 JST`
- **Upstream References**:
  - 第1工程：`HANDOVER_GSR_2026W49_STAGE1.md` / `stage1_to_stage2_handover_manifest_gsr_2026w49.json`（`LOCAL_FULL_775MB_VERIFIED`）
  - 第2工程：`GSR-2026W49_Stage2_OOS_and_MultiFix_Report.md` / `spark_audit_handover_manifest_gsr_2026w49.json`（`2026-11-26 05:04:58 JST`、`LOCAL_775MB_FULL_VERIFIED`）
  - Spark独立性能監査：`GSR-202611-W5-WED-SPARK` — **`unknown`（未発行・Drive未検出）**
- **Local Git Canonical Path**: `C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery\00_Project_Control\GSR-2026W49_decision.md`
- **Google Drive Mirror Path**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理\GSR-2026W49_decision.md`

---

## 0. 公式TRACE記録ブロック

```text
🏷️ [TRACE: GSR-202611-W5-FRI | 正式棄却・開発凍結 (GSR-TKYFIX-002 OOS, GSR-LDNFIX-001, GSR-NYCUT-001) / 保留・Spark監査待ち (GSR-TKYFIX-003) | GSR-2026W49 第3工程 執行監査・週次総括・Git資産整理]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W49; GSR-2026W48; GSR-202611-W5-WED; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md; spark_audit_handover_manifest_gsr_2026w49.json
record_id: GSR-202611-W5-FRI
session_title: GSR-2026W49 第3工程 執行監査・週次総括・Git資産整理
case_id: GSR-202611-W5-FRI
decision: REJECTED (Track A GSR-TKYFIX-002, GSR-LDNFIX-001, GSR-NYCUT-001) / HOLD (GSR-TKYFIX-003)
oos_locked: true (Track B) / completed_one_shot (Track A GSR-TKYFIX-002)
-->
```

---

## 1. 案件別 最終5ゲート合否判定サマリー

| トラック / 候補ID | 対象市場・時間枠 | G1 | G2 | G3 | G4 | G5 | 最終裁定 | 次工程処置 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Track A: `GSR-TKYFIX-002`（One-Shot OOS）** | USDJPY M1 09:55 JST（2022–2026, $n=256$） | **PASS** | **FAIL** | **FAIL** | **FAIL** | **FAIL** | **正式棄却（`REJECTED`）** | **永久凍結（事後SELL専業化などOOS再開封・延命厳禁）** |
| **Track B: `GSR-NYCUT-001`** | EURUSD ($n=392$) / USDJPY ($n=399$) NY 10:00（IS） | **PASS** | **FAIL** | **FAIL** | **FAIL** | **FAIL** | **正式棄却（`REJECTED`）** | **永久凍結・OOS未開封ロック維持** |
| **Track B: `GSR-LDNFIX-001`** | EURUSD ($n=420$) / GBPUSD ($n=462$) LDN 16:00（IS） | **PASS** | **FAIL** | **FAIL** | **FAIL** | **FAIL** | **正式棄却（`REJECTED`）** | **ヒゲ拒絶モデルは凍結（`ALL_POOLED/NONE`無条件逆張りは別案件候補）** |
| **Track B: `GSR-TKYFIX-003`** | USDJPY M1 09:55 JST（IS, $n=359$, $\phi_{	ext{urp}}$ 分解） | **PASS** | **PASS** | **PASS** | `unknown` | **PASS** | **保留（`HOLD`）** | **Spark独立監査待ち・`phi_urp <= 0.598` IS事前固定検証へ** |

---

## 2. Track A：`GSR-TKYFIX-002` One-Shot OOS 初回開封裁定根拠（`REJECTED`）

1. **Gate 1（PASS）**:
   - ガバナンス正本（`0caca9b9...`）、第1工程スクリプト（`f4609b51...`）、Track A OOS台帳（`3e5c583f...`, 774行: `PURE_STRONG` 256 + `NONE` 428 + `WEAK_SUB` 90, 除外3件）、生M1 3通貨計775MBのSHA256完全一致を確認。
2. **Gate 2・Gate 3・Gate 4・Gate 5（すべて FAIL）**:
   - **一次評価主契約（`PURE_STRONG` 両方向合算, $n=256$）**:
     - `+0.1p` 勝率 **`55.0781%`**（141勝115敗, $	ext{EV} = +0.018945$, $	ext{SE}_{	ext{HAC}} = 0.059177$）、**$	ext{CLB}_{97.5\%} = -0.097040$（正規） / $-0.097593$（$t$）**（$t = +0.3201$）であり、Gate 2 基準（$	ext{CLB}_{97.5\%} > 0$）を不通過。
     - **`+0.2p` 勝率 `53.1250%`**（< 損益分岐 `54.0541%`, $	ext{EV} = -0.017188$）、**`+0.3p` 勝率 `52.7344%`**（$	ext{EV} = -0.024414$）で Gate 5 摩擦耐性を喪失。
     - **対 Control 逆転（Gate 4 FAIL）**: `NONE`（$n=428$）が `+0.1p` 勝率 `59.5794%`（$	ext{CLB}_{97.5\%} = +0.017169 > 0$）を記録したのに対し、`PURE_STRONG` は **`-4.5013%pt`**（$\Delta	ext{EV} = -0.083275$）劣後。
     - **実運用資金シミュレーション（初期50,000円 / 固定1,000円）**: `+0.1p` 最大DD **`34.8172%`**（上限25%超過）、`+0.2p` 純損益 **`-4,400円`**（最大DD `46.3682%`）。
   - **Covariate Shift（IS vs OOS 構造変化）**: OOS期間の `atr14_pips` 中央値は `3.175p`（IS `1.8286p` の **1.7363倍**）、`pre_15m_range_pips` は `15.4p`（IS `9.4p` の **1.6383倍**）へ拡大。
   - **事前登録済み副次診断の記録（事後改変は禁止）**:
     - `SELL`（$n=113$）は `+0.1p` **`65.4867%`**（$	ext{EV}=+0.211504$, $	ext{CLB}_{97.5\%,t}=+0.064081 > 0$）、`+0.2p`/`+0.3p` **`62.8319%`**（$	ext{CLB}_{97.5\%,t}=+0.010017 > 0$）、順行中央値 `+1.4p` と強固であった一方、`BUY`（$n=143$）は `+0.1p` **`46.8531%`**（$	ext{EV}=-0.133217$, 順行中央値 `-0.4p`）へ崩壊。
     - `GSR-TKYFIX-002`（両方向契約）自体はここで **正式棄却（`REJECTED`）** と確定し、OOS結果を見た上での後付け `SELL` 専業化は禁止する。

---

## 3. Track B：マルチ・フィキシング IS探索裁定根拠（`oos_locked: true`）

1. **`GSR-NYCUT-001`（EURUSD / USDJPY, NY 10:00 カット） — `REJECTED`**:
   - `EURUSD` `PURE_STRONG`（$n=392$）: `+0.1p` `48.2143%`（$	ext{EV}=-0.108036$, 対NONE `-5.2688%pt`）。
   - `USDJPY` `PURE_STRONG`（$n=399$）: `+0.1p` `47.3684%`（$	ext{EV}=-0.123684$, 対NONE `-5.2758%pt`）。
2. **`GSR-LDNFIX-001`（EURUSD / GBPUSD, ロンドン 16:00 フィキシング） — `REJECTED`**:
   - `EURUSD` `PURE_STRONG`（$n=420$）: `+0.1p` `58.5714%`（$	ext{CLB}_{97.5\%,t}=-0.016274 < 0$、対NONE **`-4.2089%pt`**）。`BST`（`62.8571%`）と `GMT`（`52.5714%`）の乖離も大きく、ヒゲ拒絶条件は負の増分。
   - `GBPUSD` `PURE_STRONG`（$n=462$）: `+0.1p` `58.6580%`（$	ext{CLB}_{97.5\%,t}=+0.008275 > 0$）だが `+0.2p` で $	ext{CLB}$ マイナス転落（`-0.006655`）、対NONE **`-1.4787%pt`**。
   - ※一方、ヒゲ条件を課さない `ALL_POOLED` / `NONE`（EURUSD `60.78%` / `62.78%`, GBPUSD `59.29%` / `60.14%`）は強い基礎優位性を示しており、別仮説 `GSR-LDNFIX-002` としてISから再設計する余地がある。
3. **`GSR-TKYFIX-003`（USDJPY, 東京仲値 09:55 JST 幾何特徴量） — `HOLD`（Spark独立監査待ち）**:
   - `PURE_STRONG`（$n=359$）: `+0.1p` `60.4457%`（$	ext{CLB}_{97.5\%,t}=+0.020013 > 0$）、`+0.2p` `59.6100%`（$	ext{CLB}_{97.5\%,t}=+0.003567 > 0$）、`+0.3p` `57.9387%`。
   - `PURE_STRONG` 内の非累積 $\phi_{	ext{urp}}$（未解決押し戻しポテンシャル）4分位では、`Q1`（$n=90$: **`65.56%`**, CLB `+0.0522`）、`Q2`（$n=90$: **`65.56%`**, CLB `+0.0606`）、`Q3`（$n=89$: **`61.80%`**）に対し、`Q4 (0.598, 0.991]`（$n=90$）のみ **`48.8889%`**（$	ext{EV}=-0.095556$）へ急落する構造を検出。
   - 現時点で `GSR-202611-W5-WED-SPARK` が未発行（`unknown`）のため Gate 4 を `unknown` とし、正式裁定は **`HOLD`（OOS完全ロック継続）** とする。

---

## 4. Champ / Codex MQL4実装引き継ぎステータス

- 本週は 5ゲート全通過案件が **0件**（Track A `GSR-TKYFIX-002` はOOS棄却、`GSR-TKYFIX-003` は `HOLD`）のため、MQL4実装（`.mq4` / `.ex4` コンパイル）への移行は **凍結（見送り）** とする。
