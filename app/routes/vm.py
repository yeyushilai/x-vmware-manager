#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟机管理API路由
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.core.logger import logger
from app.services.vmware_service import get_vmware_client
from vmware import PlatformVmOperationType

router = APIRouter()


@router.get("/{dc_id}/clusters/{cluster_id}/vms", response_model=Dict[str, Any])
async def list_cluster_vms(dc_id: str, cluster_id: str):
    """获取指定集群的虚拟机列表
    
    Args:
        dc_id: 数据中心ID
        cluster_id: 集群ID
    
    Returns:
        Dict[str, Any]: 虚拟机列表响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        # 查找指定集群
        cluster_name = None
        for c in datacenter.get('cluster_list', []):
            if c.get('moid') == cluster_id:
                cluster_name = c.get('name')
                break
        
        if not cluster_name:
            raise HTTPException(
                status_code=404,
                detail="集群不存在"
            )
        
        vms = client.list_cluster_vm(cluster_name)
        logger.info(f"获取集群虚拟机列表成功，集群: {cluster_name}, 数量: {len(vms)}")
        
        return {
            'code': 0,
            'message': 'success',
            'data': vms
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取集群虚拟机列表失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取集群虚拟机列表失败: {str(e)}'
        )


@router.get("/{dc_id}/vms/{vm_id}", response_model=Dict[str, Any])
async def get_vm(dc_id: str, vm_id: str):
    """获取虚拟机详情
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        Dict[str, Any]: 虚拟机详情响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        vm = client.get_vm(vm_uuid=vm_id)
        if not vm:
            raise HTTPException(
                status_code=404,
                detail="虚拟机不存在"
            )
        
        logger.info(f"获取虚拟机详情成功: {vm_id}")
        
        return {
            'code': 0,
            'message': 'success',
            'data': vm
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取虚拟机详情失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取虚拟机详情失败: {str(e)}'
        )


@router.post("/{dc_id}/vms/{vm_id}/poweron", response_model=Dict[str, Any])
async def poweron_vm(dc_id: str, vm_id: str):
    """启动虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        Dict[str, Any]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.POWERON.value)


@router.post("/{dc_id}/vms/{vm_id}/poweroff", response_model=Dict[str, Any])
async def poweroff_vm(dc_id: str, vm_id: str):
    """关闭虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        Dict[str, Any]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.POWEROFF.value)


@router.post("/{dc_id}/vms/{vm_id}/reboot", response_model=Dict[str, Any])
async def reboot_vm(dc_id: str, vm_id: str):
    """重启虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        Dict[str, Any]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.REBOOT.value)


@router.post("/{dc_id}/vms/{vm_id}/suspend", response_model=Dict[str, Any])
async def suspend_vm(dc_id: str, vm_id: str):
    """挂起虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
    
    Returns:
        Dict[str, Any]: 操作响应
    """
    return await operate_vm(dc_id, vm_id, PlatformVmOperationType.SUSPEND.value)


async def operate_vm(dc_id: str, vm_id: str, operation: str) -> Dict[str, Any]:
    """操作虚拟机
    
    Args:
        dc_id: 数据中心ID
        vm_id: 虚拟机ID
        operation: 操作类型
    
    Returns:
        Dict[str, Any]: 操作响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        # 检查虚拟机是否存在
        vm = client.get_vm(vm_uuid=vm_id)
        if not vm:
            raise HTTPException(
                status_code=404,
                detail="虚拟机不存在"
            )
        
        # 执行操作
        result = client.operate_vm(vm_id, operation)
        logger.info(f"操作虚拟机成功: {vm_id}, 操作: {operation}")
        
        return {
            'code': 0,
            'message': 'success',
            'data': {
                'vm_id': vm_id,
                'operation': operation,
                'result': 'success'
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"操作虚拟机失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'操作虚拟机失败: {str(e)}'
        )
