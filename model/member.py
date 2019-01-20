from typing import List

from model.value import Value


class MemberId(Value):
    def __init__(self, value: int):
        self.value = value


class MemberIndex(Value):
    def __init__(self, value: int):
        self.value = value


class MemberName(Value):
    def __init__(self, value: str):
        self.value = value


class SkipDays(Value):
    def __init__(self, values: List[int]):
        self.values = values


class Member:
    def __init__(self, id: MemberId, index: MemberIndex, name: MemberName, skip_days: SkipDays) -> None:
        self.id = id
        self.index = index
        self.name = name
        self.skip_days = skip_days

    @staticmethod
    def from_dict(member_dict: dict) -> 'Member':
        return Member(
            id=MemberId(member_dict['id']),
            index=MemberIndex(member_dict['index']),
            name=MemberName(member_dict['name']),
            skip_days=SkipDays(member_dict['skip_days']))

    def to_dict(self) -> dict:
        return {
            'id': self.id.value,
            'index': self.index.value,
            'name': self.name.value,
            'skip_days': self.skip_days.values
        }

    def to_flat_list(self) -> List[str]:
        return [self.id.value, self.index.value, self.name.value, self.skip_days.values]

