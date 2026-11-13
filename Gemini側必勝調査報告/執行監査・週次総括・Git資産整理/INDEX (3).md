# INDEX — 執行監査・週次総括・Git資産整理（Gemini側必勝調査報告：第3工程）

- **保管パス（第3工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理`
- **関連パス（第1工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検`
- **関連パス（第2工程）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証`
- **共通マスターコンテキスト**: `..\..\QUANT_PYTHON_MASTER_CONTEXT.md`（v2.2 / SHA256: `89f9c215a02717b1057cd14fa9167b5b8cb7fbc37e60760dbe5f572c2bbb9d13`）
- **専用TRACE採番規約**: `GEMINI_DISCOVERY_TRACE_RULE.md`（SHA256: `fd70c9e64015404b8c324a03a62135a4b1f3229f5f8100d157d139c25517a4d6`）
- **最終更新日**: `2026-11-13 JST`

---

## 1. GSR-2026W47 最終5ゲート判定＆総監督最終裁定サマリ（2026-11-13 確定）

| 専用案件コード (`case_id`) | 対象市場・時間足 | 戦略・モデル概要 | Spark監査判定 (`GSR-202611-W3-WED-SPARK`) | 総監督 最終裁定 | 次工程処置・OOSロック状態 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`GSR-EXHAUST-001`**<br>（親: `GSR-2026W47`） | `EURUSD` / `USDJPY` M1 | M1 BB $\pm 2.5\sigma$ 到達後の切り下げ反転 | `FAIL` | **棄却・凍結 (`FAIL`)** | 逆アブレーション（`-2.40%pt`）、$\text{CLB}_{97.5\%} < 0$（`-0.0960` / `-0.1060`）、値幅中央値 `0.0〜0.1 pip` による摩擦崩壊（TRAP-05）。**即時開発凍結・再検証およびパラメータ延命厳禁**。 |
| **`GSR-SHOCKDECAY-001`**<br>（親: `GSR-2026W47`） | `EURUSD` / `USDJPY` M1 | M1大陽線・大陰線（$\ge 2.2\text{ ATR}$）直後の値幅収縮逆張り | `FAIL` | **棄却・凍結 (`FAIL`)** | 逆アブレーション（`-0.32%pt` / `-0.45%pt`）、$\text{CLB}_{97.5\%} < 0$（`-0.0727` / `-0.0704`）、値幅中央値 `0.1 pip` による摩擦崩壊（TRAP-05）。**即時開発凍結・再検証およびパラメータ延命厳禁**。 |
| **`GSR-TKYFIX-001`**<br>（親: `GSR-2026W47`） | `USDJPY` M1 | 東京仲値（09:55 JST）直前15分偏り＋09:54確定足ヒゲ拒絶5分逆張り | `HOLD` | **保留・IS内追加検証 (`HOLD`)** | 値幅中央値 `+0.50 pip`、`+0.1p` 勝率 `57.40%`（正のアブレーション `+3.02%pt`）、`+0.2p` 勝率 `55.62%`、`+0.3p` 勝率 `55.26%` と全摩擦水準で黒字維持。**OOS（2022年以降）未開封ロック維持のまま、IS（2015–2021）内追加検証 `GSR-TKYFIX-002`（実験A: TRAP-06排除 / 実験B: 15分変動幅下限分離 / 実験C: TRAP-07 64分割廃止・非重複粗視化）へ差配**。 |

---

## 2. 本フォルダ（第3工程：執行監査・週次総括・Git資産整理）保管ファイル一覧

| ファイル名 | 種別 | サイズ (bytes) | SHA256（実測値） | 確認状態区分 | 内容・用途 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GSR-2026W47_decision.md` | Markdown | 15,605 | `bd2a79abf080883828121c896041abdebf73441ebe877e1287269b467787ddd7` | **`確定済み`** | **`GSR-2026W47` 公式決定記録**（最終5ゲート判定・`GSR-EXHAUST-001`/`GSR-SHOCKDECAY-001` 凍結・`GSR-TKYFIX-002` 実験A/B/C契約） |
| `GSR-2026W47_Executive_Audit_and_Weekly_Summary_2026-11-13.md` | Markdown | 4,671 | `31ad4595f20f3a2c08934646d10e702f2ff44db5ee62342beb875b066a07df27` | **`確定済み`** | **`GSR-2026W47` 週次総括・執行監査統合報告書** |
| `git_commit_gsr_2026w47.ps1` | PowerShell | 19,912 | `364bafc00878e04d8377ec8389a4afc85c0592ac659e24eb8b562d90a81210d3` | **`確定済み`** | **ローカルGit（`C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery`）＆Gドライブ2段階同期・`00_Project_Control` 格納・`git push origin main` 自動化スクリプト（正本）** |
| `sync_gsr_2026w47_assets_and_git_commit.ps1` | PowerShell | 14,133 | `8e167bea874da509e7f1f79b0a51e7d6176778b5a0fcb0188732a05863c60837` | **`確定済み`** | `GSR-2026W47` 全3工程のSHA256再照合・`INDEX.md` 最新化・大容量CSV除外Gitコミット自動化スクリプト |
| `DECISION_TEMPLATE.md` | Markdown | 4,722 | `54fb98188956c831fd3489c50481404edbe4ad4e0308de135d9bf5aa11044c0d` | `確定済み` | `GSR-*` 専用コード＆非累積マージナル対応 `decision.md` 標準テンプレート |
| `GEMINI_DISCOVERY_TRACE_RULE.md` | Markdown | 3,082 | `fd70c9e64015404b8c324a03a62135a4b1f3229f5f8100d157d139c25517a4d6` | `現行版確認済み` | 専用TRACEコード（`GSR-*`）採番規約 |
| `GSR-2026W46_decision.md` | Markdown | 12,747 | `04de62ca61d43a89eb66835d2da357c76edaa79288c56d9cfe2221d743201bea` | `確定済み（アーカイブ）` | 前週 `GSR-2026W46`（EURUSD 3候補＆既存EA 6分満期バグ監査）最終棄却決定記録 |
| `BO-EUR-005_decision.md` | Markdown | 8,961 | `2d0e2e05b8dcd86c2993b2e0fea0f8c8505d609e654a5110ce49e7882c255109` | `確定済み（アーカイブ）` | 過去参照 `BO-EUR-005` 最終棄却決定記録 |

