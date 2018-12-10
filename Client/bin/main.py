# !usr/bin/env python3
# -*- coding:utf-8 -*- 
"""
@project = CMDB
@file = main
@author = Easton Liu
@time = 2018/12/8 18:59
@Description: 

"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from Client.core import handler
if __name__ == '__main__':
    handler.ArgvHandler(sys.argv)
