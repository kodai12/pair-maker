from abc import ABCMeta, abstractmethod
from typing import List
from lambdalayer.more_itertools import chunked
from itertools import chain
import random

from model.member import Member
from model.member import MemberId
from model.value import Value


class CombinationIndex(Value):
    def __init__(self, value: int):
        self.value = value


class Combination(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, index: CombinationIndex) -> None:
        pass

    @abstractmethod
    def to_dict() -> dict:
        pass

    @abstractmethod
    def skip_member_list() -> List[Member]:
        pass


class Pair(Combination):
    def __init__(self, index: CombinationIndex, memberList: List[Member]) -> None:
        self.index = index
        self.memberList = memberList

    def divide_member(self) -> tuple:
        return (self.memberList[0], self.memberList[1])

    def to_dict(self) -> dict:
        return {
            'index': self.index.value,
            'member': [member.to_dict() for member in self.memberList]
        }

    def get_member_id_list(self) -> List[MemberId]:
        return [member.id for member in self.memberList]

    def skip_member_list(self, weekday: int) -> List[Member]:
        new_index_list = []
        for member in self.memberList:
            if weekday not in member.skip_days.values:
                new_index_list.append(member.to_dict())
        return new_index_list


class Single(Combination):
    def __init__(self, index: CombinationIndex, member: Member) -> None:
        self.index = index
        self.member = member

    def to_dict(self) -> dict:
        return {
            'index': self.index.value,
            'member': self.member.to_dict()
        }

    def get_member_id(self) -> MemberId:
        return self.member.id

    def skip_member_list(self, weekday: int) -> List[Member]:
        return [self.member.to_dict()] if weekday not in self.member.skip_days.values else []


# factory
def create_pair(index: CombinationIndex, member_dict_list: List[dict]) -> Pair:
    return Pair(
        index=index,
        memberList=[
            Member.from_dict(member_dict=member_dict)
            for member_dict in member_dict_list
        ])


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
        all_member_list: List[dict]) -> 'CombinationList':
    # 各メンバーのindexをリストの順番通りに更新
    for index, _ in enumerate(all_member_list):
        all_member_list[index]['index'] = index
    # 2組づつのペアに分割
    chunked_list: List[list] = list(chunked(all_member_list, 2))
    # CombinationListの生成
    return CombinationList([
        create_combination(CombinationIndex(index), member_dict_list)
        for index, member_dict_list in enumerate(chunked_list)
    ])


class CombinationList:
    def __init__(self, values: List[Combination]):
        self.values = values

    def update_combination_list(self) -> 'CombinationList':
        index_stack = []
        remaining_stack = []
        (random_index, remain_index) = self.__get_random_index()
        for combination in self.values:
            # ペアの片方は元のペアに残したままでもう片方はremainingにappendしておく
            if isinstance(combination, Pair):
                (move_member, stay_member) = combination.divide_member()
                index_stack.append([stay_member])
                remaining_stack.append({
                    'combination_index': combination.index.value,
                    'member': move_member
                    })
            # singleの場合はランダム(1番目か2番目)にリストにinsertしておく
            if isinstance(combination, Single):
                index_stack[random_index].append(combination.member)

        # remainingに残ったメンバーをいずれかのペアにinsertする
        for remaining in remaining_stack:
            if remaining['combination_index'] == random_index:
                index_stack[remain_index].append(remaining['member'])
            else:
                index_stack.append([remaining['member']])

        index_list_dict = [i.to_dict() for i in chain.from_iterable(index_stack)]
        return create_combinations(index_list_dict)

    def update_skip_list_member(self, weekday: int) -> 'CombinationList':
        index_stack = []
        for combination in self.values:
            index_stack.append(combination.skip_member_list(weekday))
        index_list_dict = [i for i in chain.from_iterable(index_stack)]
        return create_combinations(index_list_dict)

    def __get_random_index(self) -> tuple:
        if random.choice([True, False]):
            return (0, 1)
        else:
            return (1, 0)

    def get_member_id_list(self) -> List[MemberId]:
        member_id_stack = []
        for combination in self.values:
            if isinstance(combination, Pair):
                member_id_stack.append(combination.get_member_id_list())
            if isinstance(combination, Single):
                member_id_stack.append([combination.get_member_id()])
        return [id for id in chain.from_iterable(member_id_stack)]

    def to_dict(self) -> dict:
        return {
            'pairs': [pair.to_dict() for pair in self.values]
        }
