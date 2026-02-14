#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Any, Callable
from collections import namedtuple

import numpy as np
import pandas as pd


class DataAnalyticTool:
    """数据分析工具类

    使用示例:
        aly = DataAnalyticTool(
            ("goods_id", "storage"),
            [
                (1, 2),
                (2, 10),
                (2, 500)
            ]
        )
        result = aly.filter("goods_id IN (1, 2, 3) or storage < 600").order_by("goods_id desc, storage").limit(0, 1).all()
        result = aly.filter("col_name.str.contains('diy_string')")

    :param header: 表头
    :param table: 数据行组成的列表
    """

    @staticmethod
    def my_name_tuple(tuplename: str, filed_list: list[str]) -> type:
        def __setattr__(self: Any, key: str, value: Any) -> None:
            self.__dict__[key] = value

        tuple_class = namedtuple(tuplename, filed_list)
        my_tuple = type(tuplename, (tuple_class,), {"__setattr__": __setattr__})
        return my_tuple

    def __init__(self, header: tuple[str, ...], table: list[tuple[Any, ...]]) -> None:
        self.df = pd.DataFrame(table, columns=header).fillna(0)
        self.Result = self.my_name_tuple("Result", list(header))

    def sum_columns(self, columns: tuple[str, ...]) -> Any:
        """ 多列求和 """
        Result = self.my_name_tuple("Result", list(columns))
        return Result._make(self.df[list(columns)].sum())

    def filter(self, sql: str) -> 'DataAnalyticTool':
        """ 过滤 """
        sql = re.sub(r"[A-Za-z ]+(=)?", lambda mo: mo.group(0).replace("=", "=="), sql)
        self.df.query(sql.lower(), inplace=True)
        return self

    def order_by(self, sql: str) -> 'DataAnalyticTool':
        """ 根据某列对数据排序 """
        if not sql:
            raise ValueError("必须传入有效条件")
        conditions = sql.split(",")
        by: list[str] = []
        ascending: list[bool] = []
        for condition in conditions:
            cond = list(filter(None, condition.split(" ")))
            if len(cond) == 1:
                by.append(cond[0])
                ascending.append(True)
            elif len(cond) == 2:
                by.append(cond[0])
                if cond[1] == "asc":
                    ascending.append(True)
                elif cond[1] == "desc":
                    ascending.append(False)
                else:
                    raise ValueError("排序条件语法错误")
            else:
                raise ValueError("排序条件语法错误")

        self.df = self.df.sort_values(by=by, ascending=ascending)
        return self

    def limit(self, offset: int, page_size: int) -> 'DataAnalyticTool':
        """ 分页 """
        self.df = self.df.iloc[offset: offset + page_size]
        return self

    def distinct(self, col: str) -> set[Any]:
        """去除重复项，可以用来做表头筛选

        :param col: 需要进行去重的列
        """
        return {_ for _ in self.df[col].unique() if not np.isnan(_)}

    def count(self) -> int:
        """ 计数 """
        return len(self.df)

    def all(self) -> list[Any]:
        """ 获取全部数据 """
        return list(map(self.Result._make, self.df.values))

    def join(self, analytic_obj: 'DataAnalyticTool', how: str = "outer") -> 'DataAnalyticTool':
        """在内存中进行 join, 对 pandas merge 方法的封装
        默认为外连接, 主要用来解决 MySQL 不支持 full outer join 语法
        两个对象 join 的时候, 必须确保有同名键

        :param analytic_obj: `DataAnalyticTool`对象
        :param how: 连接方式, 默认为外连接, 同时支持 inner left right

        :return: `DataAnalyticTool`对象
        """
        r = self.df.merge(analytic_obj.df, how=how)
        return DataAnalyticTool(tuple(r.columns), np.array(r))

    def append_column(self, col_name: str, rule: Callable) -> 'DataAnalyticTool':
        """给DataFrame增加一列

        :param col_name: 新列的名字
        :param rule: 计算规则的函数
        """
        if len(self.df) > 0:
            self.df[col_name] = self.df.apply(rule, axis=1)
        else:
            self.df[col_name] = 0
        return DataAnalyticTool(tuple(self.df.columns), np.array(self.df))

    def serailize(self, *args: Any, **kwargs: Any) -> None:
        """ 序列化结果 """
        raise NotImplementedError

    def group_by(self, *args: str) -> 'DataAnalyticTool':
        """
        :params args: 需要分组的列
        注意会把分组求和, 只会有数字, 字符串会过滤掉
        """
        gdf = self.df.groupby(args).sum().reset_index()
        return self.__class__(tuple(gdf.columns), np.array(gdf))
