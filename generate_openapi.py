#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成OpenAPI文档（swagger）文件
"""

import os
import sys
import json
import yaml

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app


def generate_openapi_spec():
    """生成OpenAPI规范文件
    
    Returns:
        None
    """
    # 获取OpenAPI规范
    openapi_spec = app.openapi()
    
    # 确保输出目录存在
    output_dir = 'openapi'
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成JSON文件
    json_path = os.path.join(output_dir, 'openapi.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(openapi_spec, f, indent=2, ensure_ascii=False)
    print(f"✓ OpenAPI JSON文件生成成功: {json_path}")
    
    # 生成YAML文件
    yaml_path = os.path.join(output_dir, 'openapi.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(openapi_spec, f, default_flow_style=False, allow_unicode=True)
    print(f"✓ OpenAPI YAML文件生成成功: {yaml_path}")
    
    # 显示在线文档地址
    print("\n在线文档访问地址:")
    print("- Swagger UI: http://localhost:8000/docs")
    print("- ReDoc: http://localhost:8000/redoc")


if __name__ == "__main__":
    generate_openapi_spec()
