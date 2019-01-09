import requests
import json
import os

from model import MemberList


class SlackDatasource:
    def __init__(self):
        self.end_point = os.environ['SLACK_WEBHOOK_URL']

    def post(self, member_list: MemberList):
        fields = [{
            'title': 'pair{}'.format(l.pair_number.value),
            'value': '{}'.format(l.name.value)
        } for l in member_list.values]
        requests.post(
            self.end_point,
            data=json.dumps({
                'text': u'Test',
                'username': u'me',
                'icon_emoji': u':money_with_wings:',
                'link_names': 1,
                'attachments': [{
                    'fields': fields
                }]
            }))
