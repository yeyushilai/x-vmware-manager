# -*- coding: utf-8 -*-

import re
import random
from datetime import datetime, timedelta

from log.logger import logger
from utils.common import (
    format_value_by_timeslice,
    order_list_and_paginate
)

from platforms.vmware_vsphere import VMwareVSphere
from error import (
    Error,
    ErrorCode,
    ErrorMsg
)
from return_tools import (
    return_error,
    return_success
)
from constants import (
    METRIC_CN_MAPPING,
    METRIC_COUNTER_MAPPING,
    METRIC_UNIT_MAPPING,

    PlatformVMwareToolsStatus,
    PlatformVmOperationType,
    PlatformVmStatus
)

from handlers.impl.base_impl import BaseVMwareImpl

import context
ctx = context.instance()


def handle_describe_vm_local(kwargs):
    offset = kwargs.get("offset") or 0
    limit = kwargs.get("limit") or 10
    search_word = kwargs.get("search_word")
    sort_key = kwargs.get("sort_key") or "name"
    reverse = bool(kwargs.get("reverse"))

    # 初始化基础实现
    base_impl = BaseVMwareImpl(kwargs)
    success, error = base_impl.initialize()
    if not success:
        return error

    # 获取VM列表
    try:
        raw_vm_list = base_impl.vs.list_vm()
    except (Exception, SystemExit) as e:
        account = dict(
            host=base_impl.platform["platform_host"],
            port=base_impl.platform["platform_port"],
            username=base_impl.platform["platform_user"],
            encrypt_password=base_impl.platform["platform_password"]
        )
        conn_error = base_impl._handle_connection_error(e, account)
        if conn_error:
            return conn_error
        logger.error("Failed to list VMs: platform_id=%s, reason=%s", base_impl.platform_id, str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_LIST_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_LIST_VM_ERROR.value),
                            dump=False)

    # 搜索
    vm_list = list()
    for vm_info in raw_vm_list:
        if search_word:
            match_len = re.findall(r'%s.*' % search_word, vm_info["name"])
            if len(match_len) == 0:
                continue
        vm_list.append(vm_info)

    # 排序、分页
    try:
        result_list, count = order_list_and_paginate(vm_list, sort_key, offset,
                                                     limit, reverse)
        result_list = result_list or []
        count = count or 0
    except Exception as e:
        logger.exception("Error ordering and paginating VMs: reason=%s", str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_ORDER_PAGINATE_VMS_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_ORDER_PAGINATE_VMS_ERROR.value),
                            dump=False)

    data = dict(datas=result_list, count=count)
    return return_success(kwargs, data, dump=False)


def handle_detail_vm_local(kwargs):
    vm_id = kwargs.get("vm_id")

    # 初始化基础实现
    base_impl = BaseVMwareImpl(kwargs)
    success, error = base_impl.initialize()
    if not success:
        return error

    # 获取VM详细信息
    try:
        vm_data = base_impl.vs.get_vm(vm_uuid=vm_id)
    except (Exception, SystemExit) as e:
        account = dict(
            host=base_impl.platform["platform_host"],
            port=base_impl.platform["platform_port"],
            username=base_impl.platform["platform_user"],
            encrypt_password=base_impl.platform["platform_password"]
        )
        conn_error = base_impl._handle_connection_error(e, account)
        if conn_error:
            return conn_error
        logger.exception("Failed to get VM info: platform_id=%s, vm_id=%s, reason=%s", 
                       base_impl.platform_id, vm_id, str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value),
                            dump=False
                            )

    if not vm_data:
        logger.error("VM does not exist: platform_id=%s, vm_id=%s", base_impl.platform_id, vm_id)
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_VM_NOT_EXISTS.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_VM_NOT_EXISTS.value),
                            dump=False)

    data = dict(data=vm_data)
    return return_success(kwargs, data, dump=False)


