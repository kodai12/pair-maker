import requests
import json
import os
from typing import List

from model import Combination


class SlackDatasource:
    def __init__(self):
        self.end_point = os.environ['SLACK_WEBHOOK_URL']

    def post(self, pair_list: List[Combination]):
        fields = [{
            'title': 'pair{}'.format(index),
            'value': '{}'.format(pair.to_dict()['member'])
        } for index, pair in enumerate(pair_list)]
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
