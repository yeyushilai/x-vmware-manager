# -*- coding: utf-8 -*-

"""
设置日志名称模块
"""

# 全局日志名称
_global_logger_name = "vmware_manager"


def set_logger_name(name):
    """设置全局日志名称"""
    global _global_logger_name
    _global_logger_name = name


def get_logger_name():
    """获取全局日志名称"""
    return _global_logger_name
