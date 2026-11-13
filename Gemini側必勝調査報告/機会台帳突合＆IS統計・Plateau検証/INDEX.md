# 機会台帳突合＆IS統計・Plateau検証 INDEX

最終更新: 2026-11-08 JST

## 1. 標準検証テンプレート・マスターコンテキスト（2026-11-08 配備）
- 共通マスターコンテキスト（上位正本）: `..\..\QUANT_PYTHON_MASTER_CONTEXT.md`
  - バージョン: `v2.2`（`WEEKLY_SURVEY_STAGE1` / `BO_STANDARD` / `BO_ONETOUCH` / `FX_EXPANSION` 対応）
  - SHA256 (lower): `89f9c215a02717b1057cd14fa9167b5b8cb7fbc37e60760dbe5f572c2bbb9d13`
  - SHA256 (UPPER): `89F9C215A02717B1057CD14FA9167B5B8CB7FBC37E60760DBE5F572C2BBB9D13`
  - 確認状態区分: `現行版確認済み`（2026-11-08 JST / SHA256照合完了）
- 第2工程 標準検証テンプレートスクリプト: `templates/stage2_standard_validator.py`
  - 用途: Gate 1（OOSロック・台帳一致）、Gate 2 & 5（HAC信頼下限・+0.1〜+0.3 pip摩擦）、Gate 3（非累積マージナルPlateau）、Spark監査引き継ぎマニフェスト（JSON）自動生成
  - SHA256 (lower): `a0c3a1233257248b17d3fff5c4a7012fba36f3d3f6cfb500800e8d8fb22a810e`
  - SHA256 (UPPER): `A0C3A1233257248B17D3FFF5C4A7012FBA36F3D3F6CFB500800E8D8FB22A810E`
  - 確認状態区分: `静的確認済み`（2026-11-08 JST / 標準骨格テンプレート配備・SHA256照合完了）

## 2. 検証・引き継ぎルール（v2.2 統合規定）
1. 第1工程の最新 `opportunity_ledger.csv`（および `トレード手法の市場調査＆データ点検\INDEX.md` 記載のSHA256）との100%一致（Gate 1）を前提とする。
2. OOS期間（2022–2026）は引き続きロック維持とし、本フォルダ内のいかなるスクリプトでも開封してはならない。
3. 累積条件（`<=` 等）の入れ子による「擬似プラトー」や局所スパイク（$n < 30$）の重複カウントは即棄却（FAIL）とし、必ず非累積の周辺分布（マージナル）と Control群に対する増分を検証する。

---

## 3. 完了・凍結済み検証アーカイブ（再検証禁止）
### BO-EUR-005（2026-04-16 第2工程完了 ➔ 第3工程にて正式棄却・開発凍結済み）
- 統合検証レポート: `GSR-202604-W3-S2_opportunity_ledger_is_plateau_audit.md`
  - 対象案件: `BO-EUR-005`（親案件: `GSR-202604-W3`）
  - 最終ステータス: **正式棄却・開発凍結**（第3工程 `BO-EUR-005_decision.md` にて 5ゲート審査 1/5通過・4/5不通過により確定 / OOS期間 2022–2026 未開封ロック維持）
- 実行スクリプト・成果物（リポジトリ側正本履歴）:
  - 第1工程機会台帳: `opportunity_ledger.csv`（SHA256: `587a24f4e0a0ba60163fb3f6ca7ddca77220264a020fb2c87113b8bf91632227`）
  - 検証スクリプト: `scripts/validate_is_plateau_eurusd_m1.py`（SHA256: `e35284266ee34dd91a1c3f1837352f460fd423c36c077e396045eb9484d9f162`）
  - 432セル全グリッド結果: `data/results/bo_eur_005_is_plateau_grid_432.csv`（SHA256: `92d0d4d88c4b62aa60d2e297d19be318cc4853a60351d526da5c7011647da337`）
  - 12組ベースライン集計: `data/results/bo_eur_005_is_baseline_12.csv`（SHA256: `2d4e29a8f10a3b07fd4e6fa001ab828294c8dc09ddda68ae22a6668d21445074`）
  - 周辺（マージナル）安定性集計: `data/results/bo_eur_005_is_marginal_summary.csv`（SHA256: `2f02849ce9c38315599220e026f7bf118a3918d375b459e15cc800dd8c5e3a48`）
  - Spark監査引き継ぎマニフェスト: `data/results/spark_audit_handover_manifest.json`（SHA256: `c3734525d761a14a4483a76a6c30ab74f3b49b0363cf5f57b1b423bf0efeb784`）
---

## 4. GSR-2026W47 第2工程 実行済み正本資産（2026-11-10 07:05 JST 確定）
- 検証スクリプト: gsr_2026w47_is_plateau_verifier_v1_0.py (v1.0.0 / 実行確認済み)
  - SHA256: 0e888bc1e4926d6d41d7cbd16d46c78d01c4c2b1a2e21a2ad1fe5e08f439fc2f
- 出力フォルダ: output_gsr_2026w47_is_plateau_20261110_070559
- 検証結果CSV（3種）:
  1. Standalone & Ablation集計: is_standalone_and_ablation_summary_gsr_2026w47.csv（SHA256: ba83b1a2a5e5c6543634d721bf5ab1e68d42e2bd3e0d7ecd3013c1d052ff375d）
  2. 非重複(Disjoint) 3D 64セル格子: is_disjoint_3d_grid_gsr_2026w47.csv（SHA256: e2ed1b6edd958492541d9deb1e215ea4fec1cd3df26bd26517210e5bbea1926e）
  3. 非累積1次元マージナル＆年次分解: is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv（SHA256: 0d9038e743d0af17643e1c191528be1bdca678cdfe3001c25d14bc2f85626bfb）
- Spark引き継ぎマニフェスト: spark_audit_handover_manifest_gsr_2026w47.json
