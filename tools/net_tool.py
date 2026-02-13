#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import re
import socket
import subprocess
import netaddr
import struct

from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp


class NetTool:

    @classmethod
    def is_valid_ip(cls, ip_addr):
        """ 检查IP地址是否合法 """
        try:
            netaddr.IPAddress(ip_addr, flags=1)
        except Exception:
            return False
        return True

    @classmethod
    def is_valid_mac(cls, mac_addr):
        """ 检查MAC地址是否合法 """
        try:
            if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_addr.lower()):
                return True
        except Exception:
            return False
        return False

    @classmethod
    def is_ip_reachable(cls, ip, retries=5):
        """ 检查IP地址是否通达"""
        retries = retries
        while retries > 0:
            ret = cls.normal_exec("ping -c 1 -w 1 %s" % ip)
            if ret is not None and ret[0] == 0:
                return True
            retries -= 1

        return False

    @classmethod
    def is_ip_port_reachable(cls, ip, port):
        """ 检查IP地址和端口号是否通达"""
        if not os.path.exists("/bin/nc"):
            return False
        ret = cls.normal_exec("/bin/nc -z -w 1 %s %s" % (ip, port))
        if ret is not None and ret[0] == 0:
            return True
        return False

    @classmethod
    def is_ip_network(cls, network):
        n = network
        if not isinstance(n, (netaddr.IPNetwork, netaddr.IPAddress)):
            n = cls.get_ip_network(network)

        return getattr(n, "version", None) == 4

    @classmethod
    def is_ipv6_network(cls, network):
        n = network
        if not isinstance(n, (netaddr.IPNetwork, netaddr.IPAddress)):
            n = cls.get_ip_network(network)

        return getattr(n, "version", None) == 6

    @classmethod
    def get_hostname(cls):
        """获取主机名称"""
        return socket.gethostname()

    @classmethod
    def get_ip_address(cls):
        host_name = cls.get_hostname()
        return socket.gethostbyname(host_name)

    @classmethod
    def get_hostname_by_ip(cls, ip):
        """ 根据IP地址获取主机名称 """
        try:
            socket.setdefaulttimeout(3)
            names = socket.gethostbyaddr(ip)
            for _name in names:
                name = None
                if isinstance(_name, str):
                    name = _name
                elif isinstance(_name, list):
                    if not list:
                        continue
                    name = _name[0]
                if cls.is_valid_ip(name):
                    continue
                idx = name.find(".")
                if idx > 0:
                    return name[:idx]
                else:
                    return name
        except Exception:
            print("get hostname of [%s] failed" % ip)

        return None

    @classmethod
    def get_ip_network(cls, network, suppress_error=False):
        """ 获取 IP Network """
        try:
            ip_network = netaddr.IPNetwork(network)
            return ip_network
        except Exception as e:
            if not suppress_error:
                print("invalid network [%s]: %s", network, e)
            return None

    @classmethod
    def get_ip_by_if_name(cls, if_name="eth0"):
        """ 获取当前主机指定网卡的IP地址 """
        import fcntl
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(
                fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', bytes(if_name[:15], 'utf-8'))
                )[20:24]
            )
        except Exception as e:
            print(e)
            return 'UNKNOWN'

    @classmethod
    def get_ip_by_hostname(cls, hostname, suppress_warning=False, default=None):
        """ 根据主机名称获取IP地址 """
        try:
            socket.setdefaulttimeout(3)
            ip = socket.gethostbyname(hostname)
        except Exception as e:
            print("failed to get host by name [%s]: %s", hostname, e)
            if suppress_warning:
                print("get ip of [%s] failed" % hostname)
            else:
                print("get ip of [%s] failed" % hostname)

            # NOTE: can't return None, because in many cases, None means local host
            return default if default else hostname
        return ip

    @classmethod
    def get_mac_address(cls, ip_address):
        # 创建ARP请求包
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address)
        # 发送ARP请求并接收响应
        result = srp(arp_request, timeout=3, verbose=False)[0]
        if result:
            mac_address = result[0][1].hwsrc
            return mac_address

    @classmethod
    def ignore_ssl(cls):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    @classmethod
    def normal_exec(cls, args, timeout=60):
        start_time = datetime.datetime.now()
        pipe = subprocess.Popen(args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)

        # pipe.poll()为None 说明没有执行完毕
        while pipe.poll() is None:
            end_time = datetime.datetime.now()
            total_seconds = (end_time - start_time).total_seconds()
            if total_seconds > timeout:
                pipe.terminate()
                raise Exception("exec cmd timeout, cmd: %s, timeout: %s" % (args, timeout))
            time.sleep(0.1)

        stdout, stderr = pipe.communicate()
        return pipe.returncode, stdout.strip(), stderr.strip()


if __name__ == '__main__':
    print(NetTool.get_hostname())

    print(NetTool.get_ip_network("192.168.100.152"))
    print(NetTool.is_ip_network("192.168.100.152"))

    print(NetTool.get_hostname_by_ip("127.0.0.1"))
    print(NetTool.get_hostname_by_ip("192.168.100.152"))

    print(NetTool.get_ip_by_hostname("localhost"))

    print(NetTool.is_ip_reachable("192.168.100.151"))
    print(NetTool.is_ip_port_reachable("192.168.100.151", 22))
    print(NetTool.is_ip_port_reachable("192.168.100.151", 2211))

    print(NetTool.is_valid_ip("192.168.100.151"))
    print(NetTool.is_valid_mac("10:7B:44:80:F4:6A"))

    print(NetTool.ignore_ssl())
    print(NetTool.get_mac_address("192.168.110.167"))
    print(NetTool.get_ip_address())
