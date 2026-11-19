# INDEX — トレード手法の市場調査＆データ点検（Gemini側必勝調査報告：第1工程）

- 保管パス（第1工程）: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検`
- 次工程パス（第2工程）: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証`
- 最終工程パス（第3工程）: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理`
- 共通マスターコンテキスト: `..\..\QUANT_PYTHON_MASTER_CONTEXT.md`（SHA256: `89f9c215a02717b1057cd14fa9167b5b8cb7fbc37e60760dbe5f572c2bbb9d13`）
- ロール・自己反証規定: `MASTER_DIRECTOR_ROLE_PROMPT_v1.1.md`
- 専用TRACE規約: `..\機会台帳突合＆IS統計・Plateau検証\GEMINI_DISCOVERY_TRACE_RULE.md`（SHA256: `fd70c9e64015404b8c324a03a62135a4b1f3229f5f8100d157d139c25517a4d6`）
- 最終更新日: `2026-11-16 JST`

---

## 1. 完了済み・棄却済み案件の永久凍結リスト（再検証・同型再提案の禁止）

1. **`BO-EUR-004` / `BO-EUR-005`**（EURUSD 東京レンジブレイク→再侵入 `I`・境界再テスト反発 `R`・再ブレイク `B`）：
   - 決定文書: `BO-EUR-004_decision.md` / `BO-EUR-005_decision.md`（SHA256: `2d0e2e05b8dcd86c2993b2e0fea0f8c8505d609e654a5110ce49e7882c255109`）
   - 最終ステータス: **正式棄却・永久凍結**（432セル中 $\text{CLB}_{97.5\%} > 0$ が `0/432`、擬似プラトー確定）。
2. **`GSR-2026W46`**（EURUSD 新規3候補＋既存EA監査：2026-11-09 確定）：
   - 決定文書: `GSR-2026W46_decision.md`（SHA256: `04de62ca61d43a89eb66835d2da357c76edaa79288c56d9cfe2221d743201bea`）
   - **`GSR-CLIMAX-001`** / **`GSR-PULLBACK-001`** / **`GSR-FAKEOUT-001`**: 192セル中 $\text{CLB}_{97.5\%} > 0$ が `0/192` により **正式棄却・他4通貨への展開中止**。
   - **`GSR-SURVEY-001`**（既存EURUSD逆張りEA 8本）: MQL4 `barsPassed > 5` による6分満期バグを特定、真の5分満期（`Open[t+6]`）再計算で勝率 `40.51%` へ崩壊のため **旧6分満期バグ版を破棄**。
3. **`GSR-2026W47`**（EURUSD / USDJPY 汎用逆張り2候補の棄却＋東京仲値候補の保留継承：2026-11-13 確定）：
   - 決定文書: `GSR-2026W47_decision.md`（SHA256: `bd2a79abf080883828121c896041abdebf73441ebe877e1287269b467787ddd7` / `a045fc0bd77f06349b9dd648f0f06a470a94af59ee4c7c8a356459ace1e765d3`）
   - **`GSR-EXHAUST-001`**（M1 BB $\pm 2.5\sigma$ 到達後の切り下げ反転）: 逆アブレーション（`-2.40%pt`）および順行中央値 `0.0〜0.1 pip` による摩擦崩壊（TRAP-05）のため **正式棄却・永久凍結**。
   - **`GSR-SHOCKDECAY-001`**（M1大陽線・大陰線 $\ge 2.2\text{ ATR}$ 直後の値幅収縮逆張り）: 逆アブレーションおよび順行中央値 `0.1 pip` による摩擦崩壊（TRAP-05）のため **正式棄却・永久凍結**。
   - **`GSR-TKYFIX-001`**（USDJPY 東京仲値 09:55 JST 直前15分偏り＋09:54確定足ヒゲ拒絶5分逆張り）: **保留 ➔ `GSR-TKYFIX-002`（IS内汚染除去追加検証）へ継承**。

---

## 2. GSR-2026W48 第1工程 実行済み正本資産（2026-11-16 JST 確定）

- **対象案件**: `GSR-2026W48`（個別検証コード: **`GSR-TKYFIX-002`** / 親案件: `GSR-TKYFIX-001`）
- **対象生データ**: `G:\マイドライブ\通貨ペア\Dukascopy 1分足\USDJPY\2026.10.16USDJPY(3)-M1-No Session.csv`
  - サイズ / 行数: `258,871,846` bytes / 全 `4,424,800` 行（IS採用: `2,608,784` 行 / 2014年以前除外: `32,103` 行 / 2022年以降OOS遮断: `1,783,913` 行）
  - SHA256: `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29`

| ファイル名 | 版 / 規模 | SHA256（実測値） | 確認状態区分 | 用途・備考 |
| :--- | :--- | :--- | :--- | :--- |
| `profile_is_market_structure_gsr_2026w48_v1_0.py` | v1.0.0 (23,964 B) | `c16af1fed45016c048b310987991f489a304d15776f343353c19f2f9d2ebf51a` | `実行確認済み` | `GSR-TKYFIX-002` 専用 Label-Free 機会台帳生成・データ連続性点検スクリプト |
| `is_2015_2021_opportunity_ledger_gsr_2026w48.csv` | 1,177 rows / 12 cols (136,902 B) | `834edaa0353d9f6e2cdf174553c77ceb0b121109831e51a18c15ba8bafeb784d` | `現行版確認済み` | **第2工程引き渡し主台帳**（v1.1規定準拠・厳密12カラム・結果列ゼロ保証・6分間連続性PASS `1,177/1,177`） |
| `is_2015_2021_opportunity_ledger_gsr_2026w48_masked_v22.csv` | 1,177 rows / 27 cols (378,451 B) | `757e04d23569c508cd0df7a0ecae7e9bb963b17c788cec61616c115706b148a7` | `現行版確認済み` | **v2.2標準バリデータ互換台帳**（`win_loss_label`/`net_pips_result` を `HOLD_LABEL_FREE` でマスク＋非累積3軸ビン付与） |
| `stage1_to_stage2_handover_manifest_gsr_2026w48.json` | JSON (5,379 B) | `add080fd545a077c3beec495df21bc243c905ab010df9e7fa9c64ef449b2c530` | `現行版確認済み` | 第1工程→第2工程引き継ぎマニフェスト（実験A/B/Cサンプル数・Self-Ask 3問判定記録） |
| `HANDOVER_GSR_2026W48_STAGE1.md` | Markdown (13,776 B) | `635048a706980268d21515d4f6a468c83c54efdfab3860587586c1f1674d6033` | `現行版確認済み` | 第1工程完了報告・自己反証ゲート（Self-Ask A/B/C）回答・第2工程引継ぎ書 |

---

## 3. 前週以前（GSR-2026W47 / GSR-2026W46）保管資産履歴（非破壊保持）

| ファイル名 | 版 / 規模 | SHA256（実測値） | 確認状態区分 | 用途・備考 |
| :--- | :--- | :--- | :--- | :--- |
| `profile_is_market_structure_gsr_2026w47_v1_0.py` | v1.0.2 (14,105 B) | `d3f4ba214a79bb41e38313a1dbd307afff4a303ef836bee3d922ed77619bc5a1` | `実行確認済み（旧版保持）` | `GSR-2026W47` 第1工程プロファイラ |
| `is_2015_2021_opportunity_ledger_gsr_2026w47.csv` | 99,945 rows (26,659,086 B) | `7f8581b693da499064dd3d0aaee2f20c2babc84d8859dfd852c923b5f91c7d38` | `実行確認済み（旧版保持）` | `GSR-2026W47` 3候補統合 Label-Free 機会台帳 |
| `stage1_to_stage2_handover_manifest_gsr_2026w47.json` | JSON (2,385 B) | `37a8842b0d34471d3adeeafac241279c85ab19fcb099b28f9155128c990b969c` | `実行確認済み（旧版保持）` | `GSR-2026W47` 第1工程引き継ぎマニフェスト |
| `profile_is_market_structure_2015_2021_v1_2.py` | v1.2.0 (43,374 B) | `a7fa4ada92f47c5adb2d01db7e4c823bd8a5820fb06c23c2f13951027aaae2eb` | `実行確認済み（旧版保持）` | `GSR-2026W46` 第1工程スクリプト |
| `output_is_profile_20261107_065432/is_2015_2021_opportunity_ledger_eurusd.csv` | 6,733 rows | `a45156cfc29cec249a538d3b81b85b74e02817c0cf0ae67ac783b6d57c72c327` | `実行確認済み（旧版保持）` | `GSR-2026W46` EURUSD Label-Free 機会台帳 |
