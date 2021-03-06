from datetime import datetime
from typing import List

from datasource import CsvDatasource, SlackDatasource
from model.combination import CombinationList, create_combinations
from model.date import NotifyDate


class NotifyToSlack:
    def __init__(self, csv_datasource: CsvDatasource,
                 slack_datasource: SlackDatasource):
        self.csv_datasource = csv_datasource
        self.slack_datasource = slack_datasource

    def run(self):
        # 日付を取得
        today = datetime.today()
        notify_date = NotifyDate(today)

        # 組み合わせを取得
        pair_index_list: List[dict] = self.csv_datasource.read()
        pairs: CombinationList = create_combinations(pair_index_list)

        #  import pprint
        #  pprint.pprint(pairs.to_dict())
        #  a = pairs.update_not_in_office_member(['迫地', '田中'])
        #  pprint.pprint(a.to_dict())

        # (出張などで)スキップしたいメンバーを除外
        pair_skipped_index_list = pairs.update_skip_list_member(
            notify_date.get_weekday())

        # 日付が更新可能な日付であれば前回の組み合わせから新しい組み合わせを作成
        if notify_date.is_holiday():
            print('Today is Holiday!!')
            return  # TODO: 例外処理?
        new_pairs: CombinationList = pair_skipped_index_list.update_combination_list(
        )

        # 新しい組み合わせデータを永続化
        member_id_list: List[int] = new_pairs.get_member_id_list()
        self.csv_datasource.write(member_id_list)

        # slackに通知
        self.slack_datasource.post(pair_list=new_pairs)
        #  self.slack_datasource.measure_pair_variation(pair_list=new_pairs)

