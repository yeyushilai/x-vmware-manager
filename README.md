# VMware Manager

## 项目简介

VMware Manager 是一个 VMware vSphere 平台纳管工具，工具提供了一系列 API 接口，用于获取虚拟机列表、查询详细信息、监控虚拟机状态、执行虚拟机操作、更新虚拟机信息以及获取虚拟机票据等功能。

## 功能特性

- **虚拟机管理**：获取虚拟机列表、查询详细信息、更新虚拟机配置
- **虚拟机操作**：开机、关机、重启等操作
- **虚拟机监控**：获取虚拟机性能指标
- **平台管理**：连接和管理VMware vSphere平台
- **票据管理**：获取虚拟机远程控制台票据

## 系统架构

- **Web服务层**：基于 Flask 和 Connexion 的 RESTful API 服务
- **业务逻辑层**：处理具体的业务逻辑，如虚拟机操作、监控等
- **平台对接层**：与VMware vSphere平台进行交互
- **数据存储层**：存储平台配置信息

## 目录结构

```
vmware-manager/
├── handlers/            # 处理程序目录
│   ├── controllers/     # 控制器，处理HTTP请求
│   ├── impl/            # 实现类，处理业务逻辑
│   └── api_acl/         # API访问控制
├── platforms/           # 平台对接目录（原platforms）
│   ├── iaas/            # IaaS相关功能
│   └── vmware_vsphere/  # VMware vSphere平台对接
├── common/              # 通用工具类
├── connexion/           # API框架
├── utils/               # 工具类
│   ├── common/          # 通用工具函数
│   └── db/              # 数据库相关工具
├── vmware_manager_server.py  # 主服务器文件
└── README.md            # 项目文档
```

## 快速开始

### 环境要求

- Python 3.6+
- VMware vSphere API SDK
- Flask
- Connexion

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置文件

在`/etc/pitrix`目录下创建`vmware_manager_server.yaml`配置文件，配置数据库连接、Zookeeper连接等信息。

### 启动服务

```bash
python vmware_manager_server.py
```

服务将在`http://localhost:8888`启动。

## API文档

### 虚拟机相关API

- **GET /api/v1/vm/describe**：获取虚拟机列表
- **GET /api/v1/vm/detail**：获取虚拟机详细信息
- **GET /api/v1/vm/monitor**：获取虚拟机监控数据
- **POST /api/v1/vm/operate**：执行虚拟机操作
- **POST /api/v1/vm/update**：更新虚拟机信息
- **GET /api/v1/vm/ticket**：获取虚拟机控制台票据

### 请求参数说明

大部分API需要以下参数：
- `platform_id`：平台ID
- `vm_id`：虚拟机ID（部分API需要）
- 其他参数根据具体API而定

## 开发指南

### 代码结构

- **handlers/controllers/**：控制器文件，处理HTTP请求，调用实现类
- **handlers/impl/**：实现类文件，包含具体的业务逻辑
- **platforms/vmware_vsphere/**：VMware vSphere 平台对接实现

### 新增功能

1. 在`handlers/controllers/`目录下创建或修改控制器文件
2. 在`handlers/impl/`目录下实现具体的业务逻辑
3. 在`platforms/vmware_vsphere/`目录下添加平台对接代码
4. 更新API文档

### 日志管理

项目使用Python标准日志模块，日志级别可在配置文件中设置。推荐使用以下日志级别：
- **DEBUG**：详细的调试信息
- **INFO**：重要的信息
- **ERROR**：错误信息
- **EXCEPTION**：异常信息

## 注意事项

1. 本项目已移除权限校验和身份验证代码，仅保留核心功能
2. 使用前请确保已正确配置 VMware vSphere 平台连接信息
3. 部分操作（如重启、关机）需要虚拟机安装并运行 VMware Tools
4. 获取虚拟机票据时，虚拟机必须处于开机状态

## 许可证

本项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请联系项目维护人员。