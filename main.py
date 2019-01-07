import requests
import json
import os

import jpholiday
import datetime


class NotifyToSlack:
    def __init__(self):
        self.end_point = os.environ['SLACK_WEBHOOK_URL']

    def run(self):
        requests.post(
            self.end_point,
            data=json.dumps({
                'text': u'Test',
                'username': u'me',
                'icon_emoji': u':money_with_wings:',
                'link_names': 1,
                'attachments': [{
                    'fields': [
                        {'title': 'pair1', 'value': 'sakochi:sakochi2'},
                        {'title': 'pair2', 'value': 'sakochi3:sakochi4'}
                    ]
                }]
            }))

class NotifyDate:
    def __init__(self):
        self.today = datetime.date.today()

    def is_holiday(self):
        return jpholiday.is_holiday(self.today)

if __name__ == '__main__':
    notify_date = NotifyDate()
    if notify_date.is_holiday() is False:
        notify_to_slack = NotifyToSlack()
        notify_to_slack.run()