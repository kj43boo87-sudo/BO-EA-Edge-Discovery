🏷️ [TRACE: GSR-202611-W5-WED | 保留（Gate 1全8ファイルSHA256・母数保存則・Covariate Shift実測完了／Track A One-Shot OOSおよびTrack B IS勝敗は775MB生M1のローカル実行で最終確定） | GSR-2026W49 第2工程：GSR-TKYFIX-002 One-Shot OOS初回開封決戦（Track A）＆マルチ・フィキシングIS検証（Track B）]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W49; GSR-2026W48; GSR-202611-W4-FRI; GSR-TKYFIX-002; GSR-TKYFIX-003; GSR-LDNFIX-001; GSR-NYCUT-001; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md; stage1_to_stage2_handover_manifest_gsr_2026w49.json; oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv; is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv; exclusions_log_gsr_2026w49.csv; gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py; spark_audit_handover_manifest_gsr_2026w49.json
record_id: GSR-202611-W5-WED
session_title: GSR-2026W49 第2工程：GSR-TKYFIX-002 One-Shot OOS初回開封決戦（Track A）＆マルチ・フィキシングIS検証（Track B）
case_id: GSR-202611-W5-WED
parent_case_id: GSR-2026W49
decision: 保留
target_market: USDJPY_M1 / EURUSD_M1 / GBPUSD_M1 (BO_STANDARD / 5-min expiry)
attachment_file: gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py, GSR-2026W49_Stage2_OOS_and_MultiFix_Report.md, oos_tkyfix002_standalone_and_diagnostics_gsr_2026w49.csv, is_multifix_standalone_and_ablation_gsr_2026w49.csv, is_multifix_disjoint_slices_and_yearly_gsr_2026w49.csv, spark_audit_handover_manifest_gsr_2026w49.json, INDEX.md
part_info: 1/1
timestamp: 2026-11-25 05:50:00 JST
-->

# GSR-2026W49 第2工程：Track A（`GSR-TKYFIX-002` One-Shot OOS初回開封決戦）＆ Track B（マルチ・フィキシングIS統計・非累積検証）レポート

## 0. v1.2 内部自問自答ゲート（Pre-Ruling Self-Audit）

1. **【自問1：追認バイアス・擬似プラトーの自問】**: `CLEAR` — クラウドAPIの10MB取得制限により3通貨計775MBの生M1 CSV全量をクラウド上で直接読み込めないため、推測値・定数・部分スニペットによる合否判定は一切行わず、勝敗・EV・HAC $\text{CLB}_{97.5\%}$（正規 $z$ ＆ $t$分布）は `unknown` と明記した。ローカル実行スクリプト `gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py` では累積不等号を禁止し、非累積（Disjoint）4分位・3区間のみで評価する契約を固定済み。
2. **【自問2：データ汚染・執行契約の自問】**: `CLEAR` — Track B の `is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv` は `expected_entry_utc` 最大値 `2021-12-31 16:00:00` であり、検証スクリプト内でも `allow_oos=False` により2022年以降を物理遮断（`oos_locked_for_track_b: true`）。また `GSR-NYCUT-001|USDJPY` の `FAIL_GAP_T+6` 1件（`2015-02-04`）を評価から除外し、5,532件の完全6本連続行のみを評価する。Track A（`GSR-TKYFIX-002`）は事前承認済みOne-Shot OOS契約のみに限定。
3. **【自問3：差配契約の曖昧さ検閲】**: `CLEAR` — Track A の一次評価主契約は `PURE_STRONG`（$n=256$, 両方向合算）に単独固定し、副次診断（方向・ゴトー日・曜日・ATR・年次・ヒゲ3区間）による事後差し替えを禁止。

---

## 1. Gate 1 審査：確定8ファイル SHA256完全照合および母数保存則（`PASS`）

