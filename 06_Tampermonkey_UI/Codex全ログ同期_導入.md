# Codex全ログ同期アイコン v5.1

ChatGPT側とGemini側の既存v5.0に、常時表示の「🧩🔄」ボタンを追加。
クリックすると既存Codexデスクトップ連携の登録画面 http://127.0.0.1:5001/ を別タブで開く。
クリック自体は登録・送信を行わない。登録画面で対象チャットを選び「このチャットを登録・記録開始」を押す。
既存連携は登録したチャットの過去のユーザー発言と最終回答、および以後の追加分を10秒ごとに同期する。
内部指示、ツール出力、途中経過、添付本体は対象外。「全ログ」はこの会話本文の範囲。

## 導入

1. 既存のAIチームサーバー（127.0.0.1:5000）とCodex連携（5001）を起動する。
   Codex連携の起動ファイル：`C:\Users\kj43b\Documents\ChatGPT\プログラミング管理\codex-desktop-bridge\start-background.ps1`。
2. Tampermonkeyで既存のChatGPT用スクリプトを開き、`ChatGPT_Scout_Champ_Codex_v5.1.user.js`の全文に置換して保存。
3. Gemini側も追加する場合は、既存Gemini用を`Gemini_Spark_Codex_v5.1.user.js`の全文に置換して保存。
4. 対象ページを再読み込みし、タスクバーの「🧩🔄」を押して対象チャットを登録する。

同じページで旧版と新版を同時に有効にしない。元のv5.0は変更していないため、元の全文に戻せる。
TampermonkeyのアイコンはChatGPT/Geminiのブラウザ上に表示する。Codexデスクトップ本体のUIには追加しない。
登録画面が開いても同期完了の証明にはならない。登録画面の対象名、記録状態、エラーを確認する。

## 実装記録

case_id: unknown
parent_case_id: unknown
purpose: 既存TampermonkeyからCodexデスクトップのログ同期登録画面へ到達できるようにする。
references:
- specification: 今回のユーザー指示。追加ボタンの具体方式は既存連携に合わせた実装判断。
- data: none
- code: プログラミング管理/sources/Common内のChatGPTおよびGemini v5.0参照コピー、codex-desktop-bridge/manager.py、panel.js、README.md。
- logs: unknown
changed_files:
- 06_Tampermonkey_UI/ChatGPT_Scout_Champ_Codex_v5.1.user.js（新規派生版）
- 06_Tampermonkey_UI/Gemini_Spark_Codex_v5.1.user.js（新規派生版）
- 06_Tampermonkey_UI/Codex全ログ同期_導入.md
- 07_Tests_and_Backtests/test_codex_sync_icon.cjs
tests_run:
- Node.js構文検査（両スクリプト）
- node 07_Tests_and_Backtests/test_codex_sync_icon.cjs
results: ボタンのクリック、遷移先、アクセシブルな名称、opener分離、window.openのnull返却を検証。
not_executed: Tampermonkeyへのインストール、実ブラウザ操作、本番ログ送信、Driveクラウド同期確認。
engineering_status: TESTED（構文・ボタン動作のみ）
decision: unknown
remaining_risks: インストール済みスクリプトの版は未確認。連携サーバー停止時は登録画面へ接続できない。
next_owner: ユーザー
next_action: Tampermonkeyに新版を適用し対象チャットを登録する。
