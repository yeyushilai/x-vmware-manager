# VMware Manager

## 项目简介

VMware Manager是一个基于FastAPI框架开发的VMware vSphere平台管理工具，提供了完整的RESTful API接口，用于管理数据中心、集群、文件夹和虚拟机等资源。

## 功能特性

- **数据中心管理**：获取数据中心列表和详情
- **集群管理**：获取指定数据中心的集群列表和详情
- **文件夹管理**：获取指定数据中心的文件夹列表和详情
- **虚拟机管理**：
  - 获取集群中的虚拟机列表
  - 获取虚拟机详情
  - 虚拟机电源操作（开机、关机、重启、挂起）
- **健康检查**：服务状态监控
- **API文档**：自动生成的Swagger文档

## 技术栈

- **框架**：FastAPI
- **服务器**：Uvicorn
- **VMware SDK**：pyVmomi
- **日志**：loguru
- **依赖管理**：uv
- **Python版本**：3.11+

## 快速开始

### 1. 环境准备

- Python 3.11+
- uv 包管理器

### 2. 安装依赖

```bash
# 安装uv（如果未安装）
pip install uv

# 使用uv安装项目依赖
uv sync
```

### 3. 配置环境变量

```bash
# VMware vSphere连接配置
set VMWARE_HOST=your-vcenter-host
set VMWARE_USERNAME=your-username
set VMWARE_PASSWORD=your-password

# 服务配置（可选）
set DEBUG=True
set PORT=8000
```

### 4. 启动服务

```bash
python main.py
```

服务将运行在 `http://0.0.0.0:8000`

## API文档

- **Swagger UI**：`http://localhost:8000/docs`
- **ReDoc**：`http://localhost:8000/redoc`

## API接口列表

### 健康检查
- `GET /health` - 服务健康状态检查

### 数据中心管理
- `GET /api/v1/dcs` - 获取数据中心列表
- `GET /api/v1/dcs/{dc_id}` - 获取数据中心详情

### 集群管理
- `GET /api/v1/dcs/{dc_id}/clusters` - 获取指定数据中心的集群列表
- `GET /api/v1/dcs/{dc_id}/clusters/{cluster_id}` - 获取集群详情

### 文件夹管理
- `GET /api/v1/dcs/{dc_id}/folders` - 获取指定数据中心的文件夹列表
- `GET /api/v1/dcs/{dc_id}/folders/{folder_id}` - 获取文件夹详情

### 虚拟机管理
- `GET /api/v1/dcs/{dc_id}/clusters/{cluster_id}/vms` - 获取指定集群的虚拟机列表
- `GET /api/v1/dcs/{dc_id}/vms/{vm_id}` - 获取虚拟机详情
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/poweron` - 启动虚拟机
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/poweroff` - 关闭虚拟机
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/reboot` - 重启虚拟机
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/suspend` - 挂起虚拟机

## 项目结构

```
vmware-manager/
├── app/                      # 应用目录
│   ├── core/                 # 核心模块
│   │   ├── config.py         # 配置管理
│   │   └── logger.py         # 日志管理
│   ├── routes/               # API路由
│   │   ├── datacenter.py     # 数据中心路由
│   │   ├── cluster.py        # 集群路由
│   │   ├── folder.py         # 文件夹路由
│   │   ├── vm.py             # 虚拟机路由
│   │   └── __init__.py       # 路由注册
│   ├── services/             # 服务层
│   │   └── vmware_service.py # VMware服务
│   └── __init__.py           # 应用初始化
├── vmware/                   # VMware相关模块
│   ├── tools/                # VMware工具
│   ├── __init__.py           # VMware类
│   └── interface.py          # VMware接口
├── main.py                   # 应用入口
├── pyproject.toml            # 项目配置
└── README.md                 # 项目文档
```

## 错误处理

所有API接口返回统一的错误格式：

```json
{
  "code": 错误码,
  "message": "错误信息",
  "data": null
}
```

常见错误码：
- `0` - 成功
- `500` - 服务器内部错误
- `404` - 资源不存在

## 日志管理

项目使用loguru进行日志管理，日志文件保存在 `log/` 目录下，默认按天轮转，保留7天。


## 许可证

MIT License
