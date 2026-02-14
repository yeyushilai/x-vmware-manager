#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import redis as redis_db
from typing import Callable, Optional, Any

pool_db0 = redis_db.ConnectionPool(host="", port=0, password="", db=0)
redis = redis_db.StrictRedis(connection_pool=pool_db0)


class MRedisLock:
    """
    批量分布式锁，也可用于单条数据加锁
    """

    def __init__(self, prefix: str, err_msg: str, ex: int) -> None:
        self.prefix = prefix
        self.err_msg = err_msg
        self.ex = ex

    def m_acquire(self, suffix_ls: list[str]) -> tuple[bool, str]:
        """
        批量抢锁，一个失败则全失败，全部成功才成功
        失败时会通过判断过期时间做二次抢锁，避免因为宕机导致无法释放锁
        """
        if not suffix_ls:
            return True, ""
        curr_time = int(time.time())
        mapping: dict[str, int] = {f'{str(self.prefix)}:{suffix}': curr_time for suffix in suffix_ls}
        if not redis.msetnx(**mapping):
            # 抢锁失败时，尝试通过时间解锁，成功解锁时重新执行
            ex_release = False
            for k in mapping.keys():
                res = self.release_by_ex(curr_time=curr_time, key=k)
                if res and (not ex_release):
                    ex_release = res
            if not ex_release:
                # 抢锁失败且当前key全部未过期时返回
                return False, self.err_msg
            return self.m_acquire(suffix_ls=suffix_ls)
        # 抢锁成功时，设定过期时间
        for k in mapping.keys():
            redis.expire(k, self.ex)
        return True, ""

    def release_by_ex(self, curr_time: int, key: str) -> bool:
        """
        判断key是否超时，超时则解锁
        成功解锁了超时的key时返回True
        """
        val = redis.get(key)
        if val and ((curr_time - int(val.decode('utf-8'))) >= self.ex):
            redis.delete(key)
            return True
        return False

    def release(self, suffix_ls: list[str]) -> None:
        """
        手动释放锁
        """
        if not suffix_ls:
            return
        keys = [f'{str(self.prefix)}:{suffix}' for suffix in suffix_ls]
        redis.delete(*keys)


class RedisLock:
    """使用setnx实现的redis分布式锁

    :param key_prefix: str, 加锁前缀, 对应某个功能, 形如`supplier_clearing`
    :param error_message: str, 加锁失败的报错消息
    :param lock_period: int, 占锁时间
    """

    def __init__(self, key_prefix: str, error_message: str, lock_period: int) -> None:
        self.key_prefix = key_prefix
        self.error_message = error_message
        self.lock_period = lock_period

    def acquire(self, key_suffix: str) -> tuple[bool, str]:
        """抢锁, 如果抢锁失败返回对应的报错信息

        :param key_suffix: 加锁后缀, 传递给单例的参数
        """
        key = str(self.key_prefix) + ":" + str(key_suffix)
        # if not redis.setnx(key, 1):
        #     return False, self.error_message
        # redis.expire(key, self.lock_period)
        if not redis.set(key, 1, ex=self.lock_period, nx=True):
            return False, self.error_message
        return True, ""

    def release(self, key_suffix: str) -> None:
        """ 手动释放锁 """
        redis.delete(str(self.key_prefix) + ":" + str(key_suffix))

    def check(self, key_suffix: str) -> bool:
        """检查当前是否有锁（不抢锁），如果锁被占用，返回True，否则返回False"""
        key = str(self.key_prefix) + ":" + str(key_suffix)
        if redis.get(key):
            return True
        else:
            return False


if __name__ == '__main__':
    sale_order_lock = RedisLock("sale_order", "已开票，请勿重复提交", 120)

    # 加锁
    success, errmsg = sale_order_lock.acquire("xxxx")
    if not success:
        raise Exception

    # 业务处理

    # 释放锁
    sale_order_lock.release("xxxx")
