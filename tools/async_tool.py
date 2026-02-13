#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from functools import partial
from concurrent import futures

"""
准备工作：
1. 导入asyncio包，要求python解释器版本> 3.3

"""


def pool_runner(func, arg_list: list, max_workers: int = 4):
    """ run task in thread pool
    arg_list should contains args and kwargs stored in a tuple, eg:
    [
        (
            [1,2,3],
            {'zone': 'beta'}
        ),
        (
            [4,5,6],
            {'zone': 'delta'}
        ),
    ]
    set args to blank list [] if not used
    set kwargs to blank dict {} if not used
    """

    result_list = []
    if not arg_list:
        return result_list

    executor = futures.ThreadPoolExecutor(max_workers=max_workers)
    loop = asyncio.new_event_loop()

    future_list = []
    for args, kwargs in arg_list:
        func_to_run = partial(func, *args, **kwargs)
        future_list.append(loop.run_in_executor(executor, func_to_run))

    result_list = loop.run_until_complete(asyncio.gather(*future_list, return_exceptions=True))
    loop.close()

    return result_list
