from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asset(models.Model):
    asset_type_choice = (
        ('server','服务器'),
        ('networkdevice','网络设备'),
        ('storagedevice','存储设备'),
        ('securitydevice','安全设备'),
        ('software','软件资产'),
    )
    asset_status = (
        ('0','上线'),
        ('1','下线'),
        ('2','未知'),
        ('3','故障'),
        ('4','备用'),
    )
    name = models.CharField(max_length=64,verbose_name="资产名称")
    asset_type = models.CharField(max_length=64,choices=asset_type_choice,default='server',verbose_name="资产类型")
    sn = models.CharField(max_length=128,unique=True,verbose_name="序列号")
    business_unit = models.ForeignKey('BusinessUnit',on_delete=models.CASCADE,verbose_name="所属业务线")
    status = models.SmallIntegerField(choices=asset_status,default='0',verbose_name="设备状态")
    manufacturer = models.ForeignKey('Manufacturer',on_delete=models.CASCADE,verbose_name="厂商")
    manage_ip = models.GenericIPAddressField(null=True,blank=True,verbose_name="管理IP")
    tags = models.ManyToManyField('Tag',verbose_name="标签")
    admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name="admin",verbose_name="资产管理人")
    idc = models.ForeignKey('IDC',on_delete=models.CASCADE,verbose_name="所在机房")
    contract =


class Server(models.Model):
    pass



class SecurityDevice(models.Model):
    pass


class StorageDevice(models.Model):
    pass

class NetworkDevice(models.Model):
    pass

class SoftWare(models.Model):
    pass

class IDC(models.Model):
    pass

class Manufacturer(models.Model):
    pass

class BusinessUnit(models.Model):
    pass

class Contract(models.Model):
    pass

class Tag(models.Model):
    pass

class CPU(models.Model):
    pass

class RAM(models.Model):
    pass

class Disk(models.Model):
    pass

class NIC(models.Model):
    pass

class EventLog(models.Model):
    pass

class NewAssetApprovalZone(models.Model):
    pass


