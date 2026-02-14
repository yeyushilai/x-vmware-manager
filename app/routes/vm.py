#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟机管理API路由
"""

from fastapi import APIRouter, HTTPException
from typing import Any, Optional

from app.core.logger import logger
from app.services.vmware_service import get_vmware_client
from vmware import PlatformVmOperationType
from app.schemas import ApiResponse, VmList, VmInfo

router: APIRouter = APIRouter()


@router.get("/{dc_id}/clusters/{cluster_id}/vms", response_model=ApiResponse[VmList])
async def list_cluster_vms(dc_id: str, cluster_id: str) -> ApiResponse[VmList]:
    """获取指定集群的虚拟机列表
    
    Args:
        dc_id: 数据中心ID
        cluster_id: 集群ID
    
    Returns:
        ApiResponse[VmList]: 虚拟机列表响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter: dict[str, Any] = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        # 查找指定集群
        cluster_name: Optional[str] = None
        for c in datacenter.get('cluster_list', []):
            if c.get('moid') == cluster_id:
                cluster_name = c.get('name')
                break
        
        if not cluster_name:
            raise HTTPException(
                status_code=404,
                detail="集群不存在"
            )
        
        vms: VmList = client.list_cluster_vm(cluster_name)
        logger.info(f"获取集群虚拟机列表成功，集群: {cluster_name}, 数量: {len(vms)}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=vms
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取集群虚拟机列表失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取集群虚拟机列表失败: {str(e)}'
        )


@router.get("/{dc_id}/vms/{vm_id}", response_model=ApiResponse[VmInfo])
async def get_vm(dc_id: str, vm_id: str) -> ApiResponse[VmInfo]:
    """获取虚拟机详情
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        ApiResponse[VmInfo]: 虚拟机详情响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter: dict[str, Any] = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        vm: Optional[VmInfo] = client.get_vm(vm_uuid=vm_id)
        if not vm:
            raise HTTPException(
                status_code=404,
                detail="虚拟机不存在"
            )
        
        logger.info(f"获取虚拟机详情成功: {vm_id}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=vm
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取虚拟机详情失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取虚拟机详情失败: {str(e)}'
        )


@router.post("/{dc_id}/vms/{vm_id}/poweron", response_model=ApiResponse[dict[str, str]])
async def poweron_vm(dc_id: str, vm_id: str) -> ApiResponse[dict[str, str]]:
    """启动虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        ApiResponse[dict[str, str]]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.POWERON.value)


@router.post("/{dc_id}/vms/{vm_id}/poweroff", response_model=ApiResponse[dict[str, str]])
async def poweroff_vm(dc_id: str, vm_id: str) -> ApiResponse[dict[str, str]]:
    """关闭虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        ApiResponse[dict[str, str]]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.POWEROFF.value)


@router.post("/{dc_id}/vms/{vm_id}/reboot", response_model=ApiResponse[dict[str, str]])
async def reboot_vm(dc_id: str, vm_id: str) -> ApiResponse[dict[str, str]]:
    """重启虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        ApiResponse[dict[str, str]]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.REBOOT.value)


@router.post("/{dc_id}/vms/{vm_id}/suspend", response_model=ApiResponse[dict[str, str]])
async def suspend_vm(dc_id: str, vm_id: str) -> ApiResponse[dict[str, str]]:
    """挂起虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        ApiResponse[dict[str, str]]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.SUSPEND.value)


async def operate_vm(dc_id: str, vm_id: str, operation: str) -> ApiResponse[dict[str, str]]:
    """操作虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
        operation: 操作类型
    
    Returns:
        ApiResponse[dict[str, str]]: 操作响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter: dict[str, Any] = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        # 检查虚拟机是否存在
        vm: Optional[VmInfo] = client.get_vm(vm_uuid=vm_id)
        if not vm:
            raise HTTPException(
                status_code=404,
                detail="虚拟机不存在"
            )
        
        # 执行操作
        result: Any = client.operate_vm(vm_id, operation)
        logger.info(f"操作虚拟机成功: {vm_id}, 操作: {operation}")
        
        return ApiResponse(
            code=0,
            message='success',
            data={
                'vm_id': vm_id,
                'operation': operation,
                'result': 'success'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"操作虚拟机失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'操作虚拟机失败: {str(e)}'
        )