---

## 3. GSR-2026W47 全3工程横断 スクリプト・ドキュメント・証跡SHA256一覧

| 保管工程 | ファイル名 | 版 / 規模 | SHA256（実測値） | 確認状態区分（手順書8原則） | Git登録区分 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 第1工程 | `profile_is_market_structure_gsr_2026w47_v1_0.py` | v1.0.2 (14,105 B) | `d3f4ba214a79bb41e38313a1dbd307afff4a303ef836bee3d922ed77619bc5a1` | **`実行確認済み`** | **Git登録（正本コード）** |
| 第1工程 | `stage1_to_stage2_handover_manifest_gsr_2026w47.json` | JSON (2,385 B) | `37a8842b0d34471d3adeeafac241279c85ab19fcb099b28f9155128c990b969c` | **`実行確認済み`** | **Git登録（軽量マニフェスト）** |
| 第1工程 | `is_2015_2021_opportunity_ledger_gsr_2026w47.csv` | 99,945 rows (26,659,086 B) | `7f8581b693da499064dd3d0aaee2f20c2babc84d8859dfd852c923b5f91c7d38` | **`実行確認済み`** | **Git除外（大容量CSV / Drive保管）** |
| 第1工程 | `INDEX.md`（第1工程・2026-11-13更新版） | Markdown | `ca89798acda5104ea34950450912002f9a37e30ee5c1c54953a51acb279626ae` | **`現行版確認済み`** | **Git登録（索引）** |
| 第2工程 | `gsr_2026w47_is_plateau_verifier_v1_0.py` | v1.0.0 (14,471 B) | `0e888bc1e4926d6d41d7cbd16d46c78d01c4c2b1a2e21a2ad1fe5e08f439fc2f` | **`実行確認済み`** | **Git登録（正本コード）** |
| 第2工程 | `GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md` | Markdown (25,996 B) | `1acd59bbe6223985aaa8335dc7b27be7287703a484ce1ae890c9d1240a410118` | **`実行確認済み`** | **Git登録（検証報告）** |
| 第2工程 | `spark_audit_handover_manifest_gsr_2026w47.json` | JSON (10,363 B) | `ad1b5c8b7b4b5ae430774c96f13e10759697de227f77e9e4edcf4fd62dc8e2eb` | **`実行確認済み`** | **Git登録（軽量マニフェスト）** |
| 第2工程 | `is_standalone_and_ablation_summary_gsr_2026w47.csv` | 15 rows (2,671 B) | `ba83b1a2a5e5c6543634d721bf5ab1e68d42e2bd3e0d7ecd3013c1d052ff375d` | **`実行確認済み`** | **Git登録（軽量集計CSV）** |
| 第2工程 | `is_disjoint_3d_grid_gsr_2026w47.csv` | 239 rows (33,065 B) | `e2ed1b6edd958492541d9deb1e215ea4fec1cd3df26bd26517210e5bbea1926e` | **`実行確認済み`** | **Git登録（軽量集計CSV）** |
| 第2工程 | `is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv` | 108 rows (8,677 B) | `0d9038e743d0af17643e1c191528be1bdca678cdfe3001c25d14bc2f85626bfb` | **`実行確認済み`** | **Git登録（軽量集計CSV）** |
| 第2工程 | `INDEX.md`（第2工程・2026-11-13更新版） | Markdown | `d4783d30c631f6bbeed21e41f74440f9811ff8b8ec2c47c554cc4cf8b17e8a18` | **`現行版確認済み`** | **Git登録（索引）** |
