import datetime

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class Report(object):

    def __init__(self, key_file, view_id):

        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.KEY_FILE = key_file
        self.VIEW_ID = view_id

    def initialize_analyticsreporting(self, start, end):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.KEY_FILE, self.SCOPES)
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        response = analytics.reports().batchGet(
                body={
                    'reportRequests': [{
                        'viewId': self.VIEW_ID,
                        'dateRanges': [{'startDate': start, 'endDate': end}],
                        'dimensions': [{'name': 'ga:date'}],
                        'metrics': [
                            {'expression': 'ga:adsenseRevenue'},
                            {'expression': 'ga:adsenseAdUnitsViewed'},
                            {'expression': 'ga:adsenseAdsViewed'},
                            {'expression': 'ga:adsenseAdsClicks'},
                            {'expression': 'ga:adsensePageImpressions'},
                            {'expression': 'ga:adsenseCTR'},
                            {'expression': 'ga:adsenseECPM'},
                            {'expression': 'ga:adsenseExits'},
                            {'expression': 'ga:adsenseViewableImpressionPercent'},
                            {'expression': 'ga:adsenseCoverage'},
                        ],
                    }]
                }
        ).execute()

        return response

    def response(self, start='7daysAgo', end='yesterday'):

        response = self.initialize_analyticsreporting(start, end)

        ad_columns_list = []
        for row in response['reports']:
            ad_columns_list.append(row['columnHeader']['dimensions'][0].replace('ga:', ''))
            for r in row['columnHeader']['metricHeader']['metricHeaderEntries']:
                ad_columns_list.append(r['name'].replace('ga:adsense', ''))

        if start == '7daysAgo':
            # データフレーム用のデータを取得
            ad_lists = [[row['dimensions'][0]] + row['metrics'][0]['values'] for row in response['reports'][0]['data']['rows']]
        else:
            ad_lists = [[row['dimensions'][0]] + row['metrics'][0]['values'] for row in response['reports'][0]['data']['rows']]
            last_date = ad_lists[-1:][0][0]

            if last_date != end.replace('-', ''):
                last_date_obj = datetime.datetime.strptime(last_date, '%Y%m%d')
                last_date_next_obj = last_date_obj + datetime.timedelta(days=1)
                new_start = last_date_next_obj.strftime('%Y-%m-%d')

                response = self.initialize_analyticsreporting(new_start, end)

                ad_lists_2 = [[row['dimensions'][0]] + row['metrics'][0]['values'] for row in response['reports'][0]['data']['rows']]

                ad_lists = ad_lists + ad_lists_2

        return ad_columns_list, ad_lists
