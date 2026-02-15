#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置管理
支持从环境变量和YAML配置文件读取配置
"""

import os
from typing import Final, Any
from pathlib import Path
import yaml


class Settings:
    """应用配置类"""
    
    # 配置文件路径
    CONFIG_FILE_PATH: Final[str] = 'config.yaml'
    
    # 默认配置
    _DEFAULT_CONFIG: Final[dict[str, Any]] = {
        'server': {
            'debug': True,
            'port': 8000
        },
        'vmware': {
            'host': '',
            'port': '443',
            'username': '',
            'password': ''
        },
        'logging': {
            'level': 'INFO',
            'file_path': 'logs/app.log',
            'rotation': '1 day',
            'retention': '7 days'
        }
    }
    
    def __init__(self) -> None:
        """初始化配置"""
        self._config: dict[str, Any] = self._load_config()
    
    def _load_config(self) -> dict[str, Any]:
        """加载配置
        
        优先级：环境变量 > YAML配置文件 > 默认配置
        
        Returns:
            dict[str, Any]: 合并后的配置
        """
        config: dict[str, Any] = self._DEFAULT_CONFIG.copy()
        
        # 从YAML文件加载配置
        config_file: Path = Path(self.CONFIG_FILE_PATH)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    file_config: dict[str, Any] = yaml.safe_load(f) or {}
                # 合并YAML配置
                self._merge_config(config, file_config)
            except Exception as e:
                print(f"警告: 无法加载配置文件 {self.CONFIG_FILE_PATH}: {e}")
        
        # 从环境变量加载配置（优先级最高）
        self._load_from_env(config)
        
        return config
    
    def _merge_config(self, base: dict[str, Any], override: dict[str, Any]) -> None:
        """递归合并配置
        
        Args:
            base: 基础配置字典
            override: 要覆盖的配置字典
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _load_from_env(self, config: dict[str, Any]) -> None:
        """从环境变量加载配置
        
        Args:
            config: 配置字典
        """
        # 服务配置
        if os.environ.get('DEBUG'):
            config['server']['debug'] = os.environ.get('DEBUG').lower() == 'true'
        if os.environ.get('PORT'):
            config['server']['port'] = int(os.environ.get('PORT'))
        
        # VMware配置
        if os.environ.get('VMWARE_HOST'):
            config['vmware']['host'] = os.environ.get('VMWARE_HOST')
        if os.environ.get('VMWARE_PORT'):
            config['vmware']['port'] = os.environ.get('VMWARE_PORT')
        if os.environ.get('VMWARE_USERNAME'):
            config['vmware']['username'] = os.environ.get('VMWARE_USERNAME')
        if os.environ.get('VMWARE_PASSWORD'):
            config['vmware']['password'] = os.environ.get('VMWARE_PASSWORD')
    
    @property
    def DEBUG(self) -> bool:
        return self._config['server']['debug']
    
    @property
    def PORT(self) -> int:
        return self._config['server']['port']
    
    @property
    def VMWARE_HOST(self) -> str:
        return self._config['vmware']['host']
    
    @property
    def VMWARE_PORT(self) -> str:
        return self._config['vmware']['port']
    
    @property
    def VMWARE_USERNAME(self) -> str:
        return self._config['vmware']['username']
    
    @property
    def VMWARE_PASSWORD(self) -> str:
        return self._config['vmware']['password']
    
    @property
    def LOG_LEVEL(self) -> str:
        return self._config['logging']['level']
    
    @property
    def LOG_FILE_PATH(self) -> str:
        return self._config['logging']['file_path']
    
    @property
    def LOG_ROTATION(self) -> str:
        return self._config['logging']['rotation']
    
    @property
    def LOG_RETENTION(self) -> str:
        return self._config['logging']['retention']
    
    def get_vmware_config(self) -> dict[str, str]:
        """获取VMware连接配置
        
        Returns:
            dict[str, str]: VMware连接配置字典
        """
        return {
            'host': self.VMWARE_HOST,
            'port': self.VMWARE_PORT,
            'username': self.VMWARE_USERNAME,
            'password': self.VMWARE_PASSWORD
        }
    
    def is_vmware_configured(self) -> bool:
        """检查VMware配置是否完整
        
        Returns:
            bool: 配置是否完整
        """
        return all([
            self.VMWARE_HOST,
            self.VMWARE_USERNAME,
            self.VMWARE_PASSWORD
        ])


# 创建全局配置实例
settings: Final[Settings] = Settings()
