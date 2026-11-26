# GSR-2026W49 Decision Record — 総監督最終裁定書（GSR-TKYFIX-002・GSR-NYCUT-001 永久凍結／GSR-LDNFIX-002 次週W50最優先昇格）

- **Pipeline Case ID**: `GSR-2026W49`（第3工程レコードID: `GSR-202611-W5-FRI` / 親ライン: `Gemini側必勝調査報告`）
- **Governance**: `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md`（SHA256: `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9`）
- **Decision Date**: `2026-11-27 JST`
- **Upstream Canonical Audit**:
  - 第1工程：`profile_market_structure_gsr_2026w49_v1_0.py`（v1.0.2, SHA256: `f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b`）
  - 第2工程：`gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py`（SHA256: `2b9c5017abd9f723536f05bd4f362888642af6b9cc53e0e107a412407a9ca479`） / `spark_audit_handover_manifest_gsr_2026w49.json`（`2026-11-26 05:04:58 JST`, `LOCAL_775MB_FULL_VERIFIED`, 25,846 B, SHA256: `e50c86b03a3acd954175101297495378e3e541352a909b1b7d5e3ff87aed5354`）
  - 独立性能監査：Aegis（Spark）`GSR-202611-W5-WED-SPARK` 完了済み
- **OOS保護契約**:
  - Track A（`GSR-TKYFIX-002` USDJPY 09:55 JST 2022–2026）: One-Shot OOS 開封完了・正式棄却（再開封・事後救済厳禁）
  - **EURUSD / GBPUSD（2022-01-01以降）**: **完全未開封ロック厳守（`oos_locked: true`）**
- **Local Git Canonical Path**: `C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery\00_Project_Control\GSR-2026W49_decision.md`

---

## 0. 公式TRACE記録ブロック

```text
🏷️ [TRACE: GSR-202611-W5-FRI | 正式棄却・永久凍結 (GSR-TKYFIX-002, GSR-NYCUT-001) / 保留・設計転換 (GSR-LDNFIX-001 -> GSR-LDNFIX-002 最優先昇格, GSR-TKYFIX-003 低優先待機) | GSR-2026W49 総監督確定裁定]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W49; GSR-2026W48; GSR-202611-W5-WED; GSR-202611-W5-WED-SPARK; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md; spark_audit_handover_manifest_gsr_2026w49.json
record_id: GSR-202611-W5-FRI
session_title: GSR-2026W49 総監督最終裁定書（GSR-2026W49_decision.md）
case_id: GSR-202611-W5-FRI
decision: FAIL (GSR-TKYFIX-002, GSR-NYCUT-001) / HOLD (GSR-LDNFIX-001 -> GSR-LDNFIX-002, GSR-TKYFIX-003)
oos_locked: true (EURUSD & GBPUSD 2022+)
-->
```

---

## 1. 案件別 最終5ゲート合否判定および総監督確定裁定

| 候補ID | トラック / 対象・期間 | G1 | G2 | G3 | G4 | G5 | 最終裁定 | 工学・次工程処置 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **`GSR-TKYFIX-002`** | Track A: USDJPY M1 09:55 JST One-Shot OOS (2022–2026, $n=256$) | **PASS** | **FAIL** | **FAIL** | **FAIL** | **FAIL** | **`FAIL`（正式棄却・永久凍結）** | **`GSR_TKYFIX_002.mq4` 実装中止・アーカイブ凍結（未作成のまま終了）** |
| **`GSR-NYCUT-001`** | Track B: EURUSD ($n=392$) / USDJPY ($n=399$) NY 10:00 IS (2015–2021) | **PASS** | **FAIL** | **FAIL** | **FAIL** | **FAIL** | **`FAIL`（即時棄却・永久凍結）** | 全コホート赤字・TRAP-05摩擦崩壊により永久凍結 |
| **`GSR-LDNFIX-001`** | Track B: EURUSD ($n=1,127$) / GBPUSD ($n=1,157$) LDN 16:00 IS (2015–2021) | **PASS** | **PASS**（ALL/NONE） | **HOLD** | **FAIL**（ヒゲ逆効果） | **PASS**（ALL/NONE） | **`HOLD`（設計転換・W50最優先昇格）** | ヒゲ撤廃し無フィルター契約 **`GSR-LDNFIX-002`** へ昇格（**EURUSD/GBPUSD OOS完全ロック厳守**） |
| **`GSR-TKYFIX-003`** | Track B: USDJPY M1 09:55 JST 次世代幾何モデル IS (2015–2021, $n=359$) | **PASS** | **PASS** | **PASS** | **HOLD**（OOS既閲覧） | **PASS** | **`HOLD`（低優先度・フォワード専用待機）** | TRAP-01実証済みだがUSDJPY 09:55 OOS既閲覧のため待機 |

---

## 2. 各候補の詳細裁定根拠（`LOCAL_775MB_FULL_VERIFIED` 確定値）

