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

# class NewAsset(object):
#     def __init__(self,data):
#         self.data = data
#     def add_to_new_zone(self):
#         defaults1 = {
#             'data': json.dumps(self.data),
#             'asset_type': self.data.get('asset_type'),
#             'manufacturer': self.data.get('manufacturer'),
#             'model': self.data.get('model'),
#             'ram_size': self.data.get('ram_size'),
#             'cpu_model': self.data.get('cpu_model'),
#             'cpu_count': self.data.get('cpu_count'),
#             'cpu_core_count': self.data.get('cpu_core_count'),
#             'os_distribution': self.data.get('os_distribution'),
#             'os_release': self.data.get('os_release'),
#             'os_type': self.data.get('os_type'),
#         }
#         models.NewAssetApprovalZone.objects.update_or_create(sn=self.data.get('sn'),defaults=defaults1)
#         return '资产已经加入或更新待审批区！'
def log(log_type,msg=None,asset=None,new_asset=None,request=None):
    '''
    记录日志
    :param log_type:
    :param msg:
    :param asset:
    :param new_asset:
    :param request:
    :return:
    '''
    event = models.EventLog()
    if log_type == 'upline':
        event.name = '%s<%s>: 上线' % (asset.name,asset.sn)
        event.asset = asset
        event.detail = '资产成功上线'
        event.user = request.user
    elif log_type == 'approve_failed':
        event.name = '%s<%s>: 审批失败' % (new_asset.asset_type,new_asset.sn)
        event.new_asset = new_asset
        event.detail = '审批失败! \n%s' % msg
        event.user = request.user
    event.save()

class ApproveAsset:
    '''
    审批资产并上线
    '''
    def __init__(self,request,assetid):
        self.request = request
        self.new_asset = models.NewAssetApprovalZone.objects.get(id=assetid)
        self.data = self.new_asset.data
    def _create_asset(self):
        '''
        创建资产并上线
        :return:
        '''
        asset = models.Asset.objects.create(asset_type=self.new_asset.asset_type,
                                            name="%s:%s" %(self.new_asset.asset_type,self.new_asset.sn),
                                            sn = self.new_asset.sn,
                                            approved_by= self.request.user)
        return asset
    def _create_manufacturer(self,asset):
        '''
        创建厂商
        :return:
        '''
        m = self.new_asset.manufacturer
        if m:
            manufacturer_obj,_ = models.Manufacturer.objects.get_or_create(name=m)
            asset.manufacturer = manufacturer_obj
            asset.save()
    def _create_server(self,asset):
        '''
        创建服务器
        :param asset:
        :return:
        '''
        models.Server.objects.create(asset=asset,
                                     model=self.new_asset.model,
                                     os_type=self.new_asset.os_type,
                                     os_distribution=self.new_asset.os_distribution,
                                     os_release=self.new_asset.os_release)
    def _create_CPU(self,asset):
        '''
        创建CPU
        :param asset:
        :return:
        '''
        models.CPU.objects.create(asset=asset,
                                  cpu_model=self.new_asset.cpu_model,
                                  cpu_count=self.new_asset.cpu_count,
                                  cpu_core_count=self.new_asset.cpu_core_count)
    def _create_RAM(self,asset):
        '''
        创建内存
        :param asset:
        :return:
        '''
        ram_list = self.data.get('ram')
        if not ram_list:
            return
        for ram_dict in ram_list:
            ram = models.RAM()
            ram.asset = asset
            ram.slot = ram_dict.get('slot','未知的内存插槽')
            ram.sn = ram_dict.get('sn')
            ram.model = ram_dict.get('model')
            ram.manufacturer = ram_dict.get('manufauturer')
            ram.capacity = ram_dict.get('capacity',0)
            ram.save()
    def _create_disk(self,asset):
        '''
        创建存储设备
        :param asset:
        :return:
        '''
        disk_list = self.data.get('physical_disk_driver')
        if not disk_list:
            return
        for disk_dict in disk_list:
            disk = models.Disk()
            disk.sn = disk_dict.get('sn','未知sn的硬盘！')
            disk.asset = asset
            disk.model = disk_dict.get('model')
            disk.manufacturer = disk_dict.get('manufacturer')
            disk.slot = disk_dict.get('slot')
            disk.capacity = disk_dict.get('capacity',0)
            iface = disk_dict.get('iface_type')
            if iface in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown']:
                disk.interface_type = iface
            disk.save()
    def _create_nic(self,asset):
        '''
        创建网卡
        :param asset:
        :return:
        '''
        nic_list = self.data.get('nic')
        if not nic_list:
            return
        for nic_dict in nic_list:
            nic = models.NIC()
            nic.mac = nic_dict.get('mac','网卡缺少mac地址')
            nic.model = nic_dict.get('model','网卡型号未知')








