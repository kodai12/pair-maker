import requests
import json
import os
from typing import List
import csv

from model.combination import Combination


class SlackDatasource:
    def __init__(self) -> None:
        self.end_point = os.environ['SLACK_WEBHOOK_URL']

    def post(self, pair_list: List[Combination]) -> None:
        fields = [
            {
                'title': 'pair{}'.format(pair.to_dict()['index'] +
                                         1),  # pair番号は1から始めるのでインクリメント
                'value': '{}'.format(self.__format_pair(pair))
            } for pair in pair_list
        ]
        requests.post(
            self.end_point,
            data=json.dumps({
                'text': '今日のペアプロの相手は...?',
                'username': 'ペア通知bot',
                'icon_emoji': ':barusu:',
                'link_names': 1,
                'attachments': [{
                    'fields': fields
                }]
            }))

    def __format_pair(self, pair: Combination) -> str:
        members = pair.to_dict()['member']
        if isinstance(members, list):
            name_list = [member['name'] for member in members]
            return ' : '.join(name_list)
        return members['name']


class CsvDatasource:
    def __init__(self) -> None:
        pass

    def read(self, file_name: str) -> List[dict]:
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            return [{
                'id': row[0],
                'index': row[1],
                'name': row[2]
            } for row in reader]

    def write(self, file_name: str, pair_list: List[Combination]) -> None:
        with open(file_name, 'w') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(pair_list[0].to_dict()['member'][0].keys())
            for pair in pair_list:
                lists = pair.to_flat_list()
                for l in lists:
                    w.writerow(l)
