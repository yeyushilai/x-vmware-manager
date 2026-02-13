#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import hashlib

AUTH_API_SECRETKEY = ""


class AuthFunc:
    """ 简单接口鉴权 """

    @classmethod
    def _calc_token(cls, timestr):
        """token计算方式"""
        s = AUTH_API_SECRETKEY + timestr
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    @classmethod
    def gen_token(cls):
        """生成token"""
        timestr = datetime.datetime.now().strftime('%Y%m%d%H')
        return cls._calc_token(timestr)

    @classmethod
    def verify_token(cls, token):
        """验证token"""
        # 上一小时的token在这一小时的前5分钟内仍然有效
        token_expire_delay = 5
        now = datetime.datetime.now()
        tokens = {now}
        if now.minute <= token_expire_delay:
            tokens.add(now - datetime.timedelta(hours=1))
        tokens = map(lambda x: x.strftime('%Y%m%d%H'), tokens)
        tokens = map(lambda x: cls._calc_token(x), tokens)
        return token in tokens
