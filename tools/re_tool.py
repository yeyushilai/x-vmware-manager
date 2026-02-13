#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class ReTool:

    @classmethod
    def match_ip(cls):
        """ 匹配IP地址 """
        return re.compile('^(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])$')

    @classmethod
    def match_mac(cls):
        """ 匹配MAC地址 """
        return re.compile(r"^([0-9a-fA-F]{2}[:]){5}[0-9a-fA-F]{2}$")
