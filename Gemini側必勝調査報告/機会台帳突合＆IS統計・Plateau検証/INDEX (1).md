# 機会台帳突合＆IS統計・Plateau検証 INDEX

最終更新: 2026-11-25 JST

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

---

## 5. GSR-2026W48 第2工程 完了記録（2026-11-18 確定 ➔ 第3工程にて `PASS_CANDIDATE` 承認）
- 対象候補: `GSR-TKYFIX-002`（USDJPY M1 東京仲値 `PURE_STRONG`, IS $n=360$）
- 最終裁定: `GSR-2026W48_decision.md`（SHA256: `550824ec4adca228ccf641ea5cd5c9e260085ad3cff1ab6ec86d2a6e8c5be640`）にてプロジェクト初のIS全5ゲート完全合格・One-Shot OOS初回開封申請承認。

---

## 6. GSR-2026W49 第2工程 成果物レジストリ（2026-11-25 更新 / v1.2規定準拠）
- **対象トラック**:
  - **Track A（承認済み One-Shot OOS 2022–2026）**: `GSR-TKYFIX-002`（USDJPY, $n=774$ / 主契約 `PURE_STRONG` $n=256$）
  - **Track B（IS 2015–2021専用 / `oos_locked_for_track_b: true`）**: `GSR-TKYFIX-003` (USDJPY), `GSR-LDNFIX-001` (EURUSD/GBPUSD), `GSR-NYCUT-001` (USDJPY/EURUSD) — 全5,532 PASS行（`FAIL_GAP_T+6` 1件除外）
- **検証スクリプト**: `gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py`（SHA256: `2b9c5017abd9f723536f05bd4f362888642af6b9cc53e0e107a412407a9ca479`）
- **第2工程レポート**: `GSR-2026W49_Stage2_OOS_and_MultiFix_Report.md`（SHA256: `50744a7fddd5afbe76244ef3d4eadb81b8e7c177d64ae7cafdcad322654c3f96`）
- **軽量集計CSV（3点）**:
  1. `oos_tkyfix002_standalone_and_diagnostics_gsr_2026w49.csv`（SHA256: `0518271ecbe46e5b4a2293ae66123c1753c4396f2b6b14fdce74d490b5d4951e`）
  2. `is_multifix_standalone_and_ablation_gsr_2026w49.csv`（SHA256: `5fb81723968a979952372852e625569d64cd70c9baa897651f1adbc17856d2db`）
  3. `is_multifix_disjoint_slices_and_yearly_gsr_2026w49.csv`（SHA256: `b612f745b5141b7c1bfea181c1af8bffb96f7e30a6c6a160f774eea72fcf2a55`）
- **Spark引き継ぎマニフェスト**: `spark_audit_handover_manifest_gsr_2026w49.json`（SHA256: `ac3c9004ecccd3b04efa043b513285160d489a0b42db18859501da04fe63ab18`）
