#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据中心管理API路由
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.core.config import settings
from app.core.logger import logger
from app.services.vmware_service import get_vmware_client
from app.schemas import ApiResponse, DatacenterList, DatacenterInfo

router: APIRouter = APIRouter()


@router.get("", response_model=ApiResponse[DatacenterList])
async def list_datacenters() -> ApiResponse[DatacenterList]:
    """获取数据中心列表
    
    Returns:
        ApiResponse[DatacenterList]: 数据中心列表响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        datacenters: DatacenterList = client.list_datacenter()
        logger.info(f"获取数据中心列表成功，数量: {len(datacenters)}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=datacenters
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取数据中心列表失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取数据中心列表失败: {str(e)}'
        )


@router.get("/{dc_id}", response_model=ApiResponse[DatacenterInfo])
async def get_datacenter(dc_id: str) -> ApiResponse[DatacenterInfo]:
    """获取数据中心详情
    
    Args:
        dc_id: 数据中心ID
    
    Returns:
        ApiResponse[DatacenterInfo]: 数据中心详情响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        datacenter: DatacenterInfo = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        logger.info(f"获取数据中心详情成功: {dc_id}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=datacenter
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取数据中心详情失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取数据中心详情失败: {str(e)}'
        )
