#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VMware服务管理
"""

from typing import Optional, Final
from vmware import VMwareVSphere
from app.core.config import settings
from app.core.logger import logger

# 全局VMware客户端实例
vmware_client: Optional[VMwareVSphere] = None


def get_vmware_client() -> Optional[VMwareVSphere]:
    """获取VMware客户端实例
    
    Returns:
        Optional[VMwareVSphere]: VMware客户端实例
    """
    global vmware_client
    if vmware_client is None:
        if not settings.is_vmware_configured():
            logger.error("VMware配置不完整")
            return None
        
        account: dict[str, str] = settings.get_vmware_config()
        vmware_client = VMwareVSphere(account)
        
        if not vmware_client.is_connected():
            logger.error("无法连接到VMware vSphere")
            vmware_client = None
    return vmware_client


def reset_vmware_client() -> None:
    """重置VMware客户端实例
    
    Returns:
        None
    """
    global vmware_client
    vmware_client = None
    logger.info("VMware客户端实例已重置")
