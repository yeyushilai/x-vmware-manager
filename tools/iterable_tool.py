#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import Iterable, Iterator


class IterableTool:

    @classmethod
    def is_iterable_empty(cls, iterable):
        """判断可迭代对象是否为空"""
        return not any(iterable)

    @classmethod
    def is_iterable(cls, variable):
        """判断是否为可迭代对象"""
        return isinstance(variable, Iterable)

    @classmethod
    def is_iterator_empty(cls, iterator):
        """判断迭代器是否为空"""
        return not any(iterator)

    @classmethod
    def is_iterator(cls, variable):
        """判断是否为迭代器"""
        return isinstance(variable, Iterator)


if __name__ == '__main__':
    print(IterableTool.is_iterator_empty(range(6)))
    print(IterableTool.is_iterator_empty(range(0)))
    print(IterableTool.is_iterator((x for x in range(6))))
    print(IterableTool.is_iterable((x for x in range(6))))
    print(IterableTool.is_iterable_empty(range(5)))
