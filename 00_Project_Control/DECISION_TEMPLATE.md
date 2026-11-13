# {CASE_ID} Decision Record — {MODEL_TITLE}

- **Case ID**: `{CASE_ID}`（親案件: `{PARENT_CASE_ID}`）
- **Project**: `BO・EA Edge Discovery` (`project_id: edge-discovery` / `trace_namespace: {BOEA_OR_BOOT}`)
- **Decision Date**: `{YYYY-MM-DD}`
- **Final Status**: **{採用候補 (ADOPT_CANDIDATE) / 棄却・凍結 (REJECTED_FROZEN) / 保留 (HOLD) / 追加検証 (FURTHER_VERIFICATION)}**
- **Development Status**: `{EA仕様化進行 / 終了・開発凍結 / 条件固定待ち / IS再検証中}`
- **Audit Status**: `{Gemini統計検証・Spark独立監査・執行監査 完了 / 部分確認済み・未完了事項を保持}`
- **Evaluated Scope**: In-Sample (`2015-01-01` .. `2021-12-31`, `{CALENDAR_DAYS}` calendar days / `{VALID_N}` valid opportunity instances)
- **Holdout Protection**: Out-of-Sample / `VIEWED_EVAL` (`2022-01-01` .. `2026-12-31`, `{OOS_ROWS}` rows) **{Unopened / Masked / 既閲覧区間として分離管理}**
- **確定者**: 中村さん / **記録担当**: `{Gemini / Scout / Spark / Champ}`

---

## 0. 公式TRACE記録ブロック（4者連携・掲示板転記用）

```text
🏷️ [TRACE: {CASE_ID} | {採用 / 棄却 / 保留 / 追加検証} | {SESSION_TITLE}]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery
trace_namespace: BOEA
source_trace_refs: {BOEA / {CASE_ID}、参照ファイル名・版・SHA256}
record_id: unknown
session_title: {SESSION_TITLE}
case_id: {CASE_ID}
parent_case_id: {PARENT_CASE_ID}
decision: {採用 / 棄却 / 保留 / 追加検証}
target_market: {PAIR_TIMEFRAME}
attachment_file: {CASE_ID}_decision.md
part_info: 1/1
timestamp: {YYYY-MM-DD HH:MM:SS JST}
-->
所属プロジェクト: BO・EA Edge Discovery (edge-discovery)
TRACE区分: BOEA
参照元: {BOEA / {CASE_ID}、評価契約・機会台帳・検証スクリプト・Spark独立監査ログ}

【最終決定要旨】
- 判定: {採用候補 / 棄却・凍結 / 保留 / 追加検証}
- 最終5ゲート結果: ①台帳一致[{PASS/FAIL/HOLD}] / ②IS HAC下限>54.054%[{PASS/FAIL/HOLD}] / ③近傍Plateau[{PASS/FAIL/HOLD}] / ④Spark監査[{PASS/FAIL/HOLD}] / ⑤MT4 t+1約定・スプレッド耐性[{PASS/FAIL/HOLD}]
- 2022年以降（OOS / VIEWED_EVAL）保護状態: {未開封維持 / 既閲覧のため独立OOS扱い禁止}
<!-- RESEARCH_TRACE_END -->
```

---

## 1. 4者合意・最終判定サマリ

| 役割 | 担当 | 判定 | 根拠要約 |
| :--- | :--- | :--- | :--- |
| 機会台帳・基準実装 | Scout / Codex | `{完了 / 保留}` | 機会台帳CSV（SHA256: `{LEDGER_SHA256}`）および評価契約JSON（SHA256: `{CONTRACT_SHA256}`）に基づく整数ポイント演算・Label-free台帳・基準群非破壊保持の確認結果。 |
| 統計検証・Plateau分析 | Gemini | `{採用候補 / 棄却 / 保留 / 追加検証}` | IS期間（2015–2021）における0.1 pipストレス控除後・同値LOSE・ペイアウト1.85倍（損益分岐 `54.054%`）での勝率、EV、Newey-West HAC 97.5%信頼下限（$\text{CLB}_{97.5\%}$）、および多次元Plateau格子の結果。 |
| 独立性能・過剰適合監査 | Spark | `{PASS_CANDIDATE / FAIL / HOLD}` | 独立再計算による数値一致確認、ペア比較や累積格子のマージナル（増分）分解、擬似プラトー・極小サンプルスパイク・未来参照・事後選択バイアスの有無。 |
| 執行監査・週次総括 | Gemini / Champ | `{次工程承認 / 開発終了承認 / 保留}` | 最終5ゲート確認結果、MT4での `Open[t+1]` 約定・`+0.1〜+0.3 pip` スプレッド耐性、およびOOS未開封保護の最終確認。 |

---

## 2. 最終5ゲート確認結果（Executive Gate Checklist）

