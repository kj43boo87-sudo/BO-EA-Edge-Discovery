# GSR-202611-W5-FRI 第3工程 → 次週月曜（GSR-2026W50）第1工程 引き継ぎ書

🏷️ [TRACE: GSR-202611-W5-FRI | 次週月曜引き継ぎ（GSR-2026W50） | GSR-LDNFIX-002 最優先昇格・専用Label-Free台帳設計指針およびEURUSD/GBPUSD OOS完全ロック厳命]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W49; GSR-202611-W5-FRI; GSR-202611-W5-WED-SPARK; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md
record_id: GSR-202611-W5-FRI
session_title: 第3工程から次週月曜（GSR-2026W50）第1工程への引き継ぎ指示書
case_id: GSR-202611-W5-FRI
decision: FAIL (GSR-TKYFIX-002, GSR-NYCUT-001) / HOLD -> PRIORITY (GSR-LDNFIX-002)
oos_locked: true (EURUSD & GBPUSD 2022+)
-->

- **発行日**: 2026-11-27 (JST)
- **OOS保護絶対規定**: **EURUSD および GBPUSD の `2022-01-01` 以降 OOS データは完全未開封ロック（`oos_locked: true`）を厳守** すること。

## 1. 永久除外リスト（Exclusion List — 再検証・パラメータ延命・事後救済厳禁）
- `GSR-CLIMAX-001` / `GSR-PULLBACK-001` / `GSR-FAKEOUT-001` / `GSR-SURVEY-001` / `BO-EUR-004` / `BO-EUR-005`（W46以前）
- `GSR-EXHAUST-001` / `GSR-SHOCKDECAY-001`（W47）
- `GSR-TKYFIX-001` の `WEAK_SUB`（$0 \le 	ext{wick} < 0.25$, `TRAP-06`）
- **`GSR-TKYFIX-002`（USDJPY One-Shot OOS 正式棄却・`GSR_TKYFIX_002.mq4` 実装中止・アーカイブ凍結）**
- **`GSR-NYCUT-001`（EURUSD / USDJPY NYカット逆張り・`TRAP-05` 永久凍結）**
- **`GSR-LDNFIX-001` の東京仲値由来ヒゲフィルター（`PURE_STRONG` 条件）**: 逆アブレーション確認済みのため撤廃
- （低優先待機）`GSR-TKYFIX-003`: USDJPY 09:55 OOS既閲覧のためフォワード専用待機（W50は着手不要）

## 2. 次週月曜（`GSR-2026W50`）最優先ミッション：`GSR-LDNFIX-002`（EURUSD / GBPUSD 無フィルター・ベースラインIS完全検証）

### 2.1 台帳設計指針（W49台帳の流用 vs 専用Label-Free台帳の新規生成）
- **結論：【`GSR-LDNFIX-002` 専用Label-Free台帳を第1工程で新規生成する】（W49台帳を Gate 1 突合基準として併用）**
  - **新規生成を採択する理由**: W49の `is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv`（SHA256: `0272871721a3e96b6ace75afaa72e13708c8d398355a2cc971459d8cdec1a1c1`）には、月末リバランス効果を測る **`is_month_end`**（月末最終営業日フラグ：実暦ベースで当該月の最終平日または英国営業日判定）および直前15分の出来高加重乖離 **`z_vwap_15m`**（生M1の Tick Volume を用いた `(Close[15:59] - VWAP_15m) / ATR14` または標準化乖離）が含まれていない。
  - **Gate 1 整合性保証（流用突合契約）**: 新規生成する `is_2015_2021_opportunity_ledger_gsr_ldnfix002_gsr_2026w50.csv`（純粋 `HOLD_LABEL_FREE`、勝敗・未来価格列ゼロ）は、EURUSD（`1,127`行）および GBPUSD（`1,157`行）の **`trade_date`・`expected_entry_utc`・`direction`・`dst_zone` が W49台帳（`02728717...`）と100%一致することをスクリプト内で自動検証** した上で、`is_month_end`・`z_vwap_15m`・`move15m_atr`・`atr14_pips` の追加特徴量を付与して出力すること。

### 2.2 第1工程〜第2工程の事前固定検証契約（W50）
1. **対象市場・厳密執行契約**: EURUSD / GBPUSD M1、ロンドン `15:59` 確定足判定 ➔ `16:00` 始値参入 ➔ `16:05` 厳密300秒満期（BST=`15:00 UTC` / GMT=`16:00 UTC`、同値LOSE、摩擦 `+0.0 / +0.1 / +0.2 / +0.3 pip`）。
2. **主契約（無フィルター・ベースライン）**: ヒゲ条件を撤廃した `ALL_POOLED`（`move15m_atr >= 1.5` のみ）を主契約とし、`NONE` vs `CANDIDATE` の逆アブレーション構造を含めて評価。
3. **必須非累積（Disjoint）分解テスト**:
   - ① **`dst_zone`（`BST` vs `GMT`）**（特にEURUSDでの季節断層検証）
   - ② **`direction`（`SELL` vs `BUY`）**
   - ③ **`is_month_end`（月末最終営業日 vs 通常日）**
   - ④ **`z_vwap_15m` および `move15m_atr` の非累積4分位（Q1〜Q4）**
   - ⑤ **年次安定性（2015–2021）および IS資金シミュレーション（初期50,000円・固定1,000円・マーチンなし・最大DD $\le 25\%$ 確認）**

<!-- RESEARCH_TRACE_END -->
