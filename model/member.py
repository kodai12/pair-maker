from typing import List


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


