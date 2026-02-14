#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import hashlib
from typing import Optional


AUTH_API_SECRETKEY: str = ""


class AuthFunc:
    """ 简单接口鉴权 """

    @classmethod
    def _calc_token(cls, timestr: str) -> str:
        """token计算方式"""
        s: str = AUTH_API_SECRETKEY + timestr
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    @classmethod
    def gen_token(cls) -> str:
        """生成token"""
        timestr: str = datetime.datetime.now().strftime('%Y%m%d%H')
        return cls._calc_token(timestr)

    @classmethod
    def verify_token(cls, token: str) -> bool:
        """验证token"""
        # 上一小时的token在这一小时的前5分钟内仍然有效
        token_expire_delay: int = 5
        now: datetime.datetime = datetime.datetime.now()
        tokens: set[datetime.datetime] = {now}
        if now.minute <= token_expire_delay:
            tokens.add(now - datetime.timedelta(hours=1))
        tokens_list: list[str] = list(map(lambda x: x.strftime('%Y%m%d%H'), tokens))
        tokens_list = list(map(lambda x: cls._calc_token(x), tokens_list))
        return token in tokens_list
