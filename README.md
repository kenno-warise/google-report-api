# google-report-api

Pythonで構築したGoogleAnalyticsのレポートを簡易的に取得できるようにしたAPIモジュールです。

## 使い方

各自GoogleのAPIが利用できるように、「Google Cloud Platform」で各種設定をすませ、API使用に必要なファイルを準備します。
現在取得できるレポートは、アナリティクスでいう「ユーザー」「パブリッシャー」「アドセンス」の３つです。
種類によって取得できるデータの階層構造が異なりますが、現在は「日付」「ページパス（URL）」「ページタイトル」のいずれかの軸でデータを取得できます。

## インストール

gitのクローンを使ってモジュールをダウンロードします。

```
$ git clone https://github.com/kenno-warise/google-report-api.git
```

ディレクトリを確認を確認すると、「google-report-api」が作成されています。
「cd」コマンドで移動して、仮想構築します。

```
$ ls
google-report-api

$ cd google-report_api

$ ls -a
.  ..  .git  .gitignore  .python-version  README.md  report  requirements.txt

$ python3 --version
Python 3.7.0

$ python3 -m venv venv
```

仮想環境ができたら、切り替えて必要なパッケージをインストールします。

```
$ . venv/bin/activate

(venv)$ pip install --upgrade pip

(venv)$ pip install -r requirements.txt
```
