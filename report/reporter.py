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
        return response