| # | ファイル種別 | ファイル名 | 確定SHA256（指定正本値） | 第2工程検算SHA256 | サイズ / 行数 | 判定 |
|---:|:---|:---|:---|:---|:---|:---|
| 1 | ガバナンス正本 (v1.2) | `MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md` | `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9` | `0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9` | 6,107 B | **EXACT MATCH** |
| 2 | 第1工程スクリプト | `profile_market_structure_gsr_2026w49_v1_0.py` (v1.0.2) | `f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b` | `f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b` | 29,573 B | **EXACT MATCH** |
| 3 | Track A OOS台帳 | `oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv` | `3e5c583f8b8bb5bef00846c2048c90716cb01f071d2591b65998549359758d68` | `3e5c583f8b8bb5bef00846c2048c90716cb01f071d2591b65998549359758d68` | 214,232 B / 774行 | **EXACT MATCH** |
| 4 | Track B IS台帳 | `is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv` | `0272871721a3e96b6ace75afaa72e13708c8d398355a2cc971459d8cdec1a1c1` | `0272871721a3e96b6ace75afaa72e13708c8d398355a2cc971459d8cdec1a1c1` | 1,760,257 B / 5,533行 (PASS 5,532) | **EXACT MATCH** |
| 5 | 行単位除外ログ | `exclusions_log_gsr_2026w49.csv` | `951cd609d678ff05dc4a1b62daf398f0bd89966e80e8bcd29a130d835a149757` | `951cd609d678ff05dc4a1b62daf398f0bd89966e80e8bcd29a130d835a149757` | 6,342 B / 66行 | **EXACT MATCH** |
| 6 | 生M1原本 (USDJPY) | `2026.10.16USDJPY(3)-M1-No Session.csv` | `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29` | ローカル検証スクリプト冒頭で自動照合 | 258,871,846 B | **STAGE1 MATCH / LOCAL VERIFY** |
| 7 | 生M1原本 (EURUSD) | `2026.10.16EURUSD(5)-M1-No Session.csv` | `029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d` | ローカル検証スクリプト冒頭で自動照合 | 258,932,307 B | **STAGE1 MATCH / LOCAL VERIFY** |
| 8 | 生M1原本 (GBPUSD) | `2026.10.16GBPUSD(3)-M1-No Session.csv` | `05468aa45b7e08a47fa7aff608af1d08d190fd6b5298534585f9c9554e7ab803` | ローカル検証スクリプト冒頭で自動照合 | 258,199,124 B | **STAGE1 MATCH / LOCAL VERIFY** |

---

## 2. 【最優先：Track A】`GSR-TKYFIX-002` One-Shot OOS（2022–2026）事前構造＆Covariate Shift 実測診断

### 2.1 Covariate Shift 診断（IS `GSR-TKYFIX-003` 2015–2021 vs OOS `GSR-TKYFIX-002` 2022–2026 — クラウド100%実測完了）

| コホート区分 | 特徴量 | IS (2015–2021) 中央値 (IQR) | OOS (2022–2026) 中央値 (IQR) | OOS / IS 倍率 | レジームシフト診断 |
| :--- | :--- | ---: | ---: | ---: | :--- |
| **`PURE_STRONG`** (IS `359` vs OOS `256`) | **`atr14_pips`** | `1.8286p` (`1.0572p`) | **`3.1750p`** (`1.6893p`) | **`1.736x`** | **劇的な高ボラティリティ化（`atr14 >= 2.0p` 比率が `43.6% -> 82.4%` に急増）** |
| **`PURE_STRONG`** (IS `359` vs OOS `256`) | **`pre_15m_range_pips`** | `9.4000p` (`5.0500p`) | **`15.4000p`** (`10.0250p`) | **`1.638x`** | 値幅拡大により `+0.1〜+0.3p` 摩擦の相対負担は大幅軽減 |
| **`PURE_STRONG`** (IS `359` vs OOS `256`) | **`pre_15m_body_pips`** | `5.5000p` (`4.1000p`) | **`8.6000p`** (`6.9750p`) | **`1.564x`** | 仲値直前の実需偏り幅が約1.56倍へ拡大 |
| **`PURE_STRONG`** (IS `359` vs OOS `256`) | **`wick_rejection_ratio`** | `0.4839` (`0.2331`) | **`0.5000`** (`0.2352`) | **`1.033x`** | **無次元特徴量はボラ1.74倍化下でも完全な分布定常性を維持** |

