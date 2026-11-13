# Codex公式TRACEの保存

case_id: unknown / parent_case_id: unknown。純粋な保存機能で対象市場はnone。
仕様: 本チャットでユーザーが指定した公式TRACEのみの保存。
コード: codex_trace_save.py v1。入力データ版: none。
参照: AGENTS.md、Codex_Role_Prompt_v1.0_2026-10-04.md、共有status.json revision 3、既存Codex連携zip v1.0。

## 動作

このプロジェクトでCodexが公式TRACEを発行するとき、回答本文をUTF-8の入力ファイルとして準備し、保存スクリプトを実行してから同じTRACE本文をチャットに返す。
保存先は実在した共有フォルダに合わせて `G:\マイドライブ\AIトレーサビリティ\AI4者会談\進行中\Codex`。
ユーザーの呼称「AI4者協議会談」と異なるが既存共有フォルダを改名しない。

これはCodexの作業規則に基づく保存であり、デスクトップの回答を監視する常駐プログラムやブラウザコンソールの改修ではない。
他プロジェクト・TESTチャットではこのAGENTS.mdを読まなければ自動適用されない。
他AIへの送信、サーバーのDB登録、status.json変更、確定/保留への自動振分けはしない。
技術的な保存権限を保証しない。現環境の通常権限ではGドライブが拒否されたため、必要に応じて承認付き実行を行う。

## 実行

Python標準ライブラリのみ。実行例（PowerShell）:

```powershell
& 'C:\Users\kj43b\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'G:\マイドライブ\AIトレーサビリティ\Codex\BO-EA-Edge-Discovery\05_Server_Integration\codex_trace_save.py' --input '公式TRACE本文の絶対パス'
```

実行時にJSONで保存パス・SHA256・バイト数・saved/already_savedを返す。
完全なTRACE、ai_id: codex、JST日時、ヘッダーとの整合を検査する。
ファイル名に日時・case_id・分割情報・本文SHA256を含め、既存ファイルは上書きしない。
同一本文は既存保存を確認し、変更した本文は別ファイルに保存する。
本文は改行をLFに統一し末尾改行を1つにする。内容の省略・要約はしない。
保存後に全バイトを読み戻して照合する。失敗時は非ゼロ終了、保存成功を報告しない。
書込中の強制終了に対する原子的公開、Google Driveクラウド同期完了、他AIの読了は保証しない。

## 検証記録

Python 3系の同梱ランタイムで5テスト成功。
日本語・記号の往復、同一本文の重複排除、変更本文の別保存、不正/欠落TRACEの拒否、改行差の統一、保存先障害を検査。
初回はWindowsサンドボックスの一時フォルダ権限エラーで全5件失敗。通常権限で再実行し5件成功。失敗を仕様緩和で隠していない。
この記録に加え、本番フォルダで導入ログを保存し読戻し検証する。
engineering_status: TESTED（単体）。サーバー連携未実行。decision: 追加検証。
next_owner: Codex。next_action: 公式TRACE発行時に保存を実行し、実際の保存結果を報告。
