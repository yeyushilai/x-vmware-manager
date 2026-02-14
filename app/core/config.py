#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置管理
"""

import os
from typing import Final


class Settings:
    """应用配置类"""
    
    # 服务配置
    DEBUG: Final[bool] = os.environ.get('DEBUG', 'True').lower() == 'true'
    PORT: Final[int] = int(os.environ.get('PORT', '8000'))
    
    # VMware vSphere 配置
    VMWARE_HOST: Final[str] = os.environ.get('VMWARE_HOST', '')
    VMWARE_PORT: Final[str] = os.environ.get('VMWARE_PORT', '443')
    VMWARE_USERNAME: Final[str] = os.environ.get('VMWARE_USERNAME', '')
    VMWARE_PASSWORD: Final[str] = os.environ.get('VMWARE_PASSWORD', '')
    
    @classmethod
    def get_vmware_config(cls) -> dict[str, str]:
        """获取VMware连接配置
        
        Returns:
            dict[str, str]: VMware连接配置字典
        """
        return {
            'host': cls.VMWARE_HOST,
            'port': cls.VMWARE_PORT,
            'username': cls.VMWARE_USERNAME,
            'password': cls.VMWARE_PASSWORD
        }
    
    @classmethod
    def is_vmware_configured(cls) -> bool:
        """检查VMware配置是否完整
        
        Returns:
            bool: 配置是否完整
        """
        return all([
            cls.VMWARE_HOST,
            cls.VMWARE_USERNAME,
            cls.VMWARE_PASSWORD
        ])


# 创建全局配置实例
settings: Final[Settings] = Settings()
