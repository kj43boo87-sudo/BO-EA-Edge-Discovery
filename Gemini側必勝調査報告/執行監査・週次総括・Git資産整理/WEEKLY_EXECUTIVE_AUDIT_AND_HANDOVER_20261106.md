🏷️ [TRACE: BO-EUR-005 | 棄却 | 執行監査・週次総括・最終5ゲート判定・Git資産整理（2026年11月第1週）]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery
trace_namespace: BOEA
source_trace_refs: BOEA / BO-EUR-005、BOEA / BO-EUR-004、Gemini_Role_Prompt_v2_2026-09-28.md (TR-20261025-v1)、プログラム資産管理手順.txt、機会台帳突合＆IS統計・Plateau検証/BO-EUR-005_decision.md、BO-EUR-005_Spark_Audit_and_Handover_Log_2026-11-05.md、トレード手法の市場調査＆データ点検/HANDOVER_Market_Survey_and_Data_Audit_20261105.md
record_id: unknown
session_title: 執行監査・週次総括・最終5ゲート判定・Git資産整理（2026年11月第1週）
case_id: BO-EUR-005
parent_case_id: BO-EUR-004
decision: 棄却
target_market: EURUSD_1M
attachment_file: WEEKLY_EXECUTIVE_AUDIT_AND_HANDOVER_20261106.md, BO-EUR-005_decision.md, DECISION_TEMPLATE.md, sync_weekly_assets_and_git_commit.ps1, INDEX.md
part_info: 1/1
timestamp: 2026-11-06 05:32:40 JST
-->
所属プロジェクト: BO・EA Edge Discovery (edge-discovery)
TRACE区分: BOEA
参照元: BOEA / `BO-EUR-005`、BOEA / `BO-EUR-004`、`Gemini_Role_Prompt_v2_2026-09-28.md` (TR-20261025-v1)、`プログラム資産管理手順.txt`、`BO-EUR-005_decision.md`、`BO-EUR-005_Spark_Audit_and_Handover_Log_2026-11-05.md`、`HANDOVER_Market_Survey_and_Data_Audit_20261105.md`

# 執行監査・週次総括・Git資産整理 統合報告書（2026-11-06）

