#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VMware vSphere类
"""

from typing import Any, Optional
from .interface import VMwareVSphereInterface, PlatformVmOperationType
from app.core.logger import logger


class VMwareVSphere:
    """VMware vSphere类
    
    用于管理VMware vSphere平台的连接和操作
    """

    def __init__(self, account: dict[str, str]) -> None:
        """初始化VMwareVSphere实例
        
        Args:
            account: VMware连接配置字典
        """
        self.account: dict[str, str] = account
        self.vi: VMwareVSphereInterface = VMwareVSphereInterface(account)

    def is_connected(self) -> bool:
        """检查和VMware vSphere平台的连通性
        
        Returns:
            bool: 联通返回True，不连通返回False
        """
        try:
            return self.vi.check_connected()
        except Exception as e:
            logger.error(f"检查VMware连接失败: {e}")
            return False

    def detail_root_folder(self) -> list[dict[str, Any]]:
        """获取根文件夹详情
        
        Returns:
            list[dict[str, Any]]: 根文件夹下的子实体列表
        """
        try:
            root_folder = self.vi.root_folder
            return self._loop_child_entity(root_folder)
        except Exception as e:
            logger.error(f"获取根文件夹详情失败: {e}")
            return []

    def detail_folder(self, folder_moid: str, datacenter_moid: str) -> list[dict[str, Any]]:
        """获取指定文件夹详情
        
        Args:
            folder_moid: 文件夹MOID
            datacenter_moid: 数据中心MOID
        
        Returns:
            list[dict[str, Any]]: 文件夹下的子实体列表
        """
        try:
            folder_obj = self.vi.get_folder(folder_moid, datacenter_moid)
            if not folder_obj:
                return []
            return self._loop_child_entity(folder_obj, datacenter_moid)
        except Exception as e:
            logger.error(f"获取文件夹详情失败: {e}")
            return []

    def _loop_child_entity(self, folder_obj: Any, datacenter_moid: Optional[str] = None) -> list[dict[str, Any]]:
        """递归遍历子实体
        
        Args:
            folder_obj: 文件夹对象
            datacenter_moid: 数据中心MOID
        
        Returns:
            list[dict[str, Any]]: 子实体列表
        """
        data: list[dict[str, Any]] = []
        try:
            for mo_obj in folder_obj.childEntity:
                mo_dict: dict[str, Any] = {
                    "name": mo_obj.name,
                    "moid": mo_obj._moId,
                    "datacenter_id": datacenter_moid
                }
                
                # 根据对象类型添加额外信息
                from pyVmomi import vim
                if isinstance(mo_obj, vim.VirtualMachine):
                    mo_dict["type"] = "vm"
                    mo_dict["uuid"] = mo_obj.summary.config.uuid
                elif isinstance(mo_obj, vim.Datacenter):
                    mo_dict["type"] = "datacenter"
                    mo_dict["vm_folder_moid"] = mo_obj.vmFolder._moId
                    mo_dict["vm_folder_name"] = mo_obj.vmFolder.name
                elif isinstance(mo_obj, vim.Folder):
                    mo_dict["type"] = "folder"
                    mo_dict["has_child"] = bool(mo_obj.childEntity)
                elif isinstance(mo_obj, vim.ClusterComputeResource):
                    mo_dict["type"] = "cluster"
                
                data.append(mo_dict)
        except Exception as e:
            logger.error(f"遍历子实体失败: {e}")
        return data

    def list_datacenter(self) -> list[dict[str, Any]]:
        """获取数据中心列表
        
        Returns:
            list[dict[str, Any]]: 数据中心列表
        """
        try:
            dc_list: list[dict[str, Any]] = []
            for dc_obj in self.vi.datacenters:
                dc_info: dict[str, Any] = self._layout_datacenter(dc_obj=dc_obj)
                dc_list.append(dc_info)
            return dc_list
        except Exception as e:
            logger.error(f"获取数据中心列表失败: {e}")
            return []

    def detail_datacenter(self, dc_moid: str) -> dict[str, Any]:
        """获取数据中心详情
        
        Args:
            dc_moid: 数据中心MOID
        
        Returns:
            dict[str, Any]: 数据中心详情
        """
        try:
            return self._layout_datacenter(dc_moid=dc_moid)
        except Exception as e:
            logger.error(f"获取数据中心详情失败: {e}")
            return {}

    def _layout_datacenter(self, dc_moid: Optional[str] = None, dc_obj: Optional[Any] = None) -> dict[str, Any]:
        """构建数据中心信息
        
        Args:
            dc_moid: 数据中心MOID
            dc_obj: 数据中心对象
        
        Returns:
            dict[str, Any]: 数据中心信息
        """
        assert dc_moid or dc_obj
        
        if not dc_obj:
            dc_obj = self.vi.get_datacenter_by_moid(dc_moid)
            if not dc_obj:
                return {}

        dc_info: dict[str, Any] = {
            "name": dc_obj.name,
            "moid": dc_obj._moId,
            "vm_folder_name": dc_obj.vmFolder.name,
            "vm_folder_moid": dc_obj.vmFolder._moId,
            "host_folder_name": dc_obj.hostFolder.name,
            "host_folder_moid": dc_obj.hostFolder._moId,
            "cluster_list": []
        }

        try:
            from pyVmomi import vim
            for child in dc_obj.hostFolder.childEntity:
                if isinstance(child, vim.ClusterComputeResource):
                    cluster_dict: dict[str, Any] = {
                        "name": child.name,
                        "moid": child._moId,
                        "host_list": []
                    }
                    
                    for host in child.host:
                        host_dict: dict[str, str] = {
                            "name": host.name,
                            "moid": host._moId
                        }
                        cluster_dict["host_list"].append(host_dict)
                    
                    dc_info["cluster_list"].append(cluster_dict)
        except Exception as e:
            logger.error(f"构建数据中心信息失败: {e}")

        return dc_info

    def list_cluster(self, cluster_name: Optional[str] = None) -> list[dict[str, str]]:
        """获取集群列表
        
        Args:
            cluster_name: 集群名称
        
        Returns:
            list[dict[str, str]]: 集群列表
        """
        try:
            result: list[dict[str, str]] = []
            
            from pyVmomi import vim
            if cluster_name:
                cluster = self.vi.get_cluster_by_name(cluster_name)
                if cluster:
                    result.append({"name": cluster.name, "moid": cluster._moId})
            else:
                for cluster in self.vi.clusters:
                    result.append({"name": cluster.name, "moid": cluster._moId})
            
            return result
        except Exception as e:
            logger.error(f"获取集群列表失败: {e}")
            return []

    def list_cluster_vm(self, cluster_name: str) -> list[dict[str, Any]]:
        """获取集群中的虚拟机列表
        
        Args:
            cluster_name: 集群名称
        
        Returns:
            list[dict[str, Any]]: 虚拟机列表
        """
        try:
            vms_data: list[dict[str, Any]] = []
            for vm_data in self.vi.get_cluster_vms(cluster_name):
                try:
                    vm_info: Optional[dict[str, Any]] = self.vi.layout_dict_vm_data(vm_data)
                    if vm_info:
                        vms_data.append(vm_info)
                except Exception as e:
                    uuid: str = vm_data.get("summary.config.uuid", "unknown")
                    logger.error(f"处理虚拟机数据失败, uuid: {uuid}, 原因: {e}")
                    continue
            return vms_data
        except Exception as e:
            logger.error(f"获取集群虚拟机列表失败: {e}")
            return []

    def list_vm(self, vm_properties: Optional[list[str]] = None) -> list[dict[str, Any]]:
        """获取所有虚拟机列表
        
        Args:
            vm_properties: 虚拟机属性列表
        
        Returns:
            list[dict[str, Any]]: 虚拟机列表
        """
        try:
            vms_list: list[dict[str, Any]] = []
            for vm_data in self.vi.get_vms_properties(vm_properties):
                try:
                    vm_info: Optional[dict[str, Any]] = self.vi.layout_dict_vm_data(vm_data)
                    if vm_info:
                        vms_list.append(vm_info)
                except Exception as e:
                    uuid: str = vm_data.get("summary.config.uuid", "unknown")
                    logger.error(f"处理虚拟机数据失败, uuid: {uuid}, 原因: {e}")
                    continue
            return vms_list
        except Exception as e:
            logger.error(f"获取虚拟机列表失败: {e}")
            return []

    def get_vm(self, vm_name: Optional[str] = None, vm_uuid: Optional[str] = None) -> Optional[dict[str, Any]]:
        """获取虚拟机详情
        
        Args:
            vm_name: 虚拟机名称
            vm_uuid: 虚拟机UUID
        
        Returns:
            Optional[dict[str, Any]]: 虚拟机详情
        """
        try:
            if vm_name:
                vm_obj = self.vi.get_vm_by_name(vm_name)
            else:
                vm_obj = self.vi.get_vm_by_uuid(vm_uuid)

            if not vm_obj:
                return None

            return self.vi.layout_obj_vm_data(vm_obj)
        except Exception as e:
            logger.error(f"获取虚拟机详情失败: {e}")
            return None

    def get_vm_ticket(self, vm_uuid: str) -> Optional[dict[str, Any]]:
        """获取虚拟机票据
        
        Args:
            vm_uuid: 虚拟机UUID
        
        Returns:
            Optional[dict[str, Any]]: 虚拟机票据
        """
        try:
            vm_ticket_obj = self.vi.get_vm_ticket_by_uuid(vm_uuid)
            return {
                "host": vm_ticket_obj.host,
                "port": vm_ticket_obj.port,
                "ticket": vm_ticket_obj.ticket,
            }
        except Exception as e:
            logger.error(f"获取虚拟机票据失败: {e}")
            return None

    def get_vm_power_status(self, vm_uuid: str) -> Optional[str]:
        """获取虚拟机电源状态
        
        Args:
            vm_uuid: 虚拟机UUID
        
        Returns:
            Optional[str]: 虚拟机电源状态
        """
        try:
            vm_obj = self.vi.get_vm_by_uuid(vm_uuid)
            if vm_obj:
                return vm_obj.summary.runtime.powerState
            return None
        except Exception as e:
            logger.error(f"获取虚拟机电源状态失败: {e}")
            return None

    def update_vm(self, vm_uuid: str, vm_info: dict[str, Any]) -> Optional[Any]:
        """更新虚拟机信息
        
        Args:
            vm_uuid: 虚拟机UUID
            vm_info: 虚拟机信息
        
        Returns:
            Optional[Any]: 更新结果
        """
        try:
            return self.vi.update_vm_by_uuid(vm_uuid, vm_info)
        except Exception as e:
            logger.error(f"更新虚拟机信息失败: {e}")
            return None

    def operate_vm(self, vm_uuid: str, operation: str) -> Optional[Any]:
        """操作虚拟机
        
        Args:
            vm_uuid: 虚拟机UUID
            operation: 操作类型
        
        Returns:
            Optional[Any]: 操作结果
        """
        try:
            return self.vi.operate_vm_by_uuid(vm_uuid, operation)
        except Exception as e:
            logger.error(f"操作虚拟机失败: {e}")
            return None

    def list_folders(self, datacenter_moid: Optional[str] = None) -> list[dict[str, Any]]:
        """获取文件夹列表
        
        Args:
            datacenter_moid: 数据中心MOID
        
        Returns:
            list[dict[str, Any]]: 文件夹列表
        """
        try:
            folders: list[dict[str, Any]] = []
            for folder_obj in self.vi.folders:
                folder_info: dict[str, Any] = {
                    "name": folder_obj.name,
                    "moid": folder_obj._moId,
                    "has_child": bool(folder_obj.childEntity)
                }
                folders.append(folder_info)
            return folders
        except Exception as e:
            logger.error(f"获取文件夹列表失败: {e}")
            return []
