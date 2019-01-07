import requests
import json
import os


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


if __name__ == '__main__':
    notify_to_slack = NotifyToSlack()
    notify_to_slack.run()