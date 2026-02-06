# -*- coding: utf-8 -*-

from log.logger import logger
from infra.pg import VMwareManagerPGInterface
from platforms.vmware_vsphere import VMwareVSphere
from error import (
    Error,
    ErrorCode,
    ErrorMsg
)
from return_tools import return_error


class BaseVMwareImpl:
    """VMware操作基类，封装通用逻辑"""
    
    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.platform_id = kwargs.get("platform_id")
        self.platform = None
        self.vs = None
    
    def _init_platform(self):
        """初始化平台信息"""
        pi = VMwareManagerPGInterface()
        self.platform = pi.query_platform(platform_id=self.platform_id)
        if not self.platform:
            logger.error("Platform does not exist: platform_id=%s", self.platform_id)
            return False, return_error(self.kwargs,
                                      Error(
                                          ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value,
                                          ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value),
                                      dump=False)
        return True, None
    
    def _init_vsphere(self):
        """初始化VSphere连接"""
        if not self.platform:
            return False, return_error(self.kwargs,
                                      Error(
                                          ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value,
                                          ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value),
                                      dump=False)
        
        account = dict(
            host=self.platform["platform_host"],
            port=self.platform["platform_port"],
            username=self.platform["platform_user"],
            encrypt_password=self.platform["platform_password"]
        )
        
        self.vs = VMwareVSphere(account)
        return True, None
    
    def _handle_connection_error(self, e, account):
        """处理连接错误"""
        if not self.vs.is_connected():
            logger.exception("Failed to connect to VMware vSphere platform: host=%s, username=%s", 
                           account["host"], account["username"])
            return return_error(self.kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False)
        return None
    
    def initialize(self):
        """初始化所有必要的资源"""
        success, error = self._init_platform()
        if not success:
            return False, error
        
        success, error = self._init_vsphere()
        if not success:
            return False, error
        
        return True, None
