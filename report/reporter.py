import datetime
import json

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class Report(object):

    def __init__(self, key_file, view_id):

        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.KEY_FILE = key_file
        self.VIEW_ID = view_id

    def initialize_analyticsreporting(self, requests):
        """
        requests変数には取得したいレポート内容が辞書型で格納されている。
        よってresponse変数にはレポート内容による値が格納される
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.KEY_FILE, self.SCOPES)
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        response = analytics.reports().batchGet(body=requests).execute()

        return response

    def response(self, start='7daysAgo', end='yesterday', dimensions='date', metrics='adsense', dimensions_filter=None):

        requests = self.requests(start, end, dimensions, metrics, dimensions_filter)
        response = self.initialize_analyticsreporting(requests)

        # レポートのディメンション名とメトリックス名を取得する処理
        ad_columns_list = []
        for rows in response['reports']:
            ad_columns_list.append(rows['columnHeader']['dimensions'][0])
            if len(requests['reportRequests'][0]['dimensions']) > 1:
                ad_columns_list.append(rows['columnHeader']['dimensions'][1])
                if len(requests['reportRequests'][0]['dimensions']) > 2:
                    ad_columns_list.append(rows['columnHeader']['dimensions'][2])
            for row in rows['columnHeader']['metricHeader']['metricHeaderEntries']:
                ad_columns_list.append(row['name'])

        try: # dimensions_filter次第では値が無い可能性があるので特設tra＆error文
            # レポートのバリューをデータフレーム用にリスト内包表記で取得
            if len(requests['reportRequests'][0]['dimensions']) == 2:
                ad_lists = [[rows['dimensions'][0], rows['dimensions'][1]] + rows['metrics'][0]['values'] for rows in response['reports'][0]['data']['rows']]
            elif len(requests['reportRequests'][0]['dimensions']) == 3:
                ad_lists = [[rows['dimensions'][0], rows['dimensions'][1], rows['dimensions'][2]] + rows['metrics'][0]['values'] for rows in response['reports'][0]['data']['rows']]
            else:
                ad_lists = [[rows['dimensions'][0]] + rows['metrics'][0]['values'] for rows in response['reports'][0]['data']['rows']]
        except KeyError:
            ad_lists = response['reports'][0]['data']['totals'][0]['values']
            print('dimensions_filter Error: {}には値がありません'.format(requests['reportRequests'][0]['dimensionFilterClauses'][0]['filters']))
        """
        一旦以下のコードは廃止

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
        """
        return ad_columns_list, ad_lists

    def requests(self, start, end, dimensions, metrics, dimensions_filter):

        dimensions = self.dimensions(dimensions)
        dimensions_filter = self.dimensions_filter(dimensions_filter)
        metrics = self.metrics(metrics)

        body={
                'reportRequests': [{
                    'viewId': self.VIEW_ID,
                    'dateRanges': [{'startDate': start, 'endDate': end}],
                    'dimensions': [],
                    'metrics': [],
                    'dimensionFilterClauses':[
                        {
                            'filters': [],
                        }
                    ],
                }]
        }

        body['reportRequests'][0]['dimensions'] = dimensions
        body['reportRequests'][0]['metrics'] = metrics
        if dimensions_filter:
            body['reportRequests'][0]['dimensionFilterClauses'][0]['filters'] = dimensions_filter
        
        return body

    def dimensions(self, dimensions_name):
        # dimensions名の取得
        
        if dimensions_name:
            dimensions_result = []

            if type(dimensions_name) != type(dimensions_result): 
                dimensions_name = [dimensions_name]
            
            for dimension in dimensions_name:
                dimensions_result.append({'name': 'ga:{}'.format(dimension)})
        
        return dimensions_result


    def dimensions_filter(self, dimensions_filter_name):

        return dimensions_filter_name

    def metrics(self, metrics_name):
        # metricsデータの取得
        # datas/内のjsonファイルと一致すれば特定のテーマを取得できる

        metrics_name = metrics_name + '.json'
        with open('report/datas/'+metrics_name) as f:
            str_obj = f.read()
            metrics_result = json.loads(str_obj)

        return metrics_result


if __name__ == '__main__':
    """
    このスクリプトファイルが実行された時だけ処理される。
    """
    with open('/mnt/c/Users/warik/Documents/PYTHON/science/GoogleアナリティクスAPI/view_id.txt', 'r') as f:
        view_id = f.read()
    
    KEY_FILE = '/mnt/c/Users/warik/Documents/PYTHON/science/GoogleアナリティクスAPI/client_secrets.json'
    dimensions_filter = {'dimensionName': 'ga:pagetitle', 'expressions': ['django']}
    report = Report(key_file=KEY_FILE, view_id=view_id)
    columns, datas = report.response(
            start='2023-01-12',
            end='2023-01-12',
            dimensions=['date', 'pagepath', 'pagetitle'],
            metrics='publicher',
            dimensions_filter=dimensions_filter,
    )
    print(columns)
    print('-------')
    print(datas)
