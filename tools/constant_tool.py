#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Redis:
    """使用类定义关联常量"""
    SERVER = 'localhost'
    PORT = 6379
    PASSWORD = ''
    SG_SERVER = "localhost"
    SG_PORT = 6383
    SG_PASSWORD = ""


class DateTimeFormatter:
    """日期时间格式化器"""
    YEAR = "%Y"
    MONTH = "%Y-%m"
    DATE = "%Y-%m-%d"
    TIME = "%Y-%m-%d %H:%M:%S"


NUM_ARABIC_TO_CH_MAP = {
    0: '零',
    1: '一',
    2: '二',
    3: '三',
    4: '四',
    5: '五',
    6: '六',
    7: '七',
    8: '八',
    9: '九'
}

NUM_CH_TO_ARABIC_MAP = {
    '零': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9
}

NUM_ARABIC_TO_TRA_CH_MAP = {
    0: '零',
    1: '壹',
    2: '贰',
    3: '叁',
    4: '肆',
    5: '伍',
    6: '陆',
    7: '柒',
    8: '捌',
    9: '玖'
}
