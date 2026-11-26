# GSR-202611-W5-FRI 第3工程 → 次週月曜（GSR-2026W50）第1工程 引き継ぎ書

🏷️ [TRACE: GSR-202611-W5-FRI | 次週月曜引き継ぎ（GSR-2026W50） | GSR-TKYFIX-002 OOS正式棄却に伴う新IS仮説（TKYFIX-004 SELL専業＆LDNFIX-002無条件逆張り）差配]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W49; GSR-202611-W5-FRI; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md
record_id: GSR-202611-W5-FRI
session_title: 第3工程から次週月曜（GSR-2026W50）第1工程への引き継ぎ指示書
case_id: GSR-202611-W5-FRI
decision: REJECTED (GSR-TKYFIX-002 OOS, GSR-LDNFIX-001, GSR-NYCUT-001) / HOLD (GSR-TKYFIX-003)
oos_locked: true
-->

- **発行日**: 2026-11-27 (JST)
- **OOSロック状態**: `oos_locked: true`（全通貨2022-01-01以降は完全遮断を維持）

## 1. 永久除外リスト（Exclusion List — 再検証・延命厳禁）
- `GSR-CLIMAX-001` / `GSR-PULLBACK-001` / `GSR-FAKEOUT-001` / `GSR-SURVEY-001` / `BO-EUR-004` / `BO-EUR-005`（W46以前）
- `GSR-EXHAUST-001` / `GSR-SHOCKDECAY-001`（W47）
- `WEAK_SUB`（`0 <= wick_rejection_ratio < 0.25`, TRAP-06汚染層）
- **`GSR-TKYFIX-002`（両方向合算契約）**: W49 One-Shot OOSにて正式棄却（事後 `SELL` 切り出しによる同一データの再テスト厳禁）
- **`GSR-NYCUT-001`（EURUSD / USDJPY）**: NY 10:00 カット逆張り仮説はISで全面崩壊のため永久凍結
- **`GSR-LDNFIX-001`（EURUSD / GBPUSD ヒゲ拒絶モデル）**: Control（`NONE`）に対して負の増分となったため凍結

## 2. 次週月曜（`GSR-2026W50`）第1工程 優先調査アクション（IS 2015–2021 限定・`HOLD_LABEL_FREE`）
1. **継続・Spark監査待ち**: **`GSR-TKYFIX-003`**（USDJPY 09:55 JST、`phi_urp` 幾何特徴量統合）
   - `PURE_STRONG` 内の `Q4 (0.598, 0.991]`（`48.89%`）を除外し得る事前固定仮説（`phi_urp <= 0.60` かつ/または `SELL` 方向分離）について、Spark独立監査（`GSR-202611-W5-WED-SPARK`）およびIS内追加検証を実施する。
2. **新規提案① `GSR-LDNFIX-002`（ロンドン16:00 フィキシング・ヒゲ条件なし基礎リバランス逆張り）**:
   - W49で判明した「EURUSD `NONE` `62.78%` / `ALL_POOLED` `60.78%`」「GBPUSD `NONE` `60.14%` / `ALL_POOLED` `59.29%`」という強い基礎逆張り構造を受け、ヒゲ拒絶フィルタを撤廃し、**`BST` vs `GMT` レジーム・`move15m_atr` 非累積帯・方向別（EURUSD `BUY` `61.68%` / GBPUSD `SELL` `61.18%`）** に着目したIS専用機会台帳を構築する。
3. **新規提案② `GSR-TKYFIX-004`（USDJPY 東京仲値 ボラティリティ正規化・Covariate Shift耐性モデル）**:
   - W49 OOSで判明した `atr14_pips` 1.74倍化（`1.83p -> 3.18p`）と `BUY` 側崩壊を踏まえ、絶対pips閾値に依存しない **無次元ATR比＋15分トレンド持続構造＋東京仲値実需非対称性（ショート軸）** をIS期間（2015–2021）限定で新規設計する。

<!-- RESEARCH_TRACE_END -->
