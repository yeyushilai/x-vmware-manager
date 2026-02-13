#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用日志管理
"""

import os
from loguru import logger

# 确保日志目录存在
log_dir = 'log'
os.makedirs(log_dir, exist_ok=True)

# 配置日志
logger.add(
    os.path.join(log_dir, 'vmware-manager_{time}.log'),
    rotation='1 day',
    retention='7 days',
    compression='zip',
    level='INFO'
)

# 同时输出到控制台
logger.add(
    sink=lambda msg: print(msg, end=""),
    level='DEBUG'
)

# 导出logger实例
__all__ = ['logger']
