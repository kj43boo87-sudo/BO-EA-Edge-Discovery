# Gemini側必勝調査報告 — 専用TRACEコード・案件採番規約

- **制定日**: `2026-11-06 JST`（中村さん指示により確定）
- **適用範囲**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\` 配下の全3工程
  1. 第1工程：`トレード手法の市場調査＆データ点検`
  2. 第2工程：`機会台帳突合＆IS統計・Plateau検証`
  3. 第3工程：`執行監査・週次総括・Git資産整理`

## 1. 目的と位置づけ

本ライン（`Gemini側必勝調査報告`）の目的は、多角的な方面から情報を収集し、『BO・EA Edge Discovery』の現行実務・既存ロジックを別角度から見直して、**新たな必勝法（未知のエッジ・非対称優位性）を発見すること**にある。

したがって、本ラインで発行する公式TRACEの `case_id` に過去の個別検証案件コード（`BO-EUR-005` 等）を流用してはならず、**次回より本ライン専用の案件コード（`GSR-*`：Gemini Side Research / 必勝調査報告）を発行・使用する**。

## 2. 専用TRACEコード（`case_id`）採番ルール

1. **週次横断調査・3工程パイプライン総括コード**:
   - 形式: `GSR-YYYYWww`（ISO週番号）または連番 `GSR-001`, `GSR-002`, ...
   - 例（次回 2026年11月第2週 / 第46週）: `GSR-2026W46`
2. **個別必勝法候補・テーマ別検証コード**:
   - 形式: `GSR-{対象または提案区分}-{連番3桁}`
   - 例:
     - `GSR-SURVEY-001`（多角的市場構造・既存実務見直し調査）
     - `GSR-CLIMAX-001`（M5非トレンド制限×M1極値クライマックス逆張り）
     - `GSR-PULLBACK-001`（M5トレンド同調×M1ボラ収縮後反発確定）
     - `GSR-FAKEOUT-001`（異市場・時間帯需給フェイクアウト回帰）
3. **過去案件（`BO-EUR-004`, `BO-EUR-005` 等）の扱い**:
   - 過去の棄却・凍結案件は「再検証防止の比較参照元」として `source_trace_refs` にのみ記載し、本ラインの `case_id` には使用しない。

## 3. 次回からの公式TRACEヘッダー・メタデータ標準書式

```text
🏷️ [TRACE: GSR-2026W46 | {採用 / 棄却 / 保留 / 追加検証} | {セッションタイトル}]
<!-- RESEARCH_TRACE_START
ai_id: gemini
project_id: edge-discovery
project_name: BO・EA Edge Discovery (Gemini側必勝調査報告)
trace_namespace: BOEA
source_trace_refs: {参照した過去案件・既存EA・データファイル名}
record_id: unknown
session_title: {セッションタイトル}
case_id: GSR-2026W46
parent_case_id: root
decision: {採用 / 棄却 / 保留 / 追加検証}
target_market: {対象市場・時間足}
attachment_file: {出力ファイル名}
part_info: 1/1
timestamp: {YYYY-MM-DD HH:MM:SS JST}
-->
所属プロジェクト: BO・EA Edge Discovery / Gemini側必勝調査報告 (edge-discovery)
TRACE区分: BOEA
専用案件コード: GSR-2026W46
参照元: {参照ファイル・URL}
...
<!-- RESEARCH_TRACE_END -->
```
