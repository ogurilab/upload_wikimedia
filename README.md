# upload_wikimedia

このプロジェクトは、指定された画像を Wikimedia Commons にアップロードする Python スクリプトを含んでいます。

## セットアップ

### 依存関係のインストール

まず、必要な Python ライブラリをインストールします。プロジェクトのルートディレクトリで以下のコマンドを実行してください：

```bash
pip install -r requirements.txt
```

### 環境変数の作成

次に、`.env.example`を`.env`にコピーしてください：

```bash
cp .env.example .env
```

そして、`.env`ファイルを編集してください。以下の環境変数を設定する必要があります：

- `USERNAME=あなたのユーザー名` - Wikimedia Commons のユーザー名
- `PASSWORD=あなたのパスワード` - Wikimedia Commons のパスワード
