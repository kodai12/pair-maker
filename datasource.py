import csv
import json
import os
from operator import itemgetter
from typing import List

from lambdalayer import requests
from model.combination import Combination, CombinationList
from model.member import MemberId


class SlackDatasource:
    def __init__(self, end_point: str) -> None:
        self.end_point = end_point

    def post(self, pair_list: CombinationList) -> None:
        _pairs = [
            {
                'title': 'PAIR{}'.format(pair.to_dict()['index'] +
                                         1),  # pair番号は1から始めるのでインクリメント
                'value': '{}'.format(self.__format_pair(pair))
            } for pair in pair_list.values
        ]
        _order_correction_pair = [{
            'value':
            '{}'.format(self.__format_pair(pair_list.values[0]))
        }]
        _morning_chairman = [{
            'value':
            '{}'.format(pair_list.values[0].to_dict()['member'][0]['name'])
        }]
        requests.post(
            self.end_point,
            data=json.dumps({
                'username':
                os.environ.get('SLACK_NOTIFY_USERNAME', 'ペア通知bot'),
                'icon_emoji':
                os.environ.get('SLACK_NOTIFY_ICON', ':barusu:'),
                'link_names':
                1,
                'attachments': [{
                    'title': 'ペアプロの組み合わせ',
                    'fields': _pairs,
                }, {
                    'title': '注文補正の担当ペア',
                    'fields': _order_correction_pair,
                }, {
                    'title': '朝会の司会',
                    'fields': _morning_chairman,
                }]
            }))

    def __format_pair(self, pair: Combination) -> str:
        members = pair.to_dict()['member']
        if isinstance(members, list):
            name_list = [member['name'] for member in members]
            return ' : '.join(name_list)
        return members['name']

    def measure_pair_variation(self, pair_list: CombinationList) -> None:
        members = [pair.to_dict()['member'] for pair in pair_list.values]
        if isinstance(members, list):
            print(members)
            name_list = [member['name'] for member in members]
            print_name = ' : '.join(name_list)
            if print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(0)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(1)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(2)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(3)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(4)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(5)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(6)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(7)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(8)
            elif print_name == '' or print_name == '':
                CsvDatasource.write_for_metrics(9)


class CsvDatasource:
    def __init__(self, settings_file: str, index_history_file: str) -> None:
        self.settings_file = settings_file
        self.index_history_file = index_history_file

    def read(self) -> List[dict]:
        with open(self.settings_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            l = [{
                'id':
                row[0],
                'index':
                self.__find_index_by_id(int(row[0])),
                'name':
                row[1],
                'skip_days':
                list(
                    map(lambda v: int(v) if v != '' else None,
                        row[2].split(',')))
            } for row in reader]
            return sorted(l, key=itemgetter('index'), reverse=False)

    def __find_index_by_id(self, id: int):
        with open(self.index_history_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            index_list = [int(row[0]) for row in reader]
            return index_list.index(
                id
            ) if id in index_list else 100000  # NOTE: indexがセットされてない場合適当な値(100000)を入れとく

    def write(self, member_id_list: List[MemberId]) -> None:
        with open(self.index_history_file, 'w') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['id'])
            for member_id in member_id_list:
                w.writerow(member_id.value)

    @staticmethod
    def write_for_metrics(id) -> None:
        point_list = []
        with open('metrics.csv', 'r') as f:
            r = csv.reader(f)
            point_list = [int(row[0]) for row in r]
        with open('metrics.csv', 'w') as f:
            w = csv.writer(f, lineterminator='\n')
            point_list[id] += 1
            for point in point_list:
                w.writerow([point])