### 2.2 Track A 一次評価主契約・アブレーション・事前登録済み副次診断（件数実測済・勝敗はローカル実行確定待ち）

- **一次評価主契約**: `PURE_STRONG`（$n=256$, 両方向合算） vs `NONE`（$n=428$） vs `WEAK_SUB`（$n=90$）
- **事前登録済み副次診断の確定標本数（`PURE_STRONG n=256`）**:
  - ① **売買方向別**: `BUY` = **`143` 件 (`55.9%`)** / `SELL` = **`113` 件 (`44.1%`)**（IS期の `SELL 52.8% / BUY 47.2%` から方向比率が逆転）
  - ② **ゴトー日別**: `True` = **`85` 件** / `False` = **`171` 件**
  - ③ **曜日別**: `Mon` `50` / `Tue` `47` / `Wed` `56` / `Thu` `54` / `Fri` `49`
  - ④ **ATRレジーム別**: `atr14_pips < 2.0p` = **`45` 件 (`17.6%`)** / `atr14_pips >= 2.0p` = **`211` 件 (`82.4%`)**
  - ⑤ **年次別**: `2022`: `69` / `2023`: `45` / `2024`: `46` / `2025`: `46` / `2026`: `50`
  - ⑥ **非累積ヒゲ3区間**: `[0.25, 0.40)`: `67` / `[0.40, 0.55)`: `89` / `[0.55, 1.00]`: `100`
- **実用ベースライン資金シミュレーション（初期50,000円・単発1,000円固定・マーチン禁止・`+0.1p`/`+0.2p`）**: ローカル実行により最終残高・最大ドローダウン率（`DD <= 25%` 対比）・最大連敗数を自動出力（現時点 `unknown`）。

---

## 3. 【並行探索：Track B】マルチ・フィキシング＆次世代モデル（IS 2015–2021限定 / `oos_locked_for_track_b: true`）

| 候補 (`case_id \| symbol`) | 連続性PASS総数 | `PURE_STRONG` | `WEAK_SUB` | `NONE` (`CTRL`) | DST区分 (`夏 / 冬`) | `eta_range` 中央値 | `theta_peak` 中央値 | `+0.1p`〜`+0.3p` 勝率 / EV / HAC CLB |
| :--- | ---: | ---: | ---: | ---: | :--- | ---: | ---: | :--- |
| **`GSR-TKYFIX-003 \| USDJPY`** | **1,173** | 359 | 199 | 615 | `JST` 1,173 | `0.6118` | `0.0000` | `unknown`（ローカル実行で確定） |
| **`GSR-LDNFIX-001 \| EURUSD`** | **1,127** | 420 | 261 | 446 | `BST` 667 / `GMT` 460 | `0.6519` | `0.0000` | `unknown`（ローカル実行で確定） |
| **`GSR-LDNFIX-001 \| GBPUSD`** | **1,157** | 462 | 256 | 439 | `BST` 657 / `GMT` 500 | `0.6310` | `0.0000` | `unknown`（ローカル実行で確定） |
| **`GSR-NYCUT-001 \| USDJPY`** | **1,027** (1件除外) | 399 | 212 | 416 | `EDT` 673 / `EST` 355 | `0.6117` | `0.0714` | `unknown`（ローカル実行で確定） |
| **`GSR-NYCUT-001 \| EURUSD`** | **1,048** | 392 | 211 | 445 | `EDT` 674 / `EST` 374 | `0.6054` | `0.0714` | `unknown`（ローカル実行で確定） |

---

## 4. ローカルPC確定実行コマンド（PowerShellワンライナー）

以下のコマンドをローカルPCで1回実行すると、8ファイルSHA256照合・775MB生M1実測結合・正規＆$t$分布HAC $\text{CLB}_{97.5\%}$・資金DDシミュレーション・Track B非累積4分位＆DST/年次分解を全自動実行し、3点の軽量CSVおよび `spark_audit_handover_manifest_gsr_2026w49.json` を確定SHA256付きで上書き保存します。

```powershell
python "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py"
```

---

## 5. 【🧪 数理ちゃぶ台返し＆好奇心枠】（Math-Driven Curiosity Box — v1.2 特別任務）

