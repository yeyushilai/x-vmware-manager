#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型定义
使用Pydantic进行类型约束和数据验证
"""

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field


# 定义泛型类型变量
T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """通用API响应模型
    
    Args:
        T: 响应数据的类型
    
    Attributes:
        code: 响应状态码，0表示成功
        message: 响应消息
        data: 响应数据
    """
    code: int = Field(description="响应状态码，0表示成功")
    message: str = Field(description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")


# 定义常用的数据类型别名
DatacenterInfo = dict[str, Any]
ClusterInfo = dict[str, Any]
FolderInfo = dict[str, Any]
VmInfo = dict[str, Any]

# 定义列表类型
DatacenterList = list[DatacenterInfo]
ClusterList = list[ClusterInfo]
FolderList = list[FolderInfo]
VmList = list[VmInfo]

# 导出所有模型
__all__ = [
    'ApiResponse',
    'DatacenterInfo',
    'ClusterInfo',
    'FolderInfo',
    'VmInfo',
    'DatacenterList',
    'ClusterList',
    'FolderList',
    'VmList'
]
