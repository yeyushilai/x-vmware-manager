# VMware Manager

## 项目简介

VMware Manager 是一个 VMware vSphere 平台纳管工具，工具提供了一系列 API 接口，用于获取虚拟机列表、查询详细信息、监控虚拟机状态、执行虚拟机操作、更新虚拟机信息以及获取虚拟机票据等功能。

## 功能特性

- **虚拟机管理**：获取虚拟机列表、查询详细信息、更新虚拟机配置
- **虚拟机操作**：开机、关机、重启等操作
- **虚拟机监控**：获取虚拟机性能指标
- **平台管理**：连接和管理 VMware vSphere 平台
- **票据管理**：获取虚拟机远程控制台票据

## 系统架构

- **Web服务层**：基于 Flask 和 Connexion 的 RESTful API 服务
- **业务逻辑层**：处理具体的业务逻辑，如虚拟机操作、监控等
- **平台对接层**：与 VMware vSphere 平台进行交互
- **数据存储层**：存储平台配置信息

## 目录结构

```
vmware-manager/
├── handlers/            # 处理程序目录
│   ├── controllers/     # 控制器，处理 HTTP 请求
│   ├── impl/            # 实现类，处理业务逻辑
│   └── api_acl/         # API 访问控制
├── platforms/           # 平台对接目录
│   ├── iaas/            # IaaS相关功能
│   └── vmware_vsphere/  # VMware vSphere 平台对接
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
- uv 管理工具
- VMware vSphere API SDK

### 安装 uv 管理工具

```bash
# 使用 pip 安装 uv
pip install uv

# 或者使用官方推荐的安装方式
# curl -Ls https://astral.sh/uv/install.sh | sh
```

### 初始化项目

1. **克隆项目仓库**
   ```bash
   git clone <repository-url>
   cd vmware-manager
   ```

2. **初始化虚拟环境**
   ```bash
   # 创建 .venv 虚拟环境目录
   uv venv
   ```

3. **安装依赖**
   ```bash
   # 使用 uv 安装依赖并生成 uv.lock 文件
   uv pip install -e .
   ```

4. **验证安装**
   ```bash
   # 查看已安装的依赖
   uv pip list
   ```

### 项目配置文件

在`/etc/pitrix`目录下创建`vmware_manager_server.yaml`配置文件，配置数据库连接、Zookeeper连接等信息。

### 启动服务

```bash
# 使用 uv run 启动服务
uv run python vmware_manager_server.py
```

服务将在`http://localhost:8888`启动。

### 依赖管理

#### 添加新依赖
```bash
# 添加新依赖并更新 uv.lock 文件
uv pip install <package-name>
```

#### 移除依赖
```bash
# 移除依赖并更新 uv.lock 文件
uv pip uninstall <package-name>
```

#### 从 uv.lock 文件安装依赖
```bash
# 确保虚拟环境存在
uv venv

# 从 uv.lock 文件安装依赖
uv pip sync
```

### 项目文件说明

- **pyproject.toml**：项目配置文件，包含项目依赖和 uv 配置
- **uv.lock**：依赖版本锁定文件，确保依赖版本的一致性
- **.venv/**：虚拟环境目录，包含项目依赖
- **.python-version**：指定项目使用的 Python 版本

### 开发流程

1. **创建分支**
   ```bash
   git checkout -b feature/<feature-name>
   ```

2. **开发功能**
   - 实现新功能
   - 编写代码

3. **安装依赖**（如果添加了新依赖）
   ```bash
   uv pip install <package-name>
   ```

4. **运行服务**
   ```bash
   uv run python vmware_manager_server.py
   ```

5. **提交代码**
   ```bash
   git add .
   git commit -m "Add <feature-name>"
   git push origin feature/<feature-name>
   ```

6. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 等待代码审查
   - 合并代码到主分支

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

## 注意事项

1. 使用前请确保已正确配置 VMware vSphere 平台连接信息
2. 部分操作（如重启、关机）需要虚拟机安装并运行 VMware Tools
3. 获取虚拟机票据时，虚拟机必须处于开机状态

## 许可证

本项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请联系项目维护人员。

## 提交 Issue

如果您在使用过程中遇到问题，或有新的功能建议，欢迎在 GitHub 上提交 Issue：

1. 访问项目的 GitHub 仓库页面
2. 点击 "Issues" 选项卡
3. 点击 "New issue" 按钮
4. 选择适当的 issue 模板（如果有）
5. 填写 issue 标题和详细描述
6. 点击 "Submit new issue" 按钮提交

### Issue 提交建议

- **问题报告**：
  - 描述您遇到的具体问题
  - 提供重现步骤
  - 说明您期望的行为
  - 附上相关的错误信息或日志
  - 注明您的环境信息（Python 版本、操作系统等）

- **功能请求**：
  - 描述您希望添加的功能
  - 说明为什么这个功能是有用的
  - 如有可能，提供功能实现的建议

我们会定期查看并处理提交的 Issue，感谢您对项目的贡献！
