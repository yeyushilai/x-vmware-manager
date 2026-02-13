#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List


class DescribedEnum(Enum):
    """
    可描述的枚举类基建
    mark: int        唯一标识
    desc: str        描述信息
    """

    def __init__(self, mark: int, desc: str):
        self._mark = mark
        self._desc = desc

    @property
    def mark(self) -> int:
        return self._mark

    @property
    def desc(self) -> str:
        return self._desc

    @classmethod
    def get_all_marks(cls) -> List[int]:
        return [described_enum.mark for described_enum in cls]

    @classmethod
    def get_all_descs(cls) -> List[str]:
        return [described_enum.desc for described_enum in cls]

    @classmethod
    def get_choices(cls):
        return ((described_enum.mark, described_enum.desc) for described_enum in cls)


if __name__ == '__main__':
    class MaliciousType(DescribedEnum):
        BLACK = 0, "黑"
        GREY = 1, "灰"
        WHITE = 2, "白"


    print([_ for _ in MaliciousType.get_choices()])
    print(MaliciousType.get_all_marks())
    print(MaliciousType.get_all_descs())
    print(MaliciousType.BLACK.mark)
    print(MaliciousType.BLACK.desc)
    print(MaliciousType.BLACK.value)
