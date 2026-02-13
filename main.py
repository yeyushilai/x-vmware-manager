#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VMware Manager API服务主入口
使用FastAPI框架实现的VMware vSphere管理工具
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.routes import api_router
from app.core.config import settings
from app.core.logger import logger

# 创建FastAPI应用实例
app = FastAPI(
    title="VMware Manager API",
    description="VMware vSphere平台管理工具API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("启动VMware Manager API服务")
    logger.info(f"服务运行在: http://0.0.0.0:{settings.PORT}")
    logger.info(f"API文档: http://0.0.0.0:{settings.PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("关闭VMware Manager API服务")


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "message": "VMware Manager API is running",
        "version": "0.1.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )
