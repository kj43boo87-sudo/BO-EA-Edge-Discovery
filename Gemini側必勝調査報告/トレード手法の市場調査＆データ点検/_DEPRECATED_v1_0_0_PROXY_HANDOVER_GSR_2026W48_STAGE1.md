🏷️ [TRACE: GSR-2026W48 | 追加検証 | GSR-2026W48 第1工程：GSR-TKYFIX-002専用Label-Free機会台帳生成・データ連続性点検・第2工程引継ぎ書]
<!-- RESEARCH_TRACE_START
ai_id: gemini
session_title: GSR-2026W48 第1工程：GSR-TKYFIX-002 IS内汚染除去検証用Label-Free機会台帳生成および自己反証ゲート点検
case_id: GSR-2026W48
parent_case_id: GSR-2026W47
decision: 追加検証
target_market: USDJPY_M1
attachment_file: is_2015_2021_opportunity_ledger_gsr_2026w48.csv
part_info: 1/1
timestamp: 2026-11-16 05:39:14
-->

# GSR-2026W48 第1工程 完了報告・第2工程引継ぎ書（GSR-TKYFIX-002 専用 Label-Free 機会台帳）

## 1. 準拠規定・親裁定・Gate 1 防壁ステータス

- **参照裁定・引継ぎ正本**:
  - 総監督最終裁定書: [`GSR-2026W47_decision.md`](https://drive.google.com/file/d/1GQEX0vbnugH2OOMZTwcUFvOB4J_XxyJM/view?usp=drivesdk)（リポジトリ同期版: [`GSR-2026W47_decision.md`](https://drive.google.com/file/d/1A4RP4P3oXCZNq1uqaIwau4sHAqt0Bn-U/view?usp=drivesdk), SHA256: `bd2a79abf080883828121c896041abdebf73441ebe877e1287269b467787ddd7`）
  - 第3工程→次週第1工程引継ぎ書: [`GSR-202611-W3-FRI_Stage3_to_Next_Monday_Stage1_Handover.md`](https://drive.google.com/file/d/1dXF0x0cOCPHYF247gGbezj89jMZ1rmKN/view?usp=drivesdk)
  - 運用規定・ロール定義 v1.1: [`MASTER_DIRECTOR_ROLE_PROMPT_v1.1.md`](https://drive.google.com/file/d/1lffdRanVHZOo3fu3bj1d00lZ1idxh03K/view?usp=drivesdk)
  - 前週第1工程プロファイラ・台帳正本: [`profile_is_market_structure_gsr_2026w47_v1_0.py`](https://drive.google.com/file/d/1dOEL78f4myvpdvur0Ny1ybp1fF97Fi3T/view?usp=drivesdk) / [`is_2015_2021_opportunity_ledger_gsr_2026w47.csv`](https://drive.google.com/file/d/1bUgKTFe155C2slXW202Pvq7DVlKk7ljh/view?usp=drivesdk) / [`stage1_to_stage2_handover_manifest_gsr_2026w47.json`](https://drive.google.com/file/d/1j6ULfP5HoEYK_Kdas3P67iyU8L0MGPGY/view?usp=drivesdk)
- **Gate 1（OOS完全遮断・凍結案件排除）監査結果**:
  - **対象生データ**: [`2026.10.16USDJPY(3)-M1-No Session.csv`](https://drive.google.com/file/d/1CjCXrVsAs-x9cC1e7UL16HNEfYHb-nNO/view?usp=drivesdk)（`258,871,846` bytes, SHA256: `aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29`）
  - **総行数**: `4,424,800` 行
  - **2014年以前除外行数**: `32,103` 行
  - **2022年以降 OOS 遮断行数**: `1,783,913` 行（`oos_locked: true` により完全未開封・遮断維持）
  - **IS採用行数（2015-01-01 〜 2021-12-31）**: `2,608,784` 行（OHLC論理矛盾 `0` 件、重複・逆転 `0` 件）
  - **棄却済み凍結案件の再検証禁止**: `GSR-EXHAUST-001`、`GSR-SHOCKDECAY-001`（および `GSR-CLIMAX-001` / `GSR-PULLBACK-001` / `GSR-FAKEOUT-001` / `BO-EUR-004` / `BO-EUR-005`）は完全凍結とし、今週は唯一摩擦耐性を示した東京仲値直前モデルの汚染除去検証 **`GSR-TKYFIX-002`** のみに専念。

## 2. GSR-TKYFIX-002 専用 Label-Free 機会台帳仕様と基礎件数集計

- **出力ファイル名**: `is_2015_2021_opportunity_ledger_gsr_2026w48.csv`
- **行数・カラム数**: 全 **`1,177` 行**（ヘッダー除く）× **厳密 `12` カラム**（勝敗・損益・ペイアウト・リターン等の結果列は **`0` 列**）
- **厳密12カラム構成**:
  1. `opportunity_id`: `GSR-TKYFIX-002-0001` 〜 `GSR-TKYFIX-002-1177`
  2. `trade_date`: 営業日（`YYYY-MM-DD`, JST）
  3. `entry_time`: 確定足次足始値時刻（`YYYY-MM-DD 09:55:00` JST / `Open[t+1]`）
  4. `eval_end_time`: 厳密5分満期時刻（`YYYY-MM-DD 10:00:00` JST / `Open[t+6]`）
  5. `direction`: 09:40〜09:54 JSTの15分間価格偏りに対する逆張り方向（`SELL`: `643` 件 / `BUY`: `534` 件）
  6. `pre_15m_range_pips`: 09:40〜09:54 JSTの15分間絶対変動値幅（`(High - Low)` in pips）
  7. `pre_15m_body_pips`: 09:40〜09:54 JSTの15分間始値〜終値変動幅（`|Close[09:54] - Open[09:40]|` in pips）
  8. `wick_rejection_ratio`: 09:54確定足における逆張り方向のヒゲ比率（`[0.0, 1.0]` 実数値）
  9. `wick_rejection_grade`: OR条件汚染（TRAP-06）分離用の純度区分（`PURE_STRONG`: `354` 件 / `WEAK_SUB`: `207` 件 / `NONE`: `616` 件）
  10. `day_of_week`: 曜日（`Mon`: `239` / `Tue`: `233` / `Wed`: `236` / `Thu`: `236` / `Fri`: `233`）
  11. `gotobi_flag`: ゴトー日および週末前倒し仲値日フラグ（`True`: `321` 件 / `False`: `856` 件）
  12. `m1_continuity_pass`: シグナル確定境界（`t`: 09:54 JST）から評価窓終了（`t+6`: 10:00 JST）までの6分間M1バー欠損なし判定（`True`: `1,177` 件 / `False`: `0` 件、有効連続率 **`100.0%`**）

### 2.1 年次別・ヒゲ純度区分（`wick_rejection_grade`）内訳表（Label-Free 件数のみ）

| 年次 (JST) | 総機会数 ($N$) | `PURE_STRONG` ($\text{wick} \ge 0.25$) | `WEAK_SUB` (TRAP-06 OR条件混入) | `NONE` (CONTROL_ONLY) | 6分間連続性 PASS ($n$) | 除外件数 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **2015** | 152 | 45 | 21 | 86 | 152 | 0 |
| **2016** | 189 | 53 | 32 | 104 | 189 | 0 |
| **2017** | 171 | 42 | 24 | 105 | 171 | 0 |
| **2018** | 158 | 40 | 30 | 88 | 158 | 0 |
| **2019** | 183 | 44 | 45 | 94 | 183 | 0 |
| **2020** | 169 | 61 | 28 | 80 | 169 | 0 |
| **2021** | 155 | 69 | 27 | 59 | 155 | 0 |
| **合計 (IS 7Y)** | **1,177** | **354** | **207** | **616** | **1,177 (100.0%)** | **0 (0.0%)** |

> **注記（境界値 `wick_rejection_ratio == 1.0000` の1件について）**:
> 前週 [`GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md`](https://drive.google.com/file/d/1TgDKNXCW0KyHhwrYhQbJyHa-nzN-bK4d/view?usp=drivesdk) および [`is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv`](https://drive.google.com/file/d/1D47Awffp4aJjurX5aYVrDZkgqUBOORfa/view?usp=drivesdk) において、`2021-02-11`（`GSR-TKYFIX-002-1047`）は `wick_rejection_ratio == 1.0000` であったため `pd.cut(..., right=False)` の右端境界で `bin_axis_3` が空欄となっていたが、実数値は `1.0000 >= 0.25` の完全なヒゲ拒絶バーであるため、`PURE_STRONG` は `B2_0.25_0.40`（`95` 件）+ `B3_0.40_0.55`（`130` 件）+ `B4_0.55_up`（`128` 件 + 境界 `1` 件 = `129` 件）の合計 **`354` 件**（うち `wick_rejection_ratio >= 0.40` は **`259` 件**）として1件の漏れもなく捕捉されている。

### 2.2 第2工程 事前固定3実験（実験A・実験B・実験C）のサンプルサイズ確認

| 実験区分 | 検証スライス / フィルタ条件 | 対象コホート | サンプル数 ($n$) | 第2工程での検証目的 |
| :--- | :--- | :--- | :---: | :--- |
| **実験A-0 (Baseline)** | `wick_rejection_grade in {PURE_STRONG, WEAK_SUB}` | 旧 `GSR-TKYFIX-001` CANDIDATE | **561** | TRAP-06混入時のベースライン確認 |
| **実験A-1 (Main)** | `wick_rejection_grade == 'PURE_STRONG'` (`wick >= 0.25`) | 純粋ヒゲ拒絶コホート（`WEAK_SUB` 207件除外） | **354** | OR条件汚染除去による $\text{CLB}_{97.5\%} > 0$ 到達検証 |
| **実験A-2 (Strict)** | `wick_rejection_grade == 'PURE_STRONG'` かつ `wick >= 0.40` | 強ヒゲ拒絶コホート | **259** | 高純度ヒゲ拒絶での単調性と摩擦耐性（+0.2p/+0.3p）検証 |
| **実験A-Trap (Ablation)** | `wick_rejection_grade == 'WEAK_SUB'` (`wick < 0.25`) | TRAP-06 OR条件単独混入コホート | **207** | 除外コホートが期待値足を引っ張っていたことの因果特定 |
| **実験B-1** | `PURE_STRONG` かつ `pre_15m_body_pips >= 3.0` | 中〜高モメンタム偏り + 純粋ヒゲ拒絶 | **313** | 2017/2019年の低ボラ減衰分離検証 |
| **実験B-2** | `PURE_STRONG` かつ `pre_15m_body_pips >= 4.0` | 高モメンタム偏り + 純粋ヒゲ拒絶 | **261** | 15分偏り下限引き上げ時のプラトー安定性検証 |
| **実験C-1 (Direction)** | `PURE_STRONG` × `direction` (`SELL` vs `BUY`) | 非重複2分割スライス | **183 / 171** | 仲値ドル買い偏り後の `SELL` 逆張り優位性と双方向性検証 |
| **実験C-2 (Gotobi)** | `PURE_STRONG` × `gotobi_flag` (`True` vs `False`) | 非重複2分割スライス | **98 / 256** | ゴトー日実需仲値フロー有無による構造差検証 |
| **実験C-3 (DayOfWeek)** | `PURE_STRONG` × `day_of_week` (`Mon`〜`Fri`) | 非重複5分割スライス | **65 / 69 / 65 / 81 / 74** | 曜日別の偏り・特定曜日依存の有無確認 |

---

## 3. 【必須】第1工程 自己反証ゲート（Label-Free Self-Ask 3問）

[`MASTER_DIRECTOR_ROLE_PROMPT_v1.1.md`](https://drive.google.com/file/d/1lffdRanVHZOo3fu3bj1d00lZ1idxh03K/view?usp=drivesdk) 第2.2節および第1工程指示書に基づき、機会台帳と引継ぎ書の確定前に以下の3問に対する自己反証チェックを実施した。

### 自問A（Label-Free純度）
> **「設定した特徴量と閾値は、IS期間の勝敗（Win/Loss）を一切見ずに、市場構造（ボラティリティ分位点や分布形状）の事前プロファイリングのみから決定したか？ 都合のよいピンポイント閾値になっていないか？」**

- **回答・検証根拠（PASS）**:
  1. **結果列の物理的ゼロ保証**: 生成スクリプト `profile_is_market_structure_gsr_2026w48_v1_0.py` には `write_opportunity_ledger_csv()` 内に禁止トークン検査（`win`, `loss`, `lose`, `payout`, `return`, `pnl`, `profit`, `outcome`, `hit`, `ev`, `wr`, `result`, `label`）を実装しており、出力CSV（`is_2015_2021_opportunity_ledger_gsr_2026w48.csv`）には09:55以降の価格や勝敗に関する列が一切存在しない。
  2. **事前固定された構造的分位点のみを使用**:
     - `wick_rejection_ratio` の境界値 `0.25` および `0.40` は、前週第1工程（[`profile_is_market_structure_gsr_2026w47_v1_0.py`](https://drive.google.com/file/d/1dOEL78f4myvpdvur0Ny1ybp1fF97Fi3T/view?usp=drivesdk)）で勝敗を見る前に設計された4分位ビン（`B1_sub0.25: <0.25`, `B2_0.25_0.40: [0.25, 0.40)`, `B3_0.40_0.55: [0.40, 0.55)`, `B4_0.55_up: >=0.55`）の境界そのものであり、事後的に1%刻みで探索したピンポイント閾値ではない。
     - `pre_15m_body_pips` / `pre_15m_range_pips` の下限候補（`2.0 pips`, `3.0 pips`, `4.0 pips`）も、総監督裁定書（[`GSR-2026W47_decision.md`](https://drive.google.com/file/d/1GQEX0vbnugH2OOMZTwcUFvOB4J_XxyJM/view?usp=drivesdk)）で事前固定された整数pipsグリッドに限定している。

### 自問B（未来参照の完全遮断）
> **「シグナル確定時刻 `t`（09:54確定足Close）の時点で、参照している全特徴量は `available_at <= t`（確定済みバーのみ）を満たしているか？ `Open[t+1]` 以降の価格情報が1ミリ秒でも特徴量計算に混入していないか？」**

- **回答・検証根拠（PASS）**:
  1. **タイムスタンプ因果境界の厳格分離**:
     - **特徴量計算窓（`available_at <= t`）**: すべての特徴量（`direction`, `pre_15m_range_pips`, `pre_15m_body_pips`, `wick_rejection_ratio`, `wick_rejection_grade`）は、`09:40:00` JST 〜 `09:54:00` JST の15本のM1バー（`09:54` バーが `09:55:00` JST 丁度に確定した時点のOHLC）および `09:40`〜`09:54` の14期間ATRのみから算出される。
     - **エントリー時刻（`t+1`）**: `entry_time = 09:55:00` JST（`Open[t+1]`）。
     - **満期判定時刻（`t+6`）**: `eval_end_time = 10:00:00` JST（`Open[t+6]`、厳密5分満期）。
  2. **評価窓バーの価格非参照**:
     - `m1_continuity_pass` の判定においては、`09:54`（`t`）〜`10:00`（`t+6`）の各1分足タイムスタンプの存在とOHLCフォーマット整合性のみをブール判定（`True`/`False`）し、`09:55` 以降のOpen/High/Low/Close価格値は特徴量計算に1ミリ秒たりとも参照・出力していない。

### 自問C（除外バイアス検査）
> **「6分間連続性チェック（`t`〜`t+6`）で除外された行が、特定の時間帯や急변相場（高ボラティリティ時）に偏っていないか？ 除外件数と理由がすべて追跡可能か？」**

- **回答・検証根拠（PASS）**:
  1. **除外件数ゼロ（有効連続率 100.0%）**:
     - IS期間（2015〜2021年）における `GSR-TKYFIX-002` 対象全 **`1,177` 件**のうち、`m1_continuity_pass == True` は **`1,177` 件（100.0%）**、`m1_continuity_pass == False`（欠損・ギャップ除外）は **`0` 件（0.0%）** である。
  2. **選択バイアス・生存バイアスの完全不存在**:
     - 東京仲値直前〜10:00 JST（00:54〜01:00 UTC）は東京市場のコア流動性時間帯であり、Dukascopy USDJPY M1生データにおいて7年間を通じて1分足の欠損が1件も発生していないため、高ボラティリティ時や特定年・特定曜日のデータ脱落による除外バイアスは完全にゼロである。

---

## 4. ローカルPCでのワンコマンド再生成・検証手順（Windows PowerShell）

ローカルPCの [`2026.10.16USDJPY(3)-M1-No Session.csv`](https://drive.google.com/file/d/1CjCXrVsAs-x9cC1e7UL16HNEfYHb-nNO/view?usp=drivesdk) から直接 `RAW_M1_EXACT` モードで台帳とマニフェストを再生成・ハッシュ検証する場合は、以下のワンコマンドを実行してください（引数不要）。

```powershell
python "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検\profile_is_market_structure_gsr_2026w48_v1_0.py"
```

<!-- RESEARCH_TRACE_END -->
