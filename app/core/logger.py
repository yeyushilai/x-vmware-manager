#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用日志管理
"""

import os
from typing import Callable, Final
from loguru import logger

# 确保日志目录存在
log_dir: Final[str] = 'logs'
os.makedirs(log_dir, exist_ok=True)

# 移除默认的控制台处理器，避免重复输出
logger.remove()

# 配置日志输出到文件
logger.add(
    os.path.join(log_dir, 'vmware-manager_{time}.log'),
    rotation='1 day',
    retention='7 days',
    compression='zip',
    level='INFO',
    enqueue=True
)

# 配置日志输出到控制台
console_sink: Callable[[str], None] = lambda msg: print(msg, end="")
logger.add(
    sink=console_sink,
    level='DEBUG',
    enqueue=True
)

# 导出logger实例
__all__: Final[list[str]] = ['logger']
