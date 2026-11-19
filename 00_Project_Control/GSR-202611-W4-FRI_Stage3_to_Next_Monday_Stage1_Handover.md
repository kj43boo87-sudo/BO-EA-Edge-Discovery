# GSR-202611-W4-FRI 第3工程 → 次週月曜（GSR-2026W49）第1工程 引き継ぎ書

🏷️ [TRACE: GSR-202611-W4-FRI | 次週月曜引き継ぎ（GSR-2026W49） | GSR-TKYFIX-002 One-Shot OOS開封契約および新規フィキシング候補差配]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W48; GSR-202611-W4-FRI; GSR-202611-W4-WED-SPARK; GSR-TKYFIX-002; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md
record_id: GSR-202611-W4-FRI
session_title: 第3工程から次週月曜（GSR-2026W49）第1工程への引き継ぎ指示書
case_id: GSR-202611-W4-FRI
decision: PASS_CANDIDATE
oos_locked: true
-->

- **発行日**: 2026-11-20 (JST)
- **前週結果**: **`GSR-TKYFIX-002`**（USDJPY M1 東京仲値 `PURE_STRONG`, $n=360$）がプロジェクト初の **IS全5ゲート完全合格（`PASS_CANDIDATE`）** を達成。
- **現在のOOSロック状態**: `oos_locked: true`（2022-01-01以降 `1,783,913` 行は未開封維持）。

## 1. 永久除外リスト（Exclusion List — 再検証・パラメータ延命厳禁）
以下の既知棄却案件および汚染サブグループは、一切の再検証・閾値微修正・延命工作を禁止する。
- `GSR-CLIMAX-001` / `GSR-PULLBACK-001` / `GSR-FAKEOUT-001` / `GSR-SURVEY-001` / `BO-EUR-005`（W46 棄却・凍結）
- `GSR-EXHAUST-001` / `GSR-SHOCKDECAY-001`（W47 棄却・凍結）
- `GSR-TKYFIX-001` の旧OR条件混入層 **`WEAK_SUB`**（$0 \le \text{wick} < 0.25$, $n=201$, +0.1p勝率 `49.7512%`, TRAP-06 逆アブレーション汚染層 — 永久除外）

## 2. 最優先タスク①：`GSR-TKYFIX-002` One-Shot OOS初回開封契約（総監督・オーナー承認後に実行）
1. **事後カーブフィッティングの絶対禁止（Primary OOS Contract）**:
   - IS期間で確認された `SELL`（65.79%）vs `BUY`（54.71%）の非対称性や `Move 2.6〜3.5 ATR` 帯の窪地（`52.75%`）を理由に、**OOS開封前に条件を一切変更してはならない**。
   - 事前固定仕様 `GSR-TKYFIX-002`（`PURE_STRONG`: `move_15m / atr14 >= 1.5` かつ `wick_rejection_ratio >= 0.25`、両方向合算、`09:55:00 JST` 始値参入 ➔ `10:00:00 JST` 厳密300秒満期、同値LOSE、摩擦 `+0.0 / +0.1 / +0.2 / +0.3 pip`）を 2022-01-01以降のOOSデータへ**一度限り（One-Shot）**適用する。
2. **事前登録済み副次診断（Pre-Registered Diagnostic Breakdown）**:
   - Primary合算結果と同時に、① `SELL` 単体 vs `BUY` 単体、② `gotobi_1` vs `gotobi_0`、③ 年次別（2022〜2026年）の分離成績を出力すること。
   - OOS合格後のMQL4/MQL5実装において、`SELL` 専業とするか両方向とするかの最終判断材料とする。
3. **MQL4実装必須制約（Gate 4 / TRAP-04 根絶）**:
   - `barsPassed > 5`（実質6分満期バグ）を完全禁止し、`TimeCurrent() >= entryTime + 300` およびスプレッド上限・1日1回約定ロックを実装する。

## 3. 次週月曜（`GSR-2026W49`）第1工程 新規探索タスク（IS期間 2015–2021 のみ・OOS完全ロック）
`GSR-TKYFIX-002` の成功構造（**「機関投資家ベンチマーク・フィキシング直前の実需偏り ＋ 直前足の明確な反対ヒゲ拒絶 ＋ 厳密5分逆張り」**）を軸に、以下の新規3候補をIS期間（2015–2021）限定・ラベル完全マスクで機会台帳化する。
1. **`GSR-LDNFIX-001`**（EURUSD / GBPUSD M1 ロンドン・フィキシング 16:00 London 直前15分偏り＋15:59反対ヒゲ拒絶5分逆張り — 英国夏時間BST/GMT切替を厳密反映）
2. **`GSR-NYCUT-001`**（USDJPY / EURUSD M1 NYオプションカット 10:00 New York 直前15分偏り＋09:59反対ヒゲ拒絶5分逆張り — 米国夏時間EDT/EST切替を厳密反映）
3. **`GSR-TKYFIX-003`**（USDJPY M1 東京仲値 次世代時間構造モデル：第2工程のレンジ効率 $\eta_{\text{range}}$・時間重心 $\tau_{\text{CoM}}$ と Spark監査官の極値経過時間 $\theta_{\text{peak}}$・累積押し戻し率 $\Psi_{\text{reject}}$ を用いた非累積・事前固定特徴量の機会台帳設計）

## 4. 第1工程 必須コンプライアンス（v1.2規定）
- `oos_locked: true`（2022-01-01以降の全行を物理遮断）および `HOLD_LABEL_FREE`（勝敗・未来価格列の完全マスク）を厳守すること。
- 生M1原本および出力台帳のSHA256・行数フロー・6分間連続性チェック結果を `stage1_to_stage2_handover_manifest_gsr_2026w49.json` に記録すること。

<!-- RESEARCH_TRACE_END -->
