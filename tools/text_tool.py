#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import zlib
import difflib
import hashlib

from pypinyin import Style, pinyin

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


class TextTool:

    @classmethod
    def get_same_start_end(cls, pattern):
        """获取最长前后缀相同的字符位数"""
        n = len(pattern)
        result_list = [0] * n

        # pattern为单个字符，认为它没有公共头尾
        if n <= 1:
            return result_list

        i = 2
        while i < n:
            if pattern[i - 1] == pattern[result_list[i - 1]]:
                result_list[i] = result_list[i - 1] + 1
            i += 1
        return result_list

    @classmethod
    def match_sub_str(cls, string, pattern):
        """
            用来在字符串中搜索一个子字符串
            使用kmp算法
            string是字符串，pattern是模式字符串
            返回值为匹配到的第一个字符串的第一个字符的索引，没匹配到返回-1
            算法时间复杂度O(n)
        """
        s_length = len(string)
        p_length = len(pattern)
        i = 0  # 指向string
        j = 0  # 指向pattern
        next_list = cls.get_same_start_end(pattern)
        while i < s_length:
            if string[i] == pattern[j]:  # 匹配
                if j == p_length - 1:
                    return i + 1 - p_length  # 子串匹配到尾部，命中，返回匹配的起始位置
                else:
                    i += 1
                    j += 1
            else:
                if j == 0:
                    i += 1  # j已经在串首，说明第一个字符不匹配，不必再回溯子串，主串迭代进1
                else:
                    j = next_list[j]  # 失配，j回溯，回溯的目标位置是已经匹配到的子串的头尾公共部分的长度处
        return -1  # 查找失败

    @classmethod
    def is_str(cls, value):
        """ 判断变量的值是否为字符串 """
        if (not isinstance(value, str)) and (not isinstance(value, bytes)):
            return False
        return True

    @classmethod
    def is_all_chinese(cls, value):
        """ 检验是否全是中文字符 """
        for _char in value:
            if not u'\u4e00' <= _char <= u'\u9fff':
                return False
        return True

    @classmethod
    def is_contains_chinese(cls, value):
        """ 检验是否含有中文字符 """
        for _char in value:
            if u'\u4e00' <= _char <= u'\u9fff':
                return True
        return False

    @classmethod
    def is_md5_value(cls, value):
        """使用正则表达式检查是否为32个十六进制字符"""
        md5_pattern = re.compile(r"^[0-9a-fA-F]{32}$")
        return bool(md5_pattern.match(value))

    @classmethod
    def is_sha1_value(cls, value):
        """使用正则表达式检查是否为40个十六进制字符"""
        sha1_pattern = re.compile(r"^[0-9a-fA-F]{40}$")
        return bool(sha1_pattern.match(value))

    @classmethod
    def is_sha256_value(cls, value):
        """使用正则表达式检查是否为64个十六进制字符"""
        sha256_pattern = re.compile(r"^[0-9a-fA-F]{64}$")
        return bool(sha256_pattern.match(value))

    @classmethod
    def calculate_crc32(cls, value):
        crc32_value = zlib.crc32(value.encode("utf-8"))
        return crc32_value

    @classmethod
    def calculate_md5(cls, value):
        md5_hash = hashlib.md5()
        md5_hash.update(value.encode("utf-8"))
        return md5_hash.hexdigest()

    @classmethod
    def calculate_sha1(cls, value):
        sha1_hash = hashlib.sha1()
        sha1_hash.update(value.encode("utf-8"))
        return sha1_hash.hexdigest()

    @classmethod
    def calculate_sha256(cls, value):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(value.encode("utf-8"))
        return sha256_hash.hexdigest()

    @staticmethod
    def get_char_max_index(text, char):
        """获取文本中某一个字符的最大索引"""
        return max([i for i, _ in enumerate(text) if _ == char])

    @staticmethod
    def string_similar(str1, str2):
        """计算文本相似度"""
        return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

    @staticmethod
    def convert_ch_to_arabic(text):
        """将文本中的汉字数字转换为拼音数字"""
        return (
            "".join(
                (
                    str(NUM_CH_TO_ARABIC_MAP.get(_))
                    if _ in NUM_CH_TO_ARABIC_MAP.keys() else _
                    for _ in text
                )
            )
        )

    @staticmethod
    def hanzi_to_pinyin(hanzi_name):
        """汉字转为拼音（基础版）"""
        return (
            "".join(
                (
                    pinyin_ls[0]
                    for pinyin_ls
                    in pinyin(
                        hanzi_name,
                        style=Style.NORMAL,
                        errors='ignore',
                        strict=False,
                        heteronym=True
                    )
                )
            )
        )

    @staticmethod
    def advanced_hanzi_to_pinyin(hanzi_name):
        """汉字转为拼音（高级版）

        高级特色：
        1.汉字中如果有阿拉伯数字，则将阿拉伯数字先转为汉字数字，而后再转为汉字拼音
        """
        str_arabic_list = [str(_) for _ in NUM_ARABIC_TO_TRA_CH_MAP.keys()]

        return (
            "".join(
                (
                    pinyin_ls[0]
                    for pinyin_ls
                    in pinyin(
                        "".join(
                            (
                                NUM_ARABIC_TO_TRA_CH_MAP[int(_)]
                                if _.isdigit() and _ in str_arabic_list else _
                                for _ in hanzi_name
                            )
                        ),
                        style=Style.NORMAL,
                        errors='ignore',
                        strict=False,
                        heteronym=True
                    )
                )
            )
        )


if __name__ == '__main__':
    print(TextTool.is_str(u"xxx"))
    print(TextTool.is_contains_chinese("我们中国ss"))
    print(TextTool.is_all_chinese("我们中国ss"))
    print(TextTool.is_contains_chinese("ss"))
    print(TextTool.is_all_chinese("ss"))
    print(TextTool.calculate_crc32("106.75.54.33"))
    print(TextTool.calculate_crc32("2.57.122.123"))
    print(TextTool.calculate_md5("2.57.122.123"))
    print(TextTool.calculate_sha1("2.57.122.123"))
    print(TextTool.calculate_sha256("2.57.122.123"))
    print(TextTool.is_md5_value("7daad22ca20b7fef23fea40ba37d0315"))
    print(TextTool.is_sha256_value("045bb77ae9f41e4e8df7681af68c7ad4ede3ebc27dbd9dfbf79e3bdc674023f3"))
