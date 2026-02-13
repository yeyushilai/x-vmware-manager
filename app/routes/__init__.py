#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API路由模块
"""

from fastapi import APIRouter
from app.routes.datacenter import router as datacenter_router
from app.routes.cluster import router as cluster_router
from app.routes.folder import router as folder_router
from app.routes.vm import router as vm_router

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(datacenter_router, prefix="/dcs", tags=["datacenter"])
api_router.include_router(cluster_router, prefix="/dcs", tags=["cluster"])
api_router.include_router(folder_router, prefix="/dcs", tags=["folder"])
api_router.include_router(vm_router, prefix="/dcs", tags=["vm"])
