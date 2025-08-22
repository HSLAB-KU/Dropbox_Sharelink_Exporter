## 概要
このコードは、Dropbox上にあるファイルの共有リンクを一括で取得し、ファイル名とURLをセットでcsvファイルとして保存することができます。
## 設定
### ステップ1　APIの有効化
[こちら](https://www.dropbox.com/developers/apps/create?_tk=pilot_lp&_ad=ctabtn1&_camp=create)でAPIを設定する
1. Choose an API ⇒　"Scoped access"を選択
2. Choose the type of access you need　⇒　"Full Dropbox"を選択
3. Name your app　⇒　任意の名前を付ける
4. 右下"Create app"押下

### ステップ2　APIの設定
1. "Settings"タブ内の"Generated access token"押下
2. 生成された文字列をコピー
3. "Permissions"タブ内の"account_info.read", "files.metadata.read", "files.content.read", "sharing.read"にチェック

### ステップ3　Pythonの設定
ライブラリ"dropbox"と"pandas"をインストール

### ステップ4　実行
1. ファイル"test.py"をダウンロードし実行
2. トークンを入力
3. ファイルがあるディレクトリを相対パスで入力
4. 同一ディレクトリにcsvファイルが保存されます(処理時間はファイル数によって変動します)