- **保管先（第3工程正本フォルダ）**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理`
- **対象週**: 2026年11月第1週（2026-11-01 〜 2026-11-06 JST）
- **今週の総括結論**:
  1. **`BO-EUR-005`（EURUSD M1境界再テストモデル：Control `I` / Candidate `R` / Candidate `B`）**: 第2・第3工程の最終5ゲート審査およびSpark独立性能監査を完了し、**IS期間（2015–2021年、1,050件）にて正式棄却・開発凍結（`VIEWED_EVAL` 2022–2026年 748件は未開封維持）**と確定。
  2. **次週継続の新規調査3案（`Proposal A / B / C`）および既存逆張りEA（5通貨ペア・60レポート）連続性点検**: 第1工程（`トレード手法の市場調査＆データ点検`）にて引数なし自動実行プロファイラ `profile_is_market_structure_2015_2021_v1_2.py`（SHA256: `a7fa4ada...`）を整備済み。ローカルM1データに対するLabel-Free機会台帳出力待ちのため、ゲート①〜⑤は**「追加検証（ISプロファイリング実行待ち）」**として次週へ引き継ぐ。

---

## 1. 今週の検証候補に対する最終5ゲート確認リスト

| 検証候補 / 案件ID | ① 機会台帳の一致・6分間連続性 | ② IS期間（2015–2021）HAC信頼下限 > 損益分岐54.054% | ③ 近傍Plateauの広さ（432セル×マージナル安定性） | ④ Spark監査での未来参照・選択バイアス有無 | ⑤ MT4での $t+1$ 分Open約定・スプレッド耐性（+0.1〜+0.3p） | 最終判定・処置 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`BO-EUR-005`**<br>EURUSD 東京箱ブレイク→再侵入（`I`）・境界再テスト反発（`R`）・再ブレイク（`B`） | **PASS**<br>`opportunity_ledger.csv`（`029f97ab...`）全4,264日 / IS 2,551日完全一致、重複0、Label-free確認済み。IS有効機会 `1,050/1,050`（欠損・OHLC違反0）。 | **FAIL（棄却決定因）**<br>・`I` ($n=604$): 勝率 `47.19%`, $\text{EV}=-0.1271$, $\text{CLB}_{97.5\%}=-0.2019$<br>・`R` ($n=210$): 勝率 `50.48%`, $\text{EV}=-0.0662$, $\text{CLB}_{97.5\%}=-0.1852$<br>・`B` ($n=236$): 勝率 `42.80%`, $\text{EV}=-0.2083$, $\text{CLB}_{97.5\%}=-0.3334$<br>全群 `NOT_ABOVE_ZERO`。 | **FAIL（擬似プラトー）**<br>432セル中 $\text{CLB}_{97.5\%}>0$ は **`0 / 432`（0.0%）**。`R` の3セル `STABLE_PLATEAU` も累積条件（`<=`）の入れ子と `retest==2`（$n=8$, 7勝1敗）の局所スパイクによる擬似プラトーと実証。 | **PASS（構造解明）**<br>未来参照なし。`B - I`（$\Delta\text{EV}=+0.3057$）は `I` 保有中に逆行再ブレイクした日における `I` の惨敗（勝率 `26.27%`）の裏返し。`R` の69.5%（`retest==1`, $n=146$）は `I` と勝率 `48.63%` で完全同一。 | **FAIL（摩擦崩壊）**<br>`+0.2 pip` で `R` の損益分岐超えは `6 / 192` セル、`+0.3 pip` で **`0 / 192` セル（完全消滅）**。5分値幅中央値が `+1.0 pt`（`+0.1 pip`）に張り付き、微細摩擦で崩壊。 | **棄却・凍結**<br>（`VIEWED_EVAL` 748件は未開封のまま開発終了） |
| **`Proposal_A`**<br>USDJPY 異市場比較：東京箱ブレイク失敗・即時実体再侵入（M5傾き・大実体フィルタ付） | **未計測（スクリプト整備済）**<br>第1工程 `profile_is_market_structure_2015_2021_v1_2.py` にてOOS遮断・6時刻連続性検査ロジック実装済み。※EURUSDの単純箱再侵入は `BO-EUR-005` 棄却により除外。 | **未計測（Label-Free段階）**<br>第1工程は勝敗・EVを計算しないLabel-Free台帳抽出フェーズ。 | **未計測**<br>第1工程で十分な母数（`valid_6bar_count`）が確認された後に第2工程で実施。 | **設計監査済（実測待ち）**<br>`M5_CloseTime <= M1_CloseTime` の確定足結合により上位足未来参照を遮断済み。 | **未計測**<br>第2工程にて `Open[t+1]` 参入・`+0.1〜+0.3 pip` 負荷で検証予定。 | **追加検証**<br>（第1工程ローカル実行待ち） |
| **`Proposal_B`**<br>クロス円（USDJPY / EURJPY / AUDJPY）確定M5非トレンド限定・M1 BB 2.8σクライマックス逆張り | **未計測（スクリプト整備済）**<br>第1工程スクリプトに単発独立化（5分重複保有禁止）と $t \sim t+6$ 連続性検査を実装済み。 | **未計測（Label-Free段階）**<br>IS期間（2015–2021）の機会件数・時間帯／ATR帯分布の抽出待ち。 | **未計測**<br>第2工程にてBB偏差・RSI・ヒゲ比率・M5 BB幅の近傍格子を検証予定。 | **設計監査済（実測待ち）**<br>既存EAの課題だった「5分以内の重複連打」を排除し、単発独立試行として設計済み。 | **未計測**<br>NYクローズ（21:00–23:59 UTC）および毎時55–59分を除外してスプレッド拡大を回避する設計。 | **追加検証**<br>（第1工程ローカル実行待ち） |
| **`Proposal_C`**<br>EURUSD / USDJPY / GBPUSD 確定M5 PO同調 × M1ボラ収縮後のEMA20反発確定 | **未計測（スクリプト整備済）**<br>第1工程スクリプトに実装済み。 | **未計測（Label-Free段階）**<br>IS期間（2015–2021）の機会件数抽出待ち。 | **未計測**<br>第2工程にてM5傾き・RSI調整閾値・ボラ比率 $VR_t$ の近傍格子を検証予定。 | **設計監査済（実測待ち）**<br>前足高安の実体ブレイク回復（$C_t > H_{t-1}$）確認後の `Open[t+1]` 参入とし、足内未確定エントリーのバイアスを排除済み。 | **未計測**<br>第2工程にて `+0.1〜+0.3 pip` 負荷で検証予定。 | **追加検証**<br>（第1工程ローカル実行待ち） |
| **既存逆張りEA群**<br>5通貨ペア・検証CSV 60件（`BO_BB3Sigma_Reversal_5M_*.csv`） | **点検コマンド整備済**<br>`--audit-reports-glob` による60ファイル一括の5分満期整合・生M1連続性照合を実装済み。 | **再集計待ち**<br>同値（0pt）および `+0.1 pip`（1pt）ストレス控除後の実効勝率をローカル一括算出予定。 | **対象外（既存固定レポート）**<br>通貨ペア・設定別の成績一覧化と現行ソース（`.mq4`）のSHA256対応付けを実施予定。 | **要注意（5分内重複検査）**<br>連打による相関取引（`Overlap5m`）の件数を分離集計するロジックを実装済み。 | **点検待ち**<br>`Tie`（同値負け）と `1ptWin`（0.1pipストレスで負け転落する取引）の件数を抽出予定。 | **追加検証**<br>（ローカル点検実行待ち） |

---

## 2. 今週のプログラム・ドキュメント資産棚卸し（全3工程・SHA256実測確認済み）

`プログラム資産管理手順.txt`（規則1・2・4・5）に基づき、今週作成・更新したスクリプト（`.py` / `.ps1`）およびドキュメント（`.md`）のSHA256ハッシュと確認状態を以下に確定します。

| 工程フォルダ | ファイル名 | 種別 | サイズ (bytes) | SHA256（実測値） | 確認状態 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 第1工程：`トレード手法の市場調査＆データ点検` | `profile_is_market_structure_2015_2021_v1_2.py` | Python (v1.2.0) | 43,374 | `a7fa4ada92f47c5adb2d01db7e4c823bd8a5820fb06c23c2f13951027aaae2eb` | 静的確認済み・引数なし自動探索対応（ローカル実データ実行待ち） |
| 第1工程：`トレード手法の市場調査＆データ点検` | `profile_is_market_structure_2015_2021.py` | Python (v1.1.0 旧版保持) | 39,704 | `e37a9e62626d76ae90b7013de9842bcca007906cabad4b7e5afe0ca08d0111ce` | 旧版保全（規則5に基づく履歴保持） |
| 第2工程：`機会台帳突合＆IS統計・Plateau検証` | `bo_eur_005_is_plateau_verifier.py` | Python (v2.4) | 45,367 | `7c125ea7c02db45a2e2af779f9dc7af530639cf900a3109296667207689703a9` | **実行確認済み**（`outcomes_sha256` 正規ハッシュ `080dc7a3...` 統一版） |
| 第2・第3工程共通 | `BO-EUR-005_decision.md` | Markdown（決定記録） | 8,961 | `2d0e2e05b8dcd86c2993b2e0fea0f8c8505d609e654a5110ce49e7882c255109` | **確定済み**（`BO-EUR-005` 棄却・凍結の公式決定記録） |
| 第2・第3工程共通 | `BO-EUR-005_Spark_Audit_and_Handover_Log_2026-11-05.md` | Markdown（監査統合ログ） | 7,077 | `6c663ad984c4f68f998a8a8ad0881f8787d082c7f321b2dc54bfe765a5a24fad` | **確定済み**（Gemini引き継ぎ＋Spark独立監査全文＋執行監査） |
| 第2工程：`機会台帳突合＆IS統計・Plateau検証` | `INDEX.md` | Markdown（第2工程索引） | 2,539 | `c88aaf555db62cab8edee2cadaf8daa2ba2eef2e9b56647bcd3662678c9ad0d1` | 確認済み |
| 第3工程：`執行監査・週次総括・Git資産整理` | `DECISION_TEMPLATE.md` | Markdown（決定記録テンプレート） | — | 本フォルダの `INDEX.md` に記載 | 今週新規整備 |
| 第3工程：`執行監査・週次総括・Git資産整理` | `sync_weekly_assets_and_git_commit.ps1` | PowerShell（Git整理スクリプト） | — | 本フォルダの `INDEX.md` に記載 | 今週新規整備 |
<!-- RESEARCH_TRACE_END -->
