# INDEX — 執行監査・週次総括・Git資産整理（Gemini側必勝調査報告：第3工程）

- **保管パス（第3工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理`
- **関連パス（第1工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検`
- **関連パス（第2工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証`
- **専用TRACE採番規約**: `GEMINI_DISCOVERY_TRACE_RULE.md`（SHA256: `fd70c9e64015404b8c324a03a62135a4b1f3229f5f8100d157d139c25517a4d6`）
- **最終更新日**: `2026-11-09 JST`

---

## 1. GSR-2026W46 執行監査・最終5ゲート判定サマリ（2026-11-09 確定）

| 専用案件コード | 候補モデル / 監査対象 | 対象通貨・期間 | 最終5ゲート判定 | 正式決定・処置 |
| :--- | :--- | :--- | :--- | :--- |
| **`GSR-CLIMAX-001`**<br>（親: `GSR-2026W46`） | `Proposal_B_BBClimaxReversal`<br>確定M5非トレンド限定・M1 BB 2.8σクライマックス逆張り | `EURUSD` M1/M5<br>IS: 2015–2021 ($n=734$) | ①台帳一致: **PASS**<br>②IS HAC下限: **FAIL** (`50.14%`, $\text{CLB}_{97.5\%}=-0.1377$)<br>③近傍Plateau: **FAIL** (0/64合格、唯一BE超えセルも $n=40$ 孤立スパイク)<br>④Spark監査: **PASS** (構造解明)<br>⑤MT4摩擦耐性: **FAIL** (`+0.3p` 勝率 `46.87%`) | **棄却・凍結**<br>（他4通貨への展開中止・2022–2026 OOS未開封ロック） |
| **`GSR-PULLBACK-001`**<br>（親: `GSR-2026W46`） | `Proposal_C_M5TrendPullback`<br>確定M5 PO同調 × M1ボラ収縮後のEMA20反発確定 | `EURUSD` M1/M5<br>IS: 2015–2021 ($n=4,597$) | ①台帳一致: **PASS** (Raw 4,598→有効 4,597、除外1件 `GAP_T2_T5` 完全一致)<br>②IS HAC下限: **FAIL** (`44.88%`, $\text{CLB}_{97.5\%}=-0.1964$)<br>③近傍Plateau: **FAIL** (BE超え `0/64`、全7年赤字)<br>④Spark監査: **PASS** (構造解明)<br>⑤MT4摩擦耐性: **FAIL** (`+0.3p` 勝率 `42.55%`) | **棄却・凍結**<br>（他4通貨への展開中止・2022–2026 OOS未開封ロック） |
| **`GSR-FAKEOUT-001`**<br>（親: `GSR-2026W46`） | `Proposal_A_FakeoutReentry`<br>東京箱ブレイク失敗・即時実体再侵入（M5傾き・大実体フィルタ付） | `EURUSD` M1/M5<br>IS: 2015–2021 ($n=1,401$) | ①台帳一致: **PASS**<br>②IS HAC下限: **FAIL** (`48.82%`, $\text{CLB}_{97.5\%}=-0.1460$)<br>③近傍Plateau: **FAIL** ($\text{CLB}_{97.5\%}>0$ は `0/64`、局所9セルは単一コーナー $n=67$ を使い回した**擬似プラトー**)<br>④Spark監査: **PASS** (非累積マージナルv1.1で完全実証)<br>⑤MT4摩擦耐性: **FAIL** (`+0.3p` 勝率 `46.32%`) | **棄却・凍結**<br>（他4通貨への展開中止・2022–2026 OOS未開封ロック） |
| **`GSR-SURVEY-001`**<br>（親: `GSR-2026W46`） | 既存EURUSD逆張りEA 8本（計206取引）M1連続性＆真の5分満期再計算監査 | `EURUSD` M1<br>8レポート（2020–2026） | ①連続性照合: **PASS** (連続有効 195 / 206)<br>②真の5分満期勝率: **FAIL** (全8本で `25.00%〜51.72%`、合算 **`40.51%`**, $\text{EV}=-0.2505$)<br>④Spark監査: **PASS** (`barsPassed > 5` による6分満期バグが旧高勝率の主因と特定) | **旧6分満期バグ版の破棄・厳密5分満期（`Open[t+6]`）標準化** |
| （比較参照元）<br>`BO-EUR-005` | 東京箱ブレイク→再侵入（`I`）・境界再テスト（`R` / `B`） | `EURUSD` M1<br>IS: 2015–2021 ($n=1,050$) | 2026-11-05 棄却確定済（`BO-EUR-005_decision.md`） | **棄却・凍結維持**<br>（`VIEWED_EVAL` 748件未開封維持） |

---

## 2. 本フォルダ（第3工程：執行監査・週次総括・Git資産整理）保管ファイル一覧

| ファイル名 | 種別 | サイズ (bytes) | SHA256（実測値） | 内容・用途 |
| :--- | :--- | :--- | :--- | :--- |
| `GSR-2026W46_decision.md` | Markdown | 12,747 | `04de62ca61d43a89eb66835d2da357c76edaa79288c56d9cfe2221d743201bea` | **`GSR-2026W46` 公式決定記録**（EURUSD 3候補＆既存EA監査の最終5ゲート判定・棄却・他通貨展開中止） |
| `GSR-2026W46_Spark_Audit_and_Executive_Summary_2026-11-09.md` | Markdown | 4,837 | `40132fcda3eb398232ba4fbe57c3f96b344d0460a8d49248465583e4dbdf959f` | **`GSR-2026W46` 執行監査・週次総括統合報告書**（Spark監査 `GSR-202611-W2-WED-SPARK` 受入・非累積マージナル解体） |
| `is_non_cumulative_marginal_3d_eurusd.csv` | CSV | 29,516 | `2705bea4842ab7fb9f3713d11eba873d07e143154b115e349286c0af16ca03aa` | v1.1.0スクリプトにより生成したEURUSD 3候補・192個の非累積3D直積スライス集計表（第2工程出力フォルダにも同期済） |
| `is_plateau_grid_eurusd_v1_1.csv` | CSV | 42,572 | `263ab56dc9ea57cbc53095bdffa0325a5d4ccf5c9389d8d60e17e715a73cb195` | v1.1.0スクリプトにより生成した `PSEUDO_PLATEAU_WARNING` 判定付き192セルPlateau表 |
| `DECISION_TEMPLATE.md` | Markdown | 4,722 | `54fb98188956c831fd3489c50481404edbe4ad4e0308de135d9bf5aa11044c0d` | `GSR-*` 専用コード・非累積3Dマージナル検証対応の公式TRACE＆`decision.md` 標準テンプレート |
| `sync_gsr_2026w46_assets_and_git_commit.ps1` | PowerShell | 13,583 | `f0b1d55474e9815ab13c84bbac5baa992872647f53ef79487f4f3b2481c2a2a8` | `GSR-2026W46` 全3工程の `.py` / `.md` 実ソースSHA256照合・`INDEX.md` 追記・大容量CSV除外Gitコミットスクリプト |
| `GEMINI_DISCOVERY_TRACE_RULE.md` | Markdown | 3,082 | `fd70c9e64015404b8c324a03a62135a4b1f3229f5f8100d157d139c25517a4d6` | Gemini側必勝調査報告 専用TRACEコード（`GSR-*`）採番規約 |
| `BO-EUR-005_decision.md` | Markdown | 8,961 | `2d0e2e05b8dcd86c2993b2e0fea0f8c8505d609e654a5110ce49e7882c255109` | （過去参照アーカイブ）2026-11-05 棄却確定記録 |

---

## 3. 全3工程横断 検証スクリプト（`.py`）・主要証跡のSHA256一覧（`GSR-2026W46`）

| 保管工程 | ファイル名 | 版 / 規模 | SHA256（実測値） | 確認状態区分（手順書 規則4） |
| :--- | :--- | :--- | :--- | :--- |
| 第1工程 | `profile_is_market_structure_2015_2021_v1_4.py` | v1.4.0 (43,857 B) | `809ec0ec9c5623dd369814c238ec2b344f2ab9f83ae9e11d1df718e495ad732a` | **実行確認済み**（Dukascopy M1正本＆`GSR-*`対応） |
| 第1工程 | `profile_is_market_structure_2015_2021_v1_3.py` | v1.3.0 (42,528 B) | `c2098de77aef3c19719626d0e33acd050d59bd8192479e6079c039c7d3e1fa4c` | 旧版保持 |
| 第1工程 | `profile_is_market_structure_2015_2021_v1_2.py` | v1.2.0 (43,374 B) | `a7fa4ada92f47c5adb2d01db7e4c823bd8a5820fb06c23c2f13951027aaae2eb` | 旧版保持 |
| 第1工程 | `output_is_profile_20261107_065432/is_2015_2021_opportunity_ledger_eurusd.csv` | 6,733 rows (2,261,339 B) | `a45156cfc29cec249a538d3b81b85b74e02817c0cf0ae67ac783b6d57c72c327` | **実行確認済み**（Drive保管 / Git除外） |
| 第1工程 | `output_is_profile_20261107_065432/existing_reports_continuity_audit_auto.csv` | 60 rows (18,836 B) | `f4dbb3b6d58f61fd4dcfc5aa1cc1cd205b3abe3ca557211eff506184ac58cdc3` | **実行確認済み**（Git登録対象） |
| 第2工程 | `gsr_eurusd_is_plateau_verifier_v1_0.py` | v1.1.0 (48,204 B) | `cbb38b9e9776d8215899c460d20d12ce02eca74b9e9c227a97559419d64dee21` | **実行確認済み**（Spark監査改修・非累積3Dマージナル正本） |
| 第2工程 | `gsr_eurusd_is_plateau_verifier_v1_1.py` | v1.1.0 (44,408 B) | `98a75ba95ff26e3b702bbbfa4b450f2eb195e6bec1588e41ef3a8429e5be02c9` | 静的確認済み（v1.1別名保存版） |
| 第2工程 | `gsr_eurusd_is_plateau_verifier_v1_0_old_cumulative.py` | v1.0.0 (42,846 B) | `e10faa06c2f665c1cc732fab433b6d52daf9d598205c7d53a6c8707126a9a077` | 旧版保持（累積格子レガシー版） |
| 第2工程 | `output_eurusd_is_plateau_20261109_060458/spark_audit_handover_manifest_eurusd.json` | JSON (25,969 B) | `fab0d40108e65a08c8f4e8ef0c8fd82fecd5c8aa0b180a5bbc6f63d1f58b7019` | **実行確認済み**（Git登録対象） |
| 第2工程 | `output_eurusd_is_plateau_20261109_060458/is_standalone_summary_eurusd.csv` | 3 rows (945 B) | `23a7dcc17a5adc428ebad237564307ec1f67280e07c35ff1a37af48b955947e1` | **実行確認済み**（Git登録対象） |
| 第2工程 | `output_eurusd_is_plateau_20261109_060458/is_yearly_breakdown_eurusd.csv` | 21 rows (2,019 B) | `3ee8ef47d3d937cf3bb711f5e1f658765cacc8fc2f984e1873321f9dbf6ba55a` | **実行確認済み**（Git登録対象） |
| 第2工程 | `output_eurusd_is_plateau_20261109_060458/is_session_breakdown_eurusd.csv` | 10 rows (1,188 B) | `422516c5ad06279ae6618e70065929a08c67af4ee1743b71c6dd919a575ffd6c` | **実行確認済み**（Git登録対象） |
| 第2工程 | `output_eurusd_is_plateau_20261109_060458/is_atr_breakdown_eurusd.csv` | 9 rows (1,056 B) | `6a21383115f2212ec67a5f21dcd1986c14e1ed53fa80a042f886bb0e3426193b` | **実行確認済み**（Git登録対象） |
| 第2工程 | `output_eurusd_is_plateau_20261109_060458/existing_eurusd_reports_m1_audit.csv` | 8 rows (1,005 B) | `d24d4b64f323141cc211f9bef8931a1e81ae463f7bf3795cf087c5a43f7d14c1` | **実行確認済み**（Git登録対象） |
| 第2・第3工程 | `is_non_cumulative_marginal_3d_eurusd.csv` | 192 rows (29,516 B) | `2705bea4842ab7fb9f3713d11eba873d07e143154b115e349286c0af16ca03aa` | **実行確認済み**（Git登録対象・v1.1非累積3Dスライス表） |
| 第2工程 | `output_eurusd_is_plateau_20261109_060458/is_outcomes_eurusd.csv` | 6,733 rows (2,058,533 B) | `121f7b5c960be92f08df9772302222465258fe2f161df07bdefc66d8ce68eefe` | **実行確認済み**（Drive保管 / Git除外） |
