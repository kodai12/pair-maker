from datetime import datetime
from typing import List

from datasource import CsvDatasource, SlackDatasource
from model.combination import Combination, CombinationList, create_combinations
from model.date import NotifyDate


class NotifyToSlack:
    def __init__(self, csv_datasource: CsvDatasource,
                 slack_datasource: SlackDatasource, read_csv_file: str,
                 write_csv_file: str):
        self.csv_datasource = csv_datasource
        self.slack_datasource = slack_datasource
        self.read_csv_file = read_csv_file
        self.write_csv_file = write_csv_file

    def run(self):
        # 組み合わせを取得
        pair_index_list = self.csv_datasource.read(self.read_csv_file)
        pairs: CombinationList = create_combinations(pair_index_list)

        # 日付を取得
        today = datetime.today().date()

        # 日付が更新可能な日付であれば前回の組み合わせから新しい組み合わせを作成
        notify_date = NotifyDate(today)
        if not notify_date.is_holiday():  # TODO: kesu
            print('Today is Holiday!!')
            return  # TODO: 例外処理?
        new_pairs: CombinationList = pairs.update_combination_list()

        # 新しい組み合わせデータを永続化
        self.csv_datasource.write(self.write_csv_file, new_pairs)

        # slackに通知
        self.slack_datasource.post(pair_list=new_pairs)
