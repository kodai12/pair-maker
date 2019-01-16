from abc import ABCMeta, abstractmethod
from typing import List
from more_itertools import chunked
import random


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
                'member': [{
                    'id': member.id.value,
                    'index': member.index.value,
                    'name': member.name.value
                    } for member in self.memberList]
                }


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
                'member': {
                    'id': self.member.id.value,
                    'index': self.member.index.value,
                    'name': self.member.name.value
                    }
                }


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
    new_combinations_index_list = [0] * len(combinations)
    remaining = []
    (random_index, remain_index) = _create_random_index(combinations)
    for combination in combinations:
        # ペアの片方は元のペアに残したままでもう片方はremainingにappendしておく
        if isinstance(combination, Pair):
            (move_member, stay_member) = combination.divide_member()
            new_combinations_index_list.insert(
                    move_member.index, stay_member.id)
            remaining.append(move_member)
        # singleの場合はrandom(2番目か4番目)にリストにinsertしておく
        if isinstance(combination, Single):
            new_combinations_index_list.insert(
                    random_index, combination.member.id)

    # remainingに残ったメンバーをいずれかのペアにinsertする
    for member in remaining:
        if member.index == random_index:
            new_combinations_index_list.insert(remain_index, member.id)
        else:
            new_combinations_index_list.insert(len(combinations), member.id)

    # 0を詰める
    new_combinations_index_list = list(
            filter(
                lambda x: x != 0, new_combinations_index_list
                ))

    return create_combinations(new_combinations_index_list)


def _create_random_index(combinations: list) -> tuple:
    random_set_position = random.randrange(2, len(combinations), 2)
    if random_set_position == 2:
        return (2, 4)
    if random_set_position == 4:
        return (4, 2)