1. **ゲート①：機会台帳（Opportunity Ledger）の一致・データ完全性 — `[{PASS / FAIL / HOLD}]`**
   - 入力台帳（`{LEDGER_FILE}`, SHA256: `{LEDGER_SHA256}`）の総日数 `{TOTAL_DAYS}` 日（IS `{IS_DAYS}` 日）、日付重複 `0`、未来ラベル混入 `0`（Label-free）、対照群の非破壊保持を確認。
   - 6分間連続性（判断足 $t$、エントリー足 $t+1$、中間足 $t+2 \sim t+5$、満期足 $t+6$ の1分刻み連続およびOHLC整合性）：有効 `{VALID_N}` 件 / 除外 `{INVALID_N}` 件（除外理由内訳：`{INVALID_REASONS}`）。
2. **ゲート②：IS期間（2015–2021）のHAC信頼下限 > 損益分岐54.054%（$\text{EV} > 0$） — `[{PASS / FAIL / HOLD}]`**
   - 評価前提：ペイアウト `1.85倍`（損益分岐勝率 `54.054%`）、同値 `LOSE`、`+0.1 pip` 代理ストレス控除。
   - 単独成績：$n = {VALID_N}$（`{WINS}`勝 `{LOSSES}`敗、同値 `{TIES}`件、1pt落ち `{STRESS_1PT}`件）、勝率 `{WIN_RATE}%`（損益分岐比 `{BE_DIFF}%pt`）、$\text{EV} = {EV}$、$\text{SE}_{\text{HAC}} = {SE_HAC}$、$\text{CLB}_{97.5\%} = {CLB975}$（$t = {T_STAT}$, `{ABOVE_ZERO_STATUS}`）。
   - 対照群比較（該当する場合）：$\Delta\text{EV} = {DELTA_EV}$、$\text{CLB}_{97.5\%} = {DELTA_CLB975}$。
3. **ゲート③：近傍パラメーターPlateauの広さ — `[{PASS / FAIL / HOLD}]`**
   - パラメーター格子総数 `{GRID_TOTAL}` セル中、$\text{CLB}_{97.5\%} > 0$ 達成セル：`{CLB_POS_CELLS} / {GRID_TOTAL}`、L1近傍の損益分岐超え比率 `{NEIGHBOR_BE_RATIO}%`。
   - 累積条件（`<=`）を除いたマージナル（増分）分解でも黒字が維持されるか、特定年のレジームや極小サンプル（$n < 30$）スパイクに依存していないかを確認。
4. **ゲート④：Spark監査での未来参照・選択バイアス有無 — `[{PASS / FAIL / HOLD}]`**
   - 特徴量の `source_time` / `available_at` と上位足確定条件（`CloseTime <= 判断時刻`）の遵守確認。
   - 5分以内の重複保有（Overlap）の有無、事後価格経路によるコホート選別（トートロジー）の有無、探索試行数（Multiple Testing）の記録。
5. **ゲート⑤：MT4での $t+1$ 分Open約定・スプレッド耐性（`+0.1`〜`+0.3 pip`） — `[{PASS / FAIL / HOLD}]`**
   - スプレッド・スリッページ負荷 `+0.1 pip` / `+0.2 pip` / `+0.3 pip` における損益分岐超えセル数の推移（`{BE_CELLS_01}` → `{BE_CELLS_02}` → `{BE_CELLS_03}`）。
   - 5分間の順行幅中央値と、MT4実機 / theoption提示価格での約定遅延・スプレッド拡大に対する生存性。

---

## 3. 入力原本・検証スクリプト・出力証跡のSHA256一覧

| 区分 | ファイル名 / パス | 行数・規模 | SHA256（実測値） | 確認状態 |
| :--- | :--- | :--- | :--- | :--- |
| 評価契約 | `{CONTRACT_FILE}` | JSON | `{CONTRACT_SHA256}` | `{確認済み / 未作成}` |
| 機会台帳 | `{LEDGER_FILE}` | `{LEDGER_ROWS}` rows | `{LEDGER_SHA256}` | `{確認済み / 未作成}` |
| 検証スクリプト | `{SCRIPT_FILE}` (`{VERSION}`) | `{SCRIPT_BYTES}` bytes | `{SCRIPT_SHA256}` | `{実行確認済み / 静的確認済み}` |
| 監査マニフェスト | `{MANIFEST_FILE}` | JSON | `{MANIFEST_SHA256}` | `{確認済み / 未作成}` |

---

## 4. 未完了事項・データ保全・次工程への引き継ぎ方針

1. **過去判定とOOS保護の維持**:
   - 棄却・凍結となった場合、現標本での閾値微調整や後付けフィルター追加による救済（データスヌーピング）は行わず、未使用のOOS / `VIEWED_EVAL` 期間は未開封のまま保持する。
   - 既に閲覧・探索した期間を、別案件で「未使用の独立OOS」と呼び直さない。
2. **原本・旧版の非破壊保全**:
   - 検証に使用した原データ、機会台帳、スクリプト、出力CSV/JSON、監査ログは削除・上書きせず、保管先フォルダおよびGit正本管理下に保持する。
3. **次工程アクション**:
   - `{採用候補の場合：独立OOSでの最終1回検証計画またはChampへのEA仕様化・実Tick約定監査依頼}`
   - `{棄却・凍結の場合：敗因メカニズムをINDEX.mdへ記録し、別市場・別構造の新規仮説へ移行}`
