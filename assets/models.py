from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asset(models.Model):
    '''
    资产总表
    '''
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
    status = models.SmallIntegerField(choices=asset_status,default=0,verbose_name="设备状态")
    manufacturer = models.ForeignKey('Manufacturer',on_delete=models.CASCADE,verbose_name="厂商")
    manage_ip = models.GenericIPAddressField(null=True,blank=True,verbose_name="管理IP")
    tags = models.ManyToManyField('Tag',verbose_name="标签")
    admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name="admin",verbose_name="资产管理人")
    idc = models.ForeignKey('IDC',on_delete=models.CASCADE,verbose_name="所在机房")
    contract = models.ForeignKey('Contract',on_delete=models.CASCADE,null=True,blank=True,verbose_name="合同")
    purchase_day = models.DateField(null=True,blank=True,verbose_name="购买日期")
    expire_day = models.DateField(null=True,blank=True,verbose_name="过保日期")
    price = models.FloatField(null=True,blank=True,verbose_name="价格")
    approved_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,verbose_name="批准人")
    memo = models.TextField(null=True,blank=True,verbose_name="备注")
    c_time = models.DateTimeField(auto_now=True,verbose_name="批准日期")
    m_time = models.DateTimeField(auto_now_add=True,verbose_name="更新日期")
    def __str__(self):
        return '<%s> %s'%(self.get_asset_type_display(),self.name)
    class Meta:
        verbose_name = "资产总表"
        verbose_name_plural = "资产总表"
        ordering = '[-c_time]'



class Server(models.Model):
    '''
    服务器表
    '''
    sub_asset_type_choice = (
        ('0','服务器'),
        ('1','刀片机'),
        ('2','小型机'),
    )
    created_by_choice = (
        ('auto','自动添加'),
        ('manual','手工录入'),
    )
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE,verbose_name="服务器和资产表一对一关系")
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name="服务器类型")
    created_by = models.CharField(max_length=32,choices=created_by_choice,default='auto',verbose_name="添加方式")
    hosted_on = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name="hosted_on_server",
                                  verbose_name="宿主机")
    model = models.CharField(max_length=64,null=True,blank=True,verbose_name="服务器型号")
    raid_type = models.CharField(max_length=64,null=True,blank=True,verbose_name="Raid卡型号")
    os_type = models.CharField(max_length=64,null=True,blank=True,verbose_name="操作系统型号")
    os_distribution = models.CharField(max_length=64,null=True,blank=True,verbose_name="发型版本")
    os_release = models.CharField(max_length=64,null=True,blank=True,verbose_name="操作系统版本")
    def __str__(self):
        return '{assetname}--{assettype}--{model} <sn:{sn}>'.format(assetname=self.asset.name,assettype=self.get_sub_asset_type_display(),
                                                                    model=self.model,sn=self.asset.sn)
    class Meta:
        verbose_name = "服务器"
        verbose_name_plural = "服务器"



class SecurityDevice(models.Model):
    '''
    安全设备表
    '''
    sub_asset_type_choice = (
        ('0','防火墙'),
        ('1','入侵检测设备'),
        ('2','互联网网关'),
        ('3','运维审计系统'),
    )
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE,verbose_name="安全设备和资产表一对一关系")
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name="安全设备类型")
    def __str__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display()
    class Meta:
        verbose_name = "安全设备"
        verbose_name_plural = "安全设备"


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