def handle_monitor_vm_local(kwargs):
    vm_uuid = kwargs.get("vm_uuid")
    user_id = kwargs.get("user_id")
    metrics = kwargs.get("metrics")
    interval = kwargs.get("interval")

    # 初始化基础实现
    base_impl = BaseVMwareImpl(kwargs)
    success, error = base_impl.initialize()
    if not success:
        return error

    # 获取虚拟机对象
    try:
        vm_obj = base_impl.vs.vi.get_vm_by_uuid(vm_uuid=vm_uuid)
    except (Exception, SystemExit) as e:
        account = dict(
            host=base_impl.platform["platform_host"],
            port=base_impl.platform["platform_port"],
            username=base_impl.platform["platform_user"],
            encrypt_password=base_impl.platform["platform_password"]
        )
        conn_error = base_impl._handle_connection_error(e, account)
        if conn_error:
            return conn_error
        logger.exception("Failed to get VM: platform_id=%s, vm_id=%s, reason=%s", 
                       base_impl.platform_id, vm_uuid, str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value),
                            dump=False)
    
    logger.debug("Successfully got VM object: name=%s", vm_obj.name)

    # 获取couter - metric 映射关系
    counter_id_dict = base_impl.vs.vi.get_counter_dict()
    counterid_metric_dict = {
        counter_id_dict.get(METRIC_COUNTER_MAPPING.get(metric)): metric for
        metric in metrics}
    
    logger.debug("Counter to metric mapping: %s", counterid_metric_dict)

    # 获取对应metric监控数据
    nowtime = datetime.now()
    start_time = nowtime - timedelta(minutes=80)
    end_time = nowtime - timedelta(minutes=1)
    
    try:
        result = base_impl.vs.vi.BuildQuery(
            start_time=start_time,
            end_time=end_time,
            counterIds=list(counterid_metric_dict.keys()),
            instance="",
            entity=vm_obj,
        )
    except Exception as e:
        logger.exception("Failed to build monitoring query: reason=%s", str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value),
                            dump=False)
    
    result_data = {"data": [], "ret_code": 0, "total_count": 0}
    if result:
        value = result[0].value
        value_start_time = result[0].sampleInfo[0].timestamp + timedelta(hours=8)
        
        for metric_data in value:
            counterid = metric_data.id.counterId
            metric = counterid_metric_dict.get(counterid)
            if not metric:
                continue
                
            monitor_data = format_value_by_timeslice(metric_data.value,
                                                     value_start_time,
                                                     metric, interval)
            item = {
                "monitor_data": monitor_data,
                "resource_id": vm_uuid,
                "metric_name": metric,
                "metric_cn_name": METRIC_CN_MAPPING.get(metric, metric),
                "metric_unit": METRIC_UNIT_MAPPING.get(metric, ""),
                "create_time": "",
                "description": METRIC_CN_MAPPING.get(metric, metric),
                "step": 20,
                "tags": "",
                "user_id": user_id
            }
            result_data["data"].append(item)
        
        result_data["total_count"] = len(result_data["data"])
        logger.debug("Monitoring data retrieved successfully: metrics_count=%s", result_data["total_count"])
    
    return return_success(kwargs, result_data, dump=False)


def handle_operate_vm_local(kwargs):
    vm_id = kwargs.get("vm_id")
    operation = kwargs.get("operation")

    # 初始化基础实现
    base_impl = BaseVMwareImpl(kwargs)
    success, error = base_impl.initialize()
    if not success:
        return error

    # 若动作为重启操作系统和关闭操作系统，虚拟机必须安装且运行了VMware Tools
    if operation in [
        PlatformVmOperationType.REBOOT.value,
        PlatformVmOperationType.SHUTDOWN.value
    ]:
        try:
            vm_info = base_impl.vs.get_vm(vm_uuid=vm_id)
        except (Exception, SystemExit) as e:
            account = dict(
                host=base_impl.platform["platform_host"],
                port=base_impl.platform["platform_port"],
                username=base_impl.platform["platform_user"],
                encrypt_password=base_impl.platform["platform_password"]
            )
            conn_error = base_impl._handle_connection_error(e, account)
            if conn_error:
                return conn_error
            logger.exception("Failed to get VM info: platform_id=%s, vm_id=%s, reason=%s", 
                           base_impl.platform_id, vm_id, str(e))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value),
                                dump=False)

        assert "vmware_tools_status" in vm_info
        if vm_info["vmware_tools_status"] != PlatformVMwareToolsStatus.TOOLSOK.value:
            logger.error("VMware Tools status is not OK: platform_id=%s, vm_id=%s, operation=%s, status=%s", 
                       base_impl.platform_id, vm_id, operation, vm_info["vmware_tools_status"])
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_VM_VMWARE_TOOLS_NOT_OK.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_VM_VMWARE_TOOLS_NOT_OK.value),
                                dump=False)

    try:
        base_impl.vs.operate_vm(vm_id, operation)
        logger.debug("Successfully operated VM: platform_id=%s, vm_id=%s, operation=%s", 
                   base_impl.platform_id, vm_id, operation)
    except (Exception, SystemExit) as e:
        logger.exception("Failed to operate VM: platform_id=%s, vm_id=%s, operation=%s, reason=%s", 
                       base_impl.platform_id, vm_id, operation, str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_OPERATE_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_OPERATE_VM_ERROR.value),
                            dump=False)
    
    data = dict(platform_id=base_impl.platform_id, vm_id=vm_id)
    return return_success(kwargs, dict(data=data), dump=False)


