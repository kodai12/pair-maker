from datetime import datetime
from typing import List

from model import NotifyDate
from model import Combination
from model import create_combinations
from model import update_combinations
from datasource import SlackDatasource
from datasource import CsvDatasource


class NotifyToSlack:
    def __init__(self):
        pass

    def run(self):
        # 組み合わせを取得
        csv_datasource = CsvDatasource()
        pair_index_list = csv_datasource.read('test.csv')  # TODO: 環境変数にする
        pairs: List[Combination] = create_combinations(pair_index_list)
        # 日付を取得
        today = datetime.today().date()

        # 日付が更新可能な日付であれば前回の組み合わせから新しい組み合わせを作成
        notify_date = NotifyDate(today)
        if notify_date.is_holiday():
            return  # TODO: 例外処理?
        new_pairs: List[Combination] = update_combinations(pairs)

        # 新しい組み合わせデータを永続化
        csv_datasource.write('test2.csv', new_pairs)

        # slackに通知
        slack_datasource = SlackDatasource()
        slack_datasource.post(pair_list=new_pairs)


if __name__ == '__main__':
    n = NotifyToSlack()
    n.run()
