#### Dropbox上にあるファイルの共有リンクを一括で取得し、ファイル名とURLをセットでcsvファイルに保存することができます
### ステップ1　APIの有効化
[こちら](https://www.dropbox.com/developers/apps/create?_tk=pilot_lp&_ad=ctabtn1&_camp=create)でAPIを設定する
1. Choose an API ⇒　"Scoped access"を選択
2. Choose the type of access you need　⇒　"Full Dropbox"を選択
3. Name your app　⇒　任意の名前を付ける
4. 右下"Create app"押下

### ステップ2　APIの設定
1. "Permissions"タブ内の"account_info.read", "files.metadata.read", "files.content.read", "sharing.read"にチェック
2. ページ下部"Submit"押下
3. "Settings"タブ内の"Generated access token"押下
4. 生成された文字列をコピー

### ステップ3　Pythonの設定
ライブラリ"dropbox"と"pandas"をインストール

### ステップ4　実行
1. "test.py"をダウンロードし実行(保存先は任意)
2. トークン入力を求められるので、トークンを貼り付け
3. パス入力を求められるのて、リンクを取得したいファイルが保存されているディレクトリを相対パスで入力(例: 絶対パスがDropbox/xxx/yyyの場合　⇒　相対パスとしてxxx/yyyを入力)
4. エラーが発生しなければ、"test.py"があるディレクトリにcsvファイルが保存される(処理時間はファイル数によって変動する)
