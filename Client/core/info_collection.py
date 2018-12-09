# !usr/bin/env python3
# -*- coding:utf-8 -*- 
"""
@project = CMDB
@file = info_collection
@author = Easton Liu
@time = 2018/12/9 21:12
@Description: 

"""
import platform
import sys

def linux_sys_info():
    from ..plugins.linux import sys_info
    return sys_info.collect()
def windows_sys_info():
    from ..plugins.windows import sys_info
    return sys_info.collect()

class InfoCollection(object):
    def collect(self):
        try:
            func = getattr(self,platform.system())
            info_data = func()
            return info_data
        except AttributeError:
            sys.exit('不支持当前操作系统： [%s]!' % platform.system())
    def Linux(self):
        return linux_sys_info()
    def Windows(self):
        return windows_sys_info()
