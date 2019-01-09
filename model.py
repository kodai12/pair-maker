import jpholiday
import datetime
from typing import List


class Value:
    def __init__(self) -> None:
        pass


class Entity:
    def __init__(self) -> None:
        pass


class NotifyDate(Value):
    def __init__(self) -> None:
        self.today = datetime.date.today()

    def is_holiday(self) -> bool:
        return jpholiday.is_holiday(self.today)


class PairNumber(Value):
    def __init__(self, value: int) -> None:
        self.value = value


class TimesOfPair(Value):
    def __init__(self, value: int) -> None:
        self.value = value


class Member(Entity):
    def __init__(self, pair_number: PairNumber,
                 times_of_pair: TimesOfPair) -> None:
        self.pair_number = pair_number
        self.times_of_pair = times_of_pair

    def change_pair_order(self) -> dict:
        if self.times_of_pair.value == 0:
            return {
                'pair_number': self.pair_number.value,
                'times_of_pair': self.times_of_pair.value + 1
            }
        else:
            return {
                'pair_number': self.pair_number.value + 1,
                'times_of_pair': 0
            }

    def is_belong_pair(self, member_list: list):
        filtered = [
            m for m in member_list
            if m.pair_number.value == self.pair_number.value
        ]
        if len(filtered) == 1:
            return False
        else:
            return True

    @staticmethod
    def from_dict(d: dict) -> 'Member':
        return Member(
            pair_number=PairNumber(d['pair_number']),
            times_of_pair=TimesOfPair(d['times_of_pair']))

    def to_dict(self) -> dict:
        return {
            'pair_number': self.pair_number.value,
            'times_of_pair': self.times_of_pair.value
        }


class MemberList(Value):
    def __init__(self, values: List[Member]):
        self.values = values

    def change_pair(self) -> 'MemberList':
        changed_member_list: list = []
        for member in self.values:
            if member.is_belong_pair(self.values):
                changed_member: dict = member.change_pair_order()
            else:
                changed_member: dict = {'pair_number': 0, 'times_of_pair': 0}
            changed_member_list.append(changed_member)

        return create_member_list(changed_member_list)


def create_member_list(member_list: list):
    return MemberList([Member.from_dict(m) for m in member_list])
