import datetime
import json

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class Report(object):

    def __init__(self, key_file, view_id):

        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.KEY_FILE = key_file
        self.VIEW_ID = view_id

    def initialize_analyticsreporting(self, start, end, requests):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.KEY_FILE, self.SCOPES)
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        response = analytics.reports().batchGet(body=requests).execute()

        return response

    def response(self, start='7daysAgo', end='yesterday', dimensions='date', metrics='adsense'):

        requests = self.requests(start, end, dimensions, metrics)
        response = self.initialize_analyticsreporting(start, end, requests)

        # レポートのディメンション名とメトリックス名を取得する処理
        ad_columns_list = []
        for rows in response['reports']:
            ad_columns_list.append(rows['columnHeader']['dimensions'][0])
            for row in rows['columnHeader']['metricHeader']['metricHeaderEntries']:
                ad_columns_list.append(row['name'])

        # レポートのバリューをデータフレーム用にリスト内包表記で取得
        ad_lists = [[rows['dimensions'][0]] + rows['metrics'][0]['values'] for rows in response['reports'][0]['data']['rows']]
        
        if start != '7daysAgo':
            # start変数が「7daysAgo」以外だった場合に実行される処理

            # ad_lists変数内の最後の日付を取得
            last_date = ad_lists[-1:][0][0]
            
            if last_date != end.replace('-', ''):
                # ad_lists変数内の最後の日付とパラメータ「end」に渡された日付がマッチされなかった場合の処理
                # レポートは1000ページまでが1回に取得できる限度となっているので、続きのレポートを取得するための処理

                # last_date変数の日付まではあるので、その次の日付を取得するための処理
                last_date_obj = datetime.datetime.strptime(last_date, '%Y%m%d')
                last_date_next_obj = last_date_obj + datetime.timedelta(days=1)
                new_start = last_date_next_obj.strftime('%Y-%m-%d')

                # 新たに取得できなかった日付からレポートを取得する
                requests = self.requests(new_start, end, dimensions, metrics)
                response = self.initialize_analyticsreporting(new_start, end, requests)

                # 続きのレポートのバリューをデータフレーム用にリスト内包表記で取得
                ad_lists_2 = [[row['dimensions'][0]] + row['metrics'][0]['values'] for row in response['reports'][0]['data']['rows']]

                # 最初のレポートと続きのレポートをまとめる
                ad_lists = ad_lists + ad_lists_2

        return ad_columns_list, ad_lists

    def requests(self, start, end, dimensions, metrics):

        # self.dimensionsを作成
        metrics = self.metrics(metrics)

        body={
                'reportRequests': [{
                    'viewId': self.VIEW_ID,
                    'dateRanges': [{'startDate': start, 'endDate': end}],
                    'dimensions': [{'name': 'ga:date'}],
                    'metrics': [],
                }]
        }

        body['reportRequests'][0]['metrics'] = metrics

        return body

    def metrics(self, metrics_name):
        # metricsデータの取得
        # datas/内のjsonファイルと一致すれば特定のテーマを取得できる

        metrics_name = metrics_name + '.json'
        with open('report/datas/'+metrics_name) as f:
            str_obj = f.read()
            metrics_result = json.loads(str_obj)

        return metrics_result
