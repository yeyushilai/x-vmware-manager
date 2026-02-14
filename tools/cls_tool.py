#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any


class ComplexObject:
    """
    这个类主要用于封装复杂的数据结构。
    之所以要用这么个东西，是因为python的对象太灵活，我们可以随意的给一个对象添加任意属性，如obj.x = 123
    我们需要一个确定、严格限制的结构来封装数据

    python提供了一个内置的属性__slots__，可以用于限制class能添加的属性。
    如果添加了__slots__定义之外的属性，系统会报错

    使用方法：
        重新定义一个class，继承自该class，重新定义__slots__即可，__slots__中定义的属性会统一初始化为None
        eg:
            class MyComplexObject(ComplexObject):
                __slots__ = ["name", "age"]

    注意：
        __slots__定义的属性仅对当前类生效，对继承的子类是不起作用的。
        我们必须在子类中也定义__slots__，这样，子类允许定义的属性就是自身的__slots__加上父类的__slots__
    """

    __slots__: tuple = tuple()

    def __init__(self) -> None:
        super(ComplexObject, self).__init__()
        # 把__slots__里的属性都初始化为None
        for attr in self.__slots__:
            setattr(self, attr, None)

    def __str__(self) -> str:
        result_str: str = ""
        for attr in self.__slots__:
            item: Any = getattr(self, attr)
            if (
                    isinstance(item, list)
                    or isinstance(item, tuple)
                    or isinstance(item, set)
            ):
                temp_str: str = ",".join(str(getattr(_, "id", "-")) for _ in item)
            elif isinstance(item, dict):
                temp_str = ",".join(str(_) for _ in item)
            else:
                temp_str = str(getattr(item, "id", "-"))
            result_str += f"{attr}:{temp_str}\n"
        return result_str


class ClassSyntax:

    def __new__(cls) -> None:
        # 禁止实例化
        raise Exception


if __name__ == '__main__':
    pass
