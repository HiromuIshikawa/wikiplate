# Wikiplate

UDC2018 応募作品

Wikipedia Town で作成する記事のテンプレートを生成する Web アプリケーションです．

作動中のアプリケーション URL: https://wikiplate.herokuapp.com/

## 環境

 - python: 3.5.2

 - npm: 8.12.0

## セットアップ

### サーバのセットアップ

1. clone

    ```
    git clone https://gitlab.datacradle.jp/dc-students/wiki-link-map.git
    cd wikiplate
    ```

2. パッケージのインストール

    ```
    pip install -r requirements.txt
    ```

### フロントエンドのセットアップ

1. パッケージのインストール
    ```
    npm install
    ```

### データベースのセットアップ

1. MySQL に任意のデータベースを作成

2. データのリストア
   - `article.sql.gz`
   - `jawiki-20180601-page.sql.gz`

   を [Dropbox](https://www.dropbox.com/sh/qyg3rv7v0m6uyy4/AADpvSWwQHa1NDEQOcGS1RYNa?dl=0) からダウンロードして以下を実行
      ```
      gzip -d article.sql.gz
      mysql -u USERNAME DATABASENAME < article.sql
      gzip -d jawiki-20180601-page.sql.gz
      mysql -u USERNAME DATABASENAME < jawiki-20180601-page.sql
      ```
3. 作成したデータベース情報を設定ファイルに記載
    ```
    cp settings.yml.sample settings.yml
    emacs settings.yml
    ```
    上記の実行で以下ようなファイルが開く

    ```
    host: XXXXXXX
    user: XXXXXXX
    password: XXXXXXXX
    database: XXXXXXXX
    charset: utf8
    ```

    上記ファイルの `XXXXXXXX` の箇所を，作成したMySQL データベースの情報に編集する．

## 起動

1. Flask アプリの起動
    ```
    python run.py
    ```

2. frontend 以下を改変した場合

    ```
    cd frontend
    npm run build
    ```
    を実行してから，Flask アプリを起動する．

    上記は，localhost:5000 で立ち上がる．

    フロントの変更を開発用サーバで確認したい場合は，

    ```
    cd frontend
    npm start
    ```
    で，localhost:8081 上に立ち上がる．
