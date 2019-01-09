from model import MemberList
from model import create_member_list
import pprint


class NotifyToSlack:
    def __init__(self):
        pass

    def run(self):
        # dynamoからメンバーのデータを取得しモデルに変換
        member_list: list = [
            {
                "pair_number": 0,
                "times_of_pair": 1
            },
            {
                "pair_number": 0,
                "times_of_pair": 0
            },
            {
                "pair_number": 1,
                "times_of_pair": 1
            },
            {
                "pair_number": 1,
                "times_of_pair": 0
            },
            {
                "pair_number": 2,
                "times_of_pair": 0
            },
        ]
        member_list: MemberList = create_member_list(member_list)
        print('-------original-------')
        for m in member_list.values:
            pprint.pprint(m.to_dict())
        # ペアを回して新しいペアの組み合わせを取得
        changed_member_list: MemberList = member_list.change_pair()
        print('-------changed-------')
        for m in changed_member_list.values:
            pprint.pprint(m.to_dict())
        # 新しいペアをdynamoに保存
        # slackに通知


if __name__ == '__main__':
    n = NotifyToSlack()
    n.run()