### 2.1 `GSR-TKYFIX-002`（Track A One-Shot OOS）➔ `FAIL`（正式棄却・永久凍結）
- **一次評価主契約（`PURE_STRONG` 両方向合算, $n=256$）**:
  - `+0.1p`: 勝率 **`55.0781%`**（141勝115敗）, $	ext{EV}=+0.018945$, $	ext{CLB}_{97.5\%}=-0.097040$（正規） / **$-0.097593$**（$t$分布, $t=+0.3201$）➔ Gate 2 FAIL。
  - `+0.2p`: 勝率 **`53.1250%`**（損益分岐 `54.0541%` 割れ, $	ext{EV}=-0.017188$）、`+0.3p`: **`52.7344%`**（$	ext{EV}=-0.024414$）➔ Gate 5 FAIL。
  - **逆アブレーション**: 対照群 `NONE`（$n=428$, `+0.1p` `59.5794%`, $	ext{CLB}_{97.5\%,t}=+0.017169$）に対し **`-4.5013%pt`** 劣後 ➔ Gate 4 FAIL。
  - **資金シミュレーション（初期50,000円・固定1,000円・マーチンなし）**: `+0.1p` 最大DD **`34.82%`**（21,900円）、`+0.2p` 最大DD **`46.37%`**（27,450円, 純損益 `-4,400円`）といずれも上限 `25.0%` を大幅超過。
  - **Covariate Shift**: OOS期間の `atr14_pips` 中央値 `3.175p`（IS `1.8286p` の **1.7363倍**）、`pre_15m_range_pips` `15.4p`（IS `9.4p` の **1.6383倍**）。
- **事前登録済み副次診断と規律遵守**:
  - `SELL`（$n=113$: `+0.1p` **`65.49%`**, $	ext{CLB}=+0.0657$, `+0.3p` **`62.83%`**, 中央値 `+1.40p`）対 `BUY`（$n=143$: `+0.1p` **`46.85%`**, 中央値 **`-0.40p`**）の極端な非対称性を確認したが、One-Shot OOS規律により事後救済（後付け `SELL` 専業化）を厳禁とし、永久凍結とする。
- **工学ステータス**: **`GSR_TKYFIX_002.mq4` は実装中止・アーカイブ凍結（未作成のまま終了）**。

### 2.2 `GSR-NYCUT-001`（Track B IS）➔ `FAIL`（即時棄却・永久凍結）
- **EURUSD**: `ALL_POOLED`（$n=1,048$）`+0.1p` `50.86%`、`PURE_STRONG`（$n=392$）`48.21%`（$	ext{EV}=-0.1080$, 中央値 `0.00p`, 対 `NONE` `-5.27%pt`）。
- **USDJPY**: `ALL_POOLED`（$n=1,027$）`+0.1p` `49.76%`、`PURE_STRONG`（$n=399$）`47.37%`（$	ext{EV}=-0.1237$, 中央値 `-0.20p`, 対 `NONE` `-5.28%pt`）。
- 全コホート赤字・逆アブレーション・摩擦崩壊（`TRAP-05`）により即時永久凍結（OOS未開封ロック維持）。

### 2.3 `GSR-LDNFIX-001`（Track B IS）➔ `HOLD`（`GSR-LDNFIX-002` へ設計転換・W50最優先昇格）
- **圧倒的ベースライン優位性**:
  - **EURUSD**: `ALL_POOLED`（$n=1,127$）`+0.1p` **`60.78%`**（$	ext{CLB}=+0.0702, t=+4.50$）、`+0.3p` **`57.85%`**（$	ext{CLB}=+0.0167 > 0$）、中央値 `+1.10p` ／ `NONE`（$n=446$）`+0.1p` **`62.78%`**（`+0.3p` `60.54%`, 中央値 `+1.40p`）。
  - **GBPUSD**: `ALL_POOLED`（$n=1,157$）`+0.1p` **`59.29%`**（$	ext{CLB}=+0.0432, t=+3.54$）、`+0.3p` **`58.08%`**（$	ext{CLB}=+0.0208 > 0$）、中央値 `+1.30p` ／ `NONE`（$n=439$）`+0.1p` **`60.14%`**（`+0.3p` `59.45%`, 中央値 `+1.50p`）。
- **設計転換理由**: 東京仲値由来のヒゲフィルター（`PURE_STRONG`）は両通貨で逆アブレーション（EURUSD `-4.21%pt`, GBPUSD `-1.48%pt`）を起こすため撤廃し、次週 `GSR-2026W50` にて無フィルター・ベースライン契約 **`GSR-LDNFIX-002`** のIS完全検証（非累積分解・DST/方向/年次安定性・IS資金DD $\le 25\%$）を最優先で実施する。
- **OOSロック厳命**: **EURUSD / GBPUSD の 2022-01-01 以降 OOS データは完全未開封ロック（`oos_locked: true`）を厳守**。

### 2.4 `GSR-TKYFIX-003`（Track B IS）➔ `HOLD`（低優先度・フォワード専用待機）
- `PURE_STRONG`（$n=359$）内の非累積 $\Phi_{	ext{URP}}$ 4分位で `Q1` `65.56%` / `Q2` `65.56%` / `Q3` `61.80%` に対し **`Q4 (0.598, 0.991]` のみ `48.89%`** へ崩壊することを実証（`TRAP-01`: エネルギー消費済み層の特定）。
- ただし USDJPY 09:55 JST の 2022–2026 データは Track A で既閲覧のため純粋OOS検証が成立しない。よって低優先度・フォワード専用待機とし、W50のリソースを `GSR-LDNFIX-002` へ集中する。

---

## 3. 永久凍結・再検証禁止リスト（Permanent Exclusion List — W49更新）
- `GSR-CLIMAX-001` / `GSR-PULLBACK-001` / `GSR-FAKEOUT-001` / `GSR-SURVEY-001` / `BO-EUR-004` / `BO-EUR-005`（W46以前）
- `GSR-EXHAUST-001` / `GSR-SHOCKDECAY-001`（W47）
- `GSR-TKYFIX-001` の `WEAK_SUB`（$0 \le 	ext{wick} < 0.25$, `TRAP-06`）
- **`GSR-TKYFIX-002`（Track A One-Shot OOS 棄却・`GSR_TKYFIX_002.mq4` 実装中止・アーカイブ凍結）**
- **`GSR-NYCUT-001`（EURUSD / USDJPY NYカット逆張り・`TRAP-05` 永久凍結）**
