# !usr/bin/env python3
# encoding:utf-8
"""
@project = cmdb
@file = asset_handler
@author = 'Easton Liu'
@creat_time = 2018/12/10 20:04
@explain:

"""
import json
from assets import models

class NewAsset(object):
    def __init__(self,data):
        self.data = data
    def add_to_new_zone(self):
        defaults1 = {
            'data': json.dumps(self.data),
            'asset_type': self.data.get('asset_type'),
            'manufacturer': self.data.get('manufacturer'),
            'model': self.data.get('model'),
            'ram_size': self.data.get('ram_size'),
            'cpu_model': self.data.get('cpu_model'),
            'cpu_count': self.data.get('cpu_count'),
            'cpu_core_count': self.data.get('cpu_core_count'),
            'os_distribution': self.data.get('os_distribution'),
            'os_release': self.data.get('os_release'),
            'os_type': self.data.get('os_type'),
        }
        models.NewAssetApprovalZone.objects.update_or_create(sn=self.data.get('sn'),defaults=defaults1)
        return '资产已经加入或更新待审批区！'

