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
    def __init__(self,
            pair_number: PairNumber,
            times_of_pair: TimesOfPair) -> None:
        self.pair_number = pair_number
        self.times_of_pair = times_of_pair

    def change_pair_order(self) -> 'Member':
        if self.times_of_pair == 0:
            return Member(
                    pair_number=self.pair_number,
                    times_of_pair=self.times_of_pair + 1
                    )
        else:
            return Member(
                    pair_number=self.pair_number - 1,
                    times_of_pair=0
                    )

    @staticmethod
    def from_dict(d: dict) -> 'Member':
        return Member(
                pair_number=d['pair_number'],
                times_of_pair=d['times_of_pair']
                )

    def to_dict(self) -> dict:
        return {
                'pair_number': self.pair_number.value,
                'times_of_pair': self.times_of_pair.value
                }


class MemberList(Value):
    def __init__(self, values: List[Member]):
        self.values = values

    def change_pair(self) -> 'MemberList':
        changed_member_list = []
        for member in self.values:
            if self.__is_belong_pair(member):
                changed_member = member.change_pair_order()
            else:
                changed_member = Member(
                        pair_number=0,
                        times_of_pair=0
                        )
            changed_member_list.append(changed_member)

        return changed_member_list

    def __is_belong_pair(self, m: Member):
        filterd = [v for v in self.values if v.pair_number == m.pair_number]
        if len(filterd) == 1:
            return False
        else:
            return True


def create_member_list(member_list: list):
    return [Member.from_dict(m) for m in member_list]