### 5.1 【マンネリ・飽き判定（Track A OOSのレジーム変化 ＆ Track B 他市場の構造的限界）】
1. **Track A OOSにおける「方向構成比の逆転」と「ボラ1.74倍化」という静かな地雷**:
   - 今回のCovariate Shift実測で判明した通り、2022–2026年のOOS期間ではUSDJPYの `atr14_pips` 中央値が ISの `1.83p` から **`3.18p`（`1.736倍`）** へ跳ね上がり、さらに `PURE_STRONG`（$n=256$）の方向構成比が ISの `SELL 52.8% / BUY 47.2%` から OOSでは **`BUY 55.9% (143件) / SELL 44.1% (113件)`** へと逆転している。
   - W48 ISで優位性の大半を稼いでいたのは「仲値前の実需買い釣り上げ後の逆張り `SELL`（65.79%）」であり、`BUY`（54.71%）は損益分岐ギリギリだった。OOSで円安トレンド下の押し目買い／利食い売りが増えた結果、エッジの薄い `BUY` 側が過半数を占めている事実は、**「単一の対称ヒゲ条件（SELL/BUY無差別）で両方向を同等に扱う設計そのものが、東京仲値という非対称な実需構造（輸入企業のドル買い偏重）を取りこぼしている」** ことを示唆している。
2. **Track B（ロンドンフィックス／NYカット）における「時間ウィンドウの固定化」と `theta_peak` 退化**:
   - `GSR-LDNFIX-001`（WMR 16:00 London Fix）のベンチマーク算定窓は5分間（15:57:30〜16:02:30）に跨がるため、東京仲値（09:55:00の瞬間公表）と違って **「15:59確定 ➔ 16:00参入」ではWMR執行の後半2分半（16:00:00〜16:02:30）の真っただ中に正面衝突する構造的リスク** がある。また新規特徴量 `theta_peak` は5組中3組で中央値 `0.0000` に退化しており、単一極値足 $k^*$ 頼みの設計は情報エントロピーが枯渇している。

### 5.2 【数理モデルによる「あえてこうしたらどうなる？」提案】
確定足 $t$ 以前のM1 OHLC（Label-Free・未来参照ゼロ）のみから計算可能な次世代特徴量として、**「時間重心 $\tau_{\text{CoM}}(t)$ × 経路エントロピー減衰（KL情報量 $D_{\text{KL}}(p_t \parallel u)$）× 局所ボラティリティ加速度（Hawkes Excitation Ratio $\lambda_{\text{late}} / \lambda_{\text{early}}$）」の3次元無次元状態ベクトル** を提案する：
- $t-14 \dots t$ の15本M1足に対し、15分方向 $s_t = \text{sign}(C_t - O_{t-14})$ に沿う実体寄与率 $p_k(t) = \frac{\max(s_t(C_{t-14+k} - O_{t-14+k}), 0)}{\sum_{j=0}^{14} \max(s_t(C_{t-14+j} - O_{t-14+j}), 0)}$ から、**インパルス時間重心 $\tau_{\text{CoM}}(t) = \sum_{k=0}^{14} \frac{k}{14} p_k(t)$** と **直前3分間のレンジ加速度 $\Lambda_{\text{Hawkes}}(t) = \frac{\frac{1}{3}\sum_{k=12}^{14} (H_{t-14+k}-L_{t-14+k})}{\frac{1}{12}\sum_{k=0}^{11} (H_{t-14+k}-L_{t-14+k})}$** を算出する。
- **野心的仮説**: `theta_peak` が `0.0000` に張り付く個体群であっても、**「前半主導のブリッジ減衰（$\tau_{\text{CoM}} < 0.55$）かつ直前3分間でボラティリティが鎮静化していない過熱ピーク（$\Lambda_{\text{Hawkes}} > 1.25$）に反対ヒゲが出現した状態」** を抽出すれば、2022–2026年のような `ATR 1.74倍` の高ボラレジームやWMRロンドンフィックスの5分間算定窓においても、スケール変動に不変なまま「執行枯渇による反転」と「貫通ブレイクアウト」を分離できる。
<!-- RESEARCH_TRACE_END -->
