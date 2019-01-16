from datetime import datetime
from typing import List
import pprint

#  from model import NotifyDate
from model import Combination
from model import create_combinations
from model import update_combinations
from datasource import SlackDatasource


class NotifyToSlack:
    def __init__(self):
        pass

    def run(self):
        # 組み合わせを取得
        pair_index_list = [1, 2, 3, 4, 5]
        pairs: List[Combination] = create_combinations(pair_index_list)
        # 日付を取得
        today = datetime.today()
        # 日付が更新可能な日付であれば前回の組み合わせから新しい組み合わせを作成
        #  NotifyDate.isUpdatable(today)
        new_pairs: List[Combination] = update_combinations(pairs)
        pprint.pprint(new_pairs)
        # slackに通知
        slack_datasource = SlackDatasource()
        slack_datasource.post(pair_list=new_pairs)


if __name__ == '__main__':
    n = NotifyToSlack()
    n.run()
