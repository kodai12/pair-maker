from abc import ABCMeta, abstractmethod
from typing import List
from more_itertools import chunked
import random


class Combination(metaclass=ABCMeta):
    def __init__(self, combination: list):
        self.combination = combination


class Member:
    def __init__(self, id: int, index: int):
        self.id = id
        self.index = index


class Pair(Combination):
    def __init__(self, members: List[Member]):
        self.members = members

    def divide_member(self):
        return (self.members[0], self.members[1])


class Single(Combination):
    def __init__(self, member: Member):
        self.member = member


def create_combination(combination: List[int]) -> Combination:
    if len(combination) == 1:
        return Single(member=Member(
                id=combination[0],
                index=combination[0] # TODO: indexどうやって取得しようか
            ))
    elif len(combination) == 2:
        return Pair(members=[Member(
            id=c,
            index=c) # TODO: ここもindexどうやって取得しようか
            for index, c in enumerate(combination)])
    else:
        raise Exception('combination length must be 1 or 2')


def create_combinations(combination_index_list: List[int]) -> List[Combination]:
    chunked_list: List[list] = list(chunked(combination_index_list, 2))
    return [create_combination(combination)
            for combination in chunked_list]


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
            new_combinations_index_list.insert(len(combinations), member.id)
        else:
            new_combinations_index_list.insert(remain_index, member.id)

    return create_combinations(new_combinations_index_list)


def _create_random_index(combinations: list) -> tuple:
    random_set_position = random.randrange(2, len(combinations), 2)
    if random_set_position == 2:
        return (2, 4)
    if random_set_position == 4:
        return (4, 2)

