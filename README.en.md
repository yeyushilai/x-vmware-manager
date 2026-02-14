# VMware Manager

## Project Introduction

VMware Manager is a VMware vSphere platform management tool developed based on the FastAPI framework. It provides complete RESTful API interfaces for managing resources such as datacenters, clusters, folders, and virtual machines.

## Features

- **Datacenter Management**: Get datacenter list and details
- **Cluster Management**: Get cluster list and details for a specific datacenter
- **Folder Management**: Get folder list and details for a specific datacenter
- **Virtual Machine Management**:
  - Get virtual machine list in a cluster
  - Get virtual machine details
  - Virtual machine power operations (power on, power off, reboot, suspend)
- **Health Check**: Service status monitoring
- **API Documentation**: Automatically generated Swagger documentation

## Technology Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **VMware SDK**: pyVmomi
- **Logging**: loguru
- **Dependency Management**: uv
- **Python Version**: 3.11+

## Quick Start

### 1. Environment Preparation

- Python 3.11+
- uv package manager

### 2. Install Dependencies

```bash
# Install uv (if not installed)
pip install uv

# Use uv to install project dependencies
uv sync
```

### 3. Configure Environment Variables

```bash
# VMware vSphere connection configuration
set VMWARE_HOST=your-vcenter-host
set VMWARE_USERNAME=your-username
set VMWARE_PASSWORD=your-password

# Service configuration (optional)
set DEBUG=True
set PORT=8000
```

### 4. Start Service

```bash
python main.py
```

The service will run at `http://localhost:8000`

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Swagger Files**: Automatically generated in the `swagger/` directory when the service starts
  - `swagger/swagger.json` - Swagger documentation in JSON format
  - `swagger/swagger.yaml` - Swagger documentation in YAML format

## API Interface List

### Health Check
- `GET /health` - Service health status check

### Datacenter Management
- `GET /api/v1/dcs` - Get datacenter list
- `GET /api/v1/dcs/{dc_id}` - Get datacenter details

### Cluster Management
- `GET /api/v1/dcs/{dc_id}/clusters` - Get cluster list for a specific datacenter
- `GET /api/v1/dcs/{dc_id}/clusters/{cluster_id}` - Get cluster details

### Folder Management
- `GET /api/v1/dcs/{dc_id}/folders` - Get folder list for a specific datacenter
- `GET /api/v1/dcs/{dc_id}/folders/{folder_id}` - Get folder details

### Virtual Machine Management
- `GET /api/v1/dcs/{dc_id}/clusters/{cluster_id}/vms` - Get virtual machine list in a cluster
- `GET /api/v1/dcs/{dc_id}/vms/{vm_id}` - Get virtual machine details
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/poweron` - Power on virtual machine
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/poweroff` - Power off virtual machine
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/reboot` - Reboot virtual machine
- `POST /api/v1/dcs/{dc_id}/vms/{vm_id}/suspend` - Suspend virtual machine

## Project Structure

```
vmware-manager/
├── app/                      # Application directory
│   ├── core/                 # Core modules
│   │   ├── config.py         # Configuration management
│   │   └── logger.py         # Log management
│   ├── routes/               # API routes
│   │   ├── datacenter.py     # Datacenter routes
│   │   ├── cluster.py        # Cluster routes
│   │   ├── folder.py         # Folder routes
│   │   ├── vm.py             # Virtual machine routes
│   │   └── __init__.py       # Route registration
│   ├── services/             # Service layer
│   │   └── vmware_service.py # VMware service
│   └── __init__.py           # Application initialization
├── vmware/                   # VMware related modules
│   ├── tools/                # VMware tools
│   ├── __init__.py           # VMware class
│   └── interface.py          # VMware interface
├── swagger/                  # Swagger documentation directory
│   ├── swagger.json          # Swagger documentation in JSON format
│   └── swagger.yaml          # Swagger documentation in YAML format
├── main.py                   # Application entry
├── pyproject.toml            # Project configuration
└── README.md                 # Project documentation
```

## Error Handling

All API interfaces return a unified error format:

```json
{
  "code": error code,
  "message": "error message",
  "data": null
}
```

Common error codes:
- `0` - Success
- `500` - Server internal error
- `404` - Resource not found

## Log Management

The project uses loguru for log management. Log files are saved in the `logs/` directory, rotated daily by default, and retained for 7 days.

## Deployment Recommendations

- **Development Environment**: Run `python main.py` directly
- **Production Environment**: Use Nginx reverse proxy with Uvicorn multi-process running

## License

MIT License
