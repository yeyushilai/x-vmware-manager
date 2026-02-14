#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集群管理API路由
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from app.core.logger import logger
from app.services.vmware_service import get_vmware_client
from app.schemas import ApiResponse, ClusterList, ClusterInfo

router: APIRouter = APIRouter()


@router.get("/{dc_id}/clusters", response_model=ApiResponse[ClusterList])
async def list_clusters(dc_id: str) -> ApiResponse[ClusterList]:
    """获取指定数据中心的集群列表
    
    Args:
        dc_id: 数据中心ID
    
    Returns:
        ApiResponse[ClusterList]: 集群列表响应
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
        
        clusters: ClusterList = datacenter.get('cluster_list', [])
        logger.info(f"获取数据中心集群列表成功，数据中心: {dc_id}, 集群数量: {len(clusters)}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=clusters
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取集群列表失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取集群列表失败: {str(e)}'
        )


@router.get("/{dc_id}/clusters/{cluster_id}", response_model=ApiResponse[ClusterInfo])
async def get_cluster(dc_id: str, cluster_id: str) -> ApiResponse[ClusterInfo]:
    """获取集群详情
    
    Args:
        dc_id: 数据中心ID
        cluster_id: 集群ID
    
    Returns:
        ApiResponse[ClusterInfo]: 集群详情响应
    """
    try:
        client = get_vmware_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="VMware客户端未初始化"
            )
        
        # 先获取数据中心详情
        datacenter: dict[str, Any] = client.detail_datacenter(dc_id)
        if not datacenter:
            raise HTTPException(
                status_code=404,
                detail="数据中心不存在"
            )
        
        # 查找指定集群
        cluster: Optional[ClusterInfo] = None
        for c in datacenter.get('cluster_list', []):
            if c.get('moid') == cluster_id:
                cluster = c
                break
        
        if not cluster:
            raise HTTPException(
                status_code=404,
                detail="集群不存在"
            )
        
        logger.info(f"获取集群详情成功: {cluster_id}")
        
        return ApiResponse(
            code=0,
            message='success',
            data=cluster
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取集群详情失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f'获取集群详情失败: {str(e)}'
        )
