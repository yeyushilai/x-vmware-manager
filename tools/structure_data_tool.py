#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from typing import Any, Iterable, Generator


class StructureDataTool:

    @classmethod
    def multi_assign_attr_to_obj(cls, instance_obj: Any, **kwargs: Any) -> Any:
        """ 批量给对象赋值 """
        assert isinstance(kwargs, dict)
        assert isinstance(instance_obj, object)
        assert instance_obj is not None

        for key, value in kwargs.items():
            setattr(instance_obj, key, value)
        return instance_obj

    @classmethod
    def chunked(cls, it: Iterable[Any], n: int) -> Generator[list[Any], None, None]:
        """ 手动分页 """
        marker = object()
        for group in (list(g) for g in itertools.zip_longest(
                *[iter(it)] * n, fillvalue=marker)):
            if group[-1] is marker:
                del group[group.index(marker):]
            yield group

    @classmethod
    def order_list_and_paginate(cls, target_list: list[dict[str, Any]], sort_key: str, offset: int, limit: int, reverse: bool = False) -> tuple[list[dict[str, Any]], int]:
        """ 分页 """
        length = len(target_list)
        if length == 0:
            return target_list, length
        page = offset // limit
        target_list.sort(key=lambda x: x.get(sort_key), reverse=reverse)
        if limit <= 0:
            raise Exception("limit must gte 0")
        elif page > (length // limit):
            raise Exception("offset:[%s] out target_list paginate index[%s]" % (offset, length // limit))
        chunk_res = cls.chunked(target_list, limit)
        chunk = next(itertools.islice(chunk_res, page, None))
        return chunk, length


if __name__ == '__main__':
    class A:
        pass


    a = A()

    b = StructureDataTool.multi_assign_attr_to_obj(a, **{"name": 11})
    print(b.name)
