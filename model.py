from abc import ABCMeta, abstractmethod
from typing import List
from more_itertools import chunked
from itertools import chain
import random
import jpholiday
import datetime


class NotifyDate:
    def __init__(self, datetime: datetime.datetime):
        self.datetime = datetime

    def is_holiday(self) -> bool:
        if self.datetime.weekday == 5 or 6:
            return True
        if jpholiday.is_holiday(self.datetime):
            return True
        return False


class MemberId:
    def __init__(self, value: int):
        self.value = value


class MemberIndex:
    def __init__(self, value: int):
        self.value = value


class MemberName:
    def __init__(self, value: str):
        self.value = value


class Member:
    def __init__(self, id: MemberId, index: MemberIndex, name: MemberName):
        self.id = id
        self.index = index
        self.name = name

    @staticmethod
    def from_dict(member_dict: dict) -> 'Member':
        return Member(
            id=MemberId(member_dict['id']),
            index=MemberIndex(member_dict['index']),
            name=MemberName(member_dict['name']))

    def to_dict(self) -> dict:
        return {
            'id': self.id.value,
            'index': self.index.value,
            'name': self.name.value
        }

    def to_flat_list(self) -> List[str]:
        return [self.id.value, self.index.value, self.name.value]


class Combination(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, index):
        pass

    @abstractmethod
    def to_dict() -> dict:
        pass


class CombinationIndex:
    def __init__(self, value: int):
        self.value = value


class Pair(Combination):
    def __init__(self, index: CombinationIndex, memberList: List[Member]):
        self.index = index
        self.memberList = memberList

    def divide_member(self):
        return (self.memberList[0], self.memberList[1])

    def to_dict(self):
        return {
            'index': self.index.value,
            'member': [member.to_dict() for member in self.memberList]
        }

    def to_flat_list(self):
        return [member.to_flat_list() for member in self.memberList]


def create_pair(index: CombinationIndex, member_dict_list: List[dict]) -> Pair:
    return Pair(
        index=index,
        memberList=[
            Member.from_dict(member_dict=member_dict)
            for member_dict in member_dict_list
        ])


class Single(Combination):
    def __init__(self, index: CombinationIndex, member: Member):
        self.index = index
        self.member = member

    def to_dict(self):
        return {
            'index': self.index.value,
            'member': self.member.to_dict()
        }

    def to_flat_list(self):
        return [self.member.to_flat_list()]


def create_single(index: CombinationIndex, member_dict: dict) -> Single:
    return Single(
        index=index, member=Member.from_dict(member_dict=member_dict))


def create_combination(index: CombinationIndex,
                       member_dict_list: List[dict]) -> Combination:
    if len(member_dict_list) == 1:
        return create_single(index, member_dict_list[0])
    elif len(member_dict_list) == 2:
        return create_pair(index, member_dict_list)
    else:
        raise Exception('combination length must be 1 or 2')


def create_combinations(
        combination_index_list: List[dict]) -> List[Combination]:
    chunked_list: List[list] = list(chunked(combination_index_list, 2))
    return [
        create_combination(CombinationIndex(index), member_dict_list)
        for index, member_dict_list in enumerate(chunked_list)
    ]


def update_combinations(combinations: List[Combination]) -> List[Combination]:
    index_list_1 = []
    remaining_list = []
    (random_index, remain_index) = get_random_index()
    for combination in combinations:
        # ペアの片方は元のペアに残したままでもう片方はremainingにappendしておく
        if isinstance(combination, Pair):
            (move_member, stay_member) = combination.divide_member()
            index_list_1.append([stay_member])
            remaining_list.append({
                'pair_index': combination.index.value,
                'member': move_member
                })
        # singleの場合はrandom(1番目か2番目)にリストにinsertしておく
        if isinstance(combination, Single):
            index_list_1[random_index].append(combination.member)

    # remainingに残ったメンバーをいずれかのペアにinsertする
    for remaining in remaining_list:
        if remaining['pair_index'] == random_index:
            index_list_1[remain_index].append(remaining['member'])
        else:
            index_list_1.append([remaining['member']])

    index_list_dict = [i.to_dict() for i in chain.from_iterable(index_list_1)]
    return create_combinations(index_list_dict)


def get_random_index() -> tuple:
    if random.choice([True, False]):
        return (0, 1)
    else:
        return (1, 0)

