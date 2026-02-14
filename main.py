#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VMware Manager API服务主入口
使用FastAPI框架实现的VMware vSphere管理工具
"""

import os
import sys
import json
import yaml
from typing import Any, AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.routes import api_router
from app.core.config import settings
from app.core.logger import logger


def generate_swagger_spec(app_instance: FastAPI) -> None:
    """生成Swagger规范文件
    
    Args:
        app_instance: FastAPI应用实例
    
    Returns:
        None
    """
    try:
        # 获取OpenAPI规范
        openapi_spec: dict[str, Any] = app_instance.openapi()
        
        # 确保输出目录存在
        output_dir: str = 'swagger'
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成JSON文件
        json_path: str = os.path.join(output_dir, 'swagger.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(openapi_spec, f, indent=2, ensure_ascii=False)
        logger.info(f"✓ Swagger JSON文件生成成功: {json_path}")
        
        # 生成YAML文件
        yaml_path: str = os.path.join(output_dir, 'swagger.yaml')
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(openapi_spec, f, default_flow_style=False, allow_unicode=True)
        logger.info(f"✓ Swagger YAML文件生成成功: {yaml_path}")
    except Exception as e:
        logger.error(f"生成Swagger文件失败: {e}")


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncIterator[None]:
    """应用生命周期管理
    
    Args:
        app_instance: FastAPI应用实例
    
    Yields:
        None
    """
    # 启动事件
    logger.info("启动VMware Manager API服务")
    logger.info(f"服务运行在: http://localhost:{settings.PORT}")
    logger.info(f"API文档: http://localhost:{settings.PORT}/docs")
    
    # 生成Swagger文件
    generate_swagger_spec(app_instance)
    
    yield
    
    # 关闭事件
    logger.info("关闭VMware Manager API服务")


# 创建FastAPI应用实例
app: FastAPI = FastAPI(
    title="VMware Manager API",
    description="VMware vSphere平台管理工具API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
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


@app.get("/health")
async def health_check() -> dict[str, str]:
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
