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

※「.python-version」ディレクトリはPythonバージョン管理ツールのpyenvにより作成したファイルなので、pyenvを利用していない場合は気にしなくても良いです。

```
$ ls
google-report-api

$ cd google-report-api

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

## 基本的な使い方

```
from report.reporter import Report


view_id = 'Googleアナリティクスから取得するビューID'
KEY_FILE = 'client_secrets.json'

# キーとIDを渡して初期化
report = Report(key_file=KEY_FILE, view_id=view_id)

# 日付範囲やレポート名を設定する
# 戻り値は「レポート名」と「レポートの値」の２値
columns, datas = report.response(
        start='7daysAgo',
        end='yesterday',
        dimensions=['date'],
        metrics='users'
)

print('レポートの各名前', columns)
print('----------------------------')
print('レポートの値', datas)
```

上記のファイルを実行すると以下のようにリスト形式でレポートを取得できます。

```
レポートの各名前 ['ga:date', 'ga:users', 'ga:newUsers', 'ga:percentNewSessions', 'ga:sessionsPerUser']
----------------------------
レポートの値 [['20221221', '490', '393', '75.0', '1.0693877551020408'], ['20221222', '442', '341', '70.02053388090349', '1.1018099547511313'], ['20221223', '423', '321', '70.08733624454149', '1.08274231678487'], ['20221224', '148', '128', '81.0126582278481', '1.0675675675675675'], ['20221225', '137', '114', '77.55102040816327', '1.072992700729927'], ['20221226', '392', '304', '70.53364269141531', '1.0994897959183674'], ['20221227', '387', '315', '75.90361445783132', '1.0723514211886305']]
```

## Pandasでデータフレーム化

pandasのデータフレーム化を想定しているので、それぞれの値をデータフレームオブジェクトに渡すと、すぐに分析を始められます。

```
import pandas as pd
from report.reporter import Report


view_id = 'Googleアナリティクスから取得するビューID'
KEY_FILE = 'client_secrets.json'

report = Report(key_file=KEY_FILE, view_id=view_id)

columns, datas = report.response(
        start='7daysAgo',
        end='yesterday',
        dimensions=['date'],
        metrics='users'
)

df = pd.DataFrame(datas, columns=columns)

df.head()
```