def handle_update_vm_local(kwargs):
    vm_id = kwargs.get("vm_id")
    vm_name = kwargs.get("vm_name")
    vm_note = kwargs.get("vm_note")

    vm_info = dict()
    if vm_name:
        vm_info["vm_name"] = vm_name
    if vm_note:
        vm_info["vm_note"] = vm_note

    # 初始化基础实现
    base_impl = BaseVMwareImpl(kwargs)
    success, error = base_impl.initialize()
    if not success:
        return error
    
    try:
        base_impl.vs.update_vm(vm_uuid=vm_id, vm_info=vm_info)
        logger.debug("Successfully updated VM: platform_id=%s, vm_id=%s, info=%s", 
                   base_impl.platform_id, vm_id, vm_info)
    except (Exception, SystemExit) as e:
        account = dict(
            host=base_impl.platform["platform_host"],
            port=base_impl.platform["platform_port"],
            username=base_impl.platform["platform_user"],
            encrypt_password=base_impl.platform["platform_password"]
        )
        conn_error = base_impl._handle_connection_error(e, account)
        if conn_error:
            return conn_error
        logger.exception("Failed to update VM config: platform_id=%s, vm_id=%s, info=%s, reason=%s", 
                       base_impl.platform_id, vm_id, vm_info, str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_UPDATE_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_UPDATE_VM_ERROR.value),
                            dump=False)

    data = dict(platform_id=base_impl.platform_id, vm_id=vm_id)
    return return_success(kwargs, dict(data=data), dump=False)


def handle_detail_vm_ticket_local(kwargs):
    vm_id = kwargs.get("vm_id")

    # 初始化基础实现
    base_impl = BaseVMwareImpl(kwargs)
    success, error = base_impl.initialize()
    if not success:
        return error

    try:
        vm_ticket = base_impl.vs.get_vm_ticket(vm_id)
        logger.debug("Successfully obtained VM ticket: platform_id=%s, vm_id=%s", 
                   base_impl.platform_id, vm_id)
    except (Exception, SystemExit) as e:
        account = dict(
            host=base_impl.platform["platform_host"],
            port=base_impl.platform["platform_port"],
            username=base_impl.platform["platform_user"],
            encrypt_password=base_impl.platform["platform_password"]
        )
        conn_error = base_impl._handle_connection_error(e, account)
        if conn_error:
            return conn_error
        # 检查虚拟机状态
        # 只有在开机状态下才能拿到ticket
        vm_power_status = base_impl.vs.get_vm_power_status(vm_id)
        if vm_power_status != PlatformVmStatus.POWEREDON.value:
            logger.error("VM power status is not poweredOn: platform_id=%s, vm_id=%s, status=%s", 
                       base_impl.platform_id, vm_id, vm_power_status)
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_VM_INVALID_VM_POWERSTATUS.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_VM_INVALID_VM_POWERSTATUS.value),
                                dump=False)

        logger.exception("Failed to get VM ticket: platform_id=%s, vm_id=%s, reason=%s", 
                       base_impl.platform_id, vm_id, str(e))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_TICKET_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_TICKET_ERROR.value),
                            dump=False)

    # 获取代理主机和端口
    data = {
        "broker_host": random.choice(ctx.domain_name.values()),
        "broker_port": ctx.broker_port,
        "host": vm_ticket["host"],
        "port": vm_ticket["port"],
        "ticket": vm_ticket["ticket"]
    }

    return return_success(kwargs, dict(data=data), dump=False)
