# GSR-2026W49 週次統合総括書（執行監査・One-Shot OOS裁定・マルチフィキシングIS審査）

🏷️ [TRACE: GSR-202611-W5-FRI | 正式棄却 (GSR-TKYFIX-002 OOS, GSR-LDNFIX-001, GSR-NYCUT-001) / 保留 (GSR-TKYFIX-003) | GSR-2026W49 週次統合総括]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: GSR-2026W49; GSR-202611-W5-WED; MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md; spark_audit_handover_manifest_gsr_2026w49.json
record_id: GSR-202611-W5-FRI
session_title: GSR-2026W49 週次統合総括書（2026-11-27）
case_id: GSR-202611-W5-FRI
decision: REJECTED (GSR-TKYFIX-002 OOS, GSR-LDNFIX-001, GSR-NYCUT-001) / HOLD (GSR-TKYFIX-003)
oos_locked: true
-->

- **作成日**: 2026-11-27 (JST)
- **監査対象**: `GSR-2026W49`（2026-11-26 05:04:58 JST ローカル3通貨計775MB生M1全量実測確定版）
- **Spark監査ログ状態**: `GSR-202611-W5-WED-SPARK` は Drive 未検出（`unknown`）のため、第2工程確定マニフェスト（`spark_audit_handover_manifest_gsr_2026w49.json`）および確定集計CSV 3本から直接5ゲート監査を実施。

## 1. Track A & Track B 定量結果総括（1.85ペイアウト / 損益分岐 54.0541% / 同値LOSE）

| 候補 / コホート | $n$ | +0.1p 勝率 | +0.1p EV | +0.1p $\text{CLB}_{97.5\%,t}$ | +0.2p 勝率 | +0.3p 勝率 | 対NONE差 | 判定 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `GSR-TKYFIX-002` OOS `PURE_STRONG` | 256 | 55.0781% | +0.018945 | -0.097593 | 53.1250% | 52.7344% | -4.5013%pt | **REJECTED** |
| └ OOS `NONE (CONTROL_ONLY)` | 428 | 59.5794% | +0.102220 | +0.017169 | 58.8785% | 58.6449% | 0.0000%pt | 対照群 |
| └ OOS `SELL`（副次診断） | 113 | 65.4867% | +0.211504 | +0.064081 | 62.8319% | 62.8319% | +5.9073%pt | 参考記録（事後採用禁止） |
| └ OOS `BUY`（副次診断） | 143 | 46.8531% | -0.133217 | -0.335945 | 45.4545% | 44.7552% | -12.7263%pt | 崩壊確認 |
| `GSR-LDNFIX-001` EURUSD `PURE_STRONG` | 420 | 58.5714% | +0.083571 | -0.016274 | 57.3810% | 55.4762% | -4.2089%pt | **REJECTED**（対NONE負） |
| `GSR-LDNFIX-001` GBPUSD `PURE_STRONG` | 462 | 58.6580% | +0.085173 | +0.008275 | 57.7922% | 57.1429% | -1.4787%pt | **REJECTED**（対NONE負） |
| `GSR-NYCUT-001` EURUSD `PURE_STRONG` | 392 | 48.2143% | -0.108036 | -0.202821 | 47.7041% | 46.9388% | -5.2688%pt | **REJECTED** |
| `GSR-NYCUT-001` USDJPY `PURE_STRONG` | 399 | 47.3684% | -0.123684 | -0.219114 | 45.6140% | 44.6115% | -5.2758%pt | **REJECTED** |
| `GSR-TKYFIX-003` USDJPY `PURE_STRONG` | 359 | 60.4457% | +0.118245 | +0.020013 | 59.6100% | 57.9387% | +6.9498%pt | **HOLD**（Spark監査待ち） |

## 2. プログラム資産の4段階確認区分

| ファイル名 | 確認区分 | SHA256 | 変更差分・未実施事項 |
| :--- | :--- | :--- | :--- |
| `profile_market_structure_gsr_2026w49_v1_0.py` | **実行確認済み** | `f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b` | 第1工程 775MB実測完了 |
| `gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py` | **実行確認済み** | `2b9c5017abd9f723536f05bd4f362888642af6b9cc53e0e107a412407a9ca479` | 第2工程 775MB実測完了 |
| `oos_tkyfix002_standalone_and_diagnostics_gsr_2026w49.csv` | **実行確認済み** | `1483b04b0f6f5e2c09e6d9aa36b5829534eee6d6385eff560f52acbf294190f1` | Track A 軽量集計CSV（Drive版実測値） |
| `is_multifix_standalone_and_ablation_gsr_2026w49.csv` | **実行確認済み** | `63e602fbe2b21321d85adb299299db82b0319ab33262c81efbf564b4e2884a8a` | Track B 軽量集計CSV（Drive版実測値） |
| `is_multifix_disjoint_slices_and_yearly_gsr_2026w49.csv` | **実行確認済み** | `80cad076b09fb835356f838074307e1295edaf4e95729eb9d80534528f5ab164` | Track B 非累積スライスCSV（Drive版実測値） |
| `spark_audit_handover_manifest_gsr_2026w49.json` | **現行版確認済み** | `e50c86b03a3acd954175101297495378e3e541352a909b1b7d5e3ff87aed5354` | 2026-11-26 05:04:58 JST 確定版 |
| `GSR-2026W49_Stage2_OOS_and_MultiFix_Report.md` | **静的確認済み** | `50744a7fddd5afbe76244ef3d4eadb81b8e7c177d64ae7cafdcad322654c3f96` | クラウド先行版（実測値はmanifest/CSVを参照） |
| `GSR-202611-W5-WED-SPARK.md` | **未確認（`unknown`）** | `unknown` | Spark独立監査ログ未発行 |
| `GSR_TKYFIX_002.mq4` / `.ex4` | **作成中止（凍結）** | `unknown` | OOS棄却によりEA実装見送り |

<!-- RESEARCH_TRACE_END -->
