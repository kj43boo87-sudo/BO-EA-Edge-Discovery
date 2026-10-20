# 実行証跡の退避・復元手順

## 未確定事項

通常実行ログ・受入メタデータの永続保存先、保存担当、保存期間、バックアップ頻度・第二保管先は **未確定**。
`G:\マイドライブ\AIトレーサビリティ\` は候補であり、この作業で配下フォルダを決めたり、保存済みと扱ったりしない。公式TRACE専用先とは区別する。ユーザーが保存先とアクセス権を確定するまで、クラウドだけの証跡は未退避として扱う。

## 環境破棄前の手順（手動）

1. 保存担当と永続先を決める。非公開の受入メタデータや入力パスを扱える権限を確認する。原本実データの保管先も別途確認する。
2. 対象のreports/*.json（失敗ログを含む）、data/raw/*.metadata.json、data/processed/の加工履歴・除外判断を一覧化する。認証情報・.venv・実データを無差別に収集しない。入力原本を含めない場合は、既存保管場所とSHA-256を記録する。
3. 対象コードのGitコミットと再構築手順も記録する。コードが未pushなら先に作業ブランチへ保存する。ログの入力ハッシュと実際に使った原本が照合できることを確認する。
4. 下の例のプレースホルダーを実在する対象と確定保存先へ置換し、選んだファイルだけをアーカイブする。既存アーカイブを上書きせず、JST日時と一意な名前を付ける。
5. 永続先へコピーまたはダウンロード/アップロードし、保存先から読み戻してアーカイブのSHA-256が一致することを確認する。同期アイコンだけで保存完了としない。
6. 別の空ディレクトリに復元して内部の各SHA-256も確認する。実施日時（JST）、担当、実在する保存先、アーカイブと内部の照合結果を退避記録へ残す。
7. 全対象の読み戻し・復元確認が完了するまで、クラウド側の削除・環境破棄を完了扱いにしない。失敗や未対象を記録する。

Linuxでの例（例示用パスのまま実行しない）:

```bash
# リポジトリのルート。対象は実在するファイル名に置き換える。
sha256sum reports/RUN.json data/raw/DATA.metadata.json > reports/evidence-JST-ID.sha256
# 出力先はユーザーが確定した場所。既存ファイルのない一意なパスを使う。
tar -czf /CONFIRMED_DEST/evidence-JST-ID.tar.gz reports/RUN.json data/raw/DATA.metadata.json reports/evidence-JST-ID.sha256
sha256sum /CONFIRMED_DEST/evidence-JST-ID.tar.gz
```

ダウンロード等を挟んだ場合は、転送元と読み戻した先のアーカイブハッシュを照合する。

復元例（自分で作成しハッシュ照合したアーカイブだけを使う）:

```bash
mkdir /RESTORE_PARENT/new-empty-directory
# 一覧で想定した相対パスだけが含まれることを確認する。
tar -tzf /CONFIRMED_DEST/evidence-JST-ID.tar.gz
tar -xzf /CONFIRMED_DEST/evidence-JST-ID.tar.gz -C /RESTORE_PARENT/new-empty-directory
cd /RESTORE_PARENT/new-empty-directory
sha256sum -c reports/evidence-JST-ID.sha256
```

コードは該当Gitコミットをチェックアウトして依存を再構築する。入力原本は別保管先から戻し、メタデータのハッシュと照合する。ログだけの復元は実データ検証の再現成功とは扱わない。

本手順は自動バックアップ機能ではない。人工ファイルでのアーカイブ/復元確認と、実際の永続先への退避完了は区別して報告する。
