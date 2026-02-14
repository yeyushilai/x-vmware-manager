#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件夹管理API路由
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.core.logger import logger
from app.services.vmware_service import get_vmware_client
from app.schemas import ApiResponse, FolderList, FolderInfo

router: APIRouter = APIRouter()


@router.get("/{dc_id}/folders", response_model=ApiResponse[FolderList])
async def list_folders(dc_id: str) -> ApiResponse[FolderList]:
    """获取指定数据中心的文件夹列表
    
    Args:
        dc_id: 数据中心ID
    
    Returns:
        ApiResponse[FolderList]: 文件夹列表响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter: Dict[str, Any] = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        folders: FolderList = client.list_folders(dc_id)
        logger.info(f"获取文件夹列表成功，数据中心: {dc_id}, 数量: {len(folders)}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=folders
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取文件夹列表失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取文件夹列表失败: {str(e)}'
        )


@router.get("/{dc_id}/folders/{folder_id}", response_model=ApiResponse[FolderInfo])
async def get_folder(dc_id: str, folder_id: str) -> ApiResponse[FolderInfo]:
    """获取文件夹详情
    
    Args:
        dc_id: 数据中心ID
        folder_id: 文件夹ID
    
    Returns:
        ApiResponse[FolderInfo]: 文件夹详情响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情，确认存在
        datacenter: Dict[str, Any] = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        folder_detail: FolderInfo = client.detail_folder(folder_id, dc_id)
        logger.info(f"获取文件夹详情成功: {folder_id}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=folder_detail
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取文件夹详情失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取文件夹详情失败: {str(e)}'
        )
