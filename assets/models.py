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
        ordering = ['-c_time']



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
    '''存储设备'''
    sub_asset_type_choice = (
        ('0','磁盘阵列'),
        ('1','网络存储器'),
        ('2','磁带库'),
        ('3','磁带机')
    )
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE,verbose_name="存储设备和资产表一对一关系")
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name="存储设备类型")

    def __str__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display()
    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = "存储设备"

class NetworkDevice(models.Model):
    '''网络设备'''
    sub_asset_type_choice = (
        ('0','路由器'),
        ('1','交换机'),
        ('2','负载均衡器'),
        ('3','VPN设备')
    )
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE,verbose_name="网络设备和资产表一对一关系")
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name="网络设备类型")
    vlan_ip = models.GenericIPAddressField(null=True,blank=True,verbose_name="VlanIP")
    intranet_ip = models.GenericIPAddressField(null=True,blank=True,verbose_name="内网IP")
    model = models.CharField(max_length=128,null=True,blank=True,verbose_name="网络设备型号")
    firmware = models.CharField(max_length=128,null=True,blank=True,verbose_name="设备固件版本")
    port_num = models.SmallIntegerField(null=True,blank=True,verbose_name="端口数")
    device_detail = models.TextField(null=True,blank=True,verbose_name="详细配置")
    def __str__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display()
    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = "网络设备"

class SoftWare(models.Model):
    '''软件资产'''
    sub_asset_type_choice = (
        ('0','操作系统'),
        ('1','办公\开发软件'),
        ('2','业务软件')
    )
    asset = models.OneToOneField("Asset",on_delete=models.CASCADE,verbose_name="软件资产和资产表一对一关系")
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name="软件类型")
    license_num = models.IntegerField(default=1,verbose_name="授权数量")
    version = models.CharField(max_length=128,help_text='例如：CentOS release 6.7 (Final)',verbose_name="软件版本")
    def __str__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display()
    class Meta:
        verbose_name = "软件资产"
        verbose_name_plural = "软件资产"

class IDC(models.Model):
    '''机房'''
    name = models.CharField(max_length=128,unique=True,verbose_name="机房名称")
    memo = models.CharField(max_length=256,null=True,blank=True,verbose_name="备注")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "机房"
        verbose_name_plural = "机房"

class Manufacturer(models.Model):
    '''厂商'''
    name = models.CharField(max_length=128,verbose_name="厂商名称")
    telephone = models.CharField(max_length=11,null=True,blank=True,verbose_name="联系电话")
    memo = models.CharField(max_length=256,null=True,blank=True,verbose_name="备注")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "制造商"
        verbose_name_plural = "制造商"

class BusinessUnit(models.Model):
    '''业务线'''
    parent_unit = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name="parent_level")
    name = models.CharField(max_length=64,verbose_name="业务线名称")
    memo = models.CharField(max_length=256,null=True,blank=True,verbose_name="备注")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "业务线"
        verbose_name_plural = "业务线"

class Contract(models.Model):
    '''合同'''
    sn = models.CharField(max_length=128,unique=True,verbose_name="合同号")
    name = models.CharField(max_length=64,verbose_name="合同名称")
    price = models.FloatField(verbose_name="合同金额")
    detail = models.TextField(null=True,blank=True,verbose_name="合同详情")
    start_day = models.DateField(null=True,blank=True,verbose_name="合同开始日期")
    end_day = models.DateField(null=True,blank=True,verbose_name="合同结束日期")
    license_num = models.IntegerField(null=True,blank=True,verbose_name="license数量")
    c_day = models.DateTimeField(auto_now_add=True,verbose_name="创建日期")
    m_day = models.DateTimeField(auto_now=True,verbose_name="修改日期")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "合同"
        verbose_name_plural = "合同"


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=128,verbose_name="标签名称")
    c_day = models.DateTimeField(auto_now_add=True,verbose_name="创建日期")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"

class CPU(models.Model):
    '''CPU组件'''
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE,verbose_name='CPU和资产表一对一关系')
    cpu_model = models.CharField(max_length=64,null=True,blank=True,verbose_name="CPU型号")
    cpu_count = models.PositiveSmallIntegerField(default=1,verbose_name="物理CPU个数")
    cpu_core_count = models.PositiveSmallIntegerField(default=2,verbose_name="CPU核数")
    def __str__(self):
        return self.asset.name + '--' + self.cpu_model
    class Meta:
        verbose_name = "CPU组件"
        verbose_name_plural = "CPU组件"


class RAM(models.Model):
    '''内存组件'''
    asset = models.ForeignKey('Asset',on_delete=models.CASCADE)
    sn = models.CharField(max_length=128,null=True,blank=True,verbose_name="SN号")
    model = models.CharField(max_length=64,null=True,blank=True,verbose_name="内存型号")
    manufacturer = models.CharField(max_length=64,null=True,blank=True,verbose_name="制造厂家")
    slot = models.CharField(max_length=64,verbose_name="插槽")
    capacity = models.IntegerField(verbose_name="内存大小(GB)")
    def __str__(self):
        return '%s:%s:%s:%s'%(self.asset.name,self.model,self.manufacturer,self.slot)
    class Meta:
        verbose_name = "内存组件"
        verbose_name_plural = "内存组件"
        unique_together = ('asset','slot')

class Disk(models.Model):
    '''存储设备'''
    interface_type_choice = (
        ('SATA','SATA'),
        ('SAS','SAS'),
        ('SCSI','SCSI'),
        ('SSD','SSD'),
        ('unknow','unknow')
    )
    asset = models.ForeignKey('Asset',on_delete=models.CASCADE)
    sn = models.CharField(max_length=128,verbose_name="硬盘SN号")
    slot = models.CharField(max_length=64,null=True,blank=True,verbose_name="硬盘插槽")
    model = models.CharField(max_length=64,null=True,blank=True,verbose_name="型号")
    manufacturer = models.CharField(max_length=128,null=True,blank=True,verbose_name="制造厂家")
    capacity = models.IntegerField(null=True,blank=True,verbose_name="硬盘容量(GB)")
    interface_type = models.CharField(max_length=16,choices=interface_type_choice,default='unknow',verbose_name="硬盘接口类型")
    def __str__(self):
        return '%s: %s: %s: %sGB'%(self.asset.name,self.model,self.slot,self.capacity)
    class Meta:
        verbose_name = "硬盘"
        verbose_name_plural = "硬盘"
        unique_together = ('asset','sn')

class NIC(models.Model):
    '''网卡'''
    asset = models.ForeignKey('Asset',on_delete=models.CASCADE,verbose_name="网卡和资产表关联关系")
    name = models.CharField(max_length=64,null=True,blank=True,verbose_name="网卡名称")
    model = models.CharField(max_length=64,verbose_name="网卡型号")
    mac = models.CharField(max_length=64,verbose_name="网卡Mac地址")
    ip_addr = models.GenericIPAddressField(null=True,blank=True,verbose_name="网卡IP地址")
    net_mask = models.GenericIPAddressField(null=True,blank=True,verbose_name="掩码")
    bonding = models.GenericIPAddressField(null=True,blank=True,verbose_name="绑定地址")
    def __str__(self):
        return "%s: %s: %s"%(self.asset.name,self.model,self.mac)
    class Meta:
        verbose_name = "网卡"
        verbose_name_plural = "网卡"
        unique_together = ('asset', 'model','mac')

class EventLog(models.Model):
    '''日志'''
    event_type_choice = (
        ('0','其他'),
        ('1','硬件变更'),
        ('2','新增配件'),
        ('3','设备下线'),
        ('4','设备上线'),
        ('5','定期维护'),
        ('6','业务上线\更新')
    )
    name = models.CharField(max_length=64,verbose_name="事件名称")
    asset = models.ForeignKey('Asset',null=True,blank=True,on_delete=models.SET_NULL)
    new_asset = models.ForeignKey('NewAssetApprovalZone',null=True,blank=True,on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField(choices=event_type_choice,default=0,verbose_name="事件类型")
    component = models.CharField(max_length=256,null=True,blank=True,verbose_name="事件子项")
    detail = models.TextField(verbose_name="事件详情")
    date = models.DateTimeField(auto_now_add=True,verbose_name="事件时间")
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="事件执行人")
    memo = models.TextField(null=True,blank=True,verbose_name="备注")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "日志"
        verbose_name_plural = "日志"

class NewAssetApprovalZone(models.Model):
    '''新资产待审批'''
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('IDC', '机房'),
        ('software', '软件资产'),
    )
    sn = models.CharField(max_length=128,unique=True,verbose_name="资产SN号")
    asset_type = models.CharField(max_length=64,choices=asset_type_choice,default='server',verbose_name="资产类型")
    manufacturer = models.CharField(max_length=128,null=True,blank=True,verbose_name="生产厂家")
    model = models.CharField(max_length=64,null=True,blank=True,verbose_name="资产型号")
    ram_size = models.SmallIntegerField(null=True,blank=True,verbose_name="内存大小")
    cpu_model = models.CharField(max_length=64,null=True,blank=True,verbose_name="cpu型号")
    cpu_count = models.PositiveSmallIntegerField(null=True,blank=True,verbose_name="cpu数量")
    cpu_core_count = models.PositiveSmallIntegerField(null=True,blank=True,verbose_name="cpu核数")
    os_distribution = models.CharField(max_length=64,null=True,blank=True,verbose_name="系统发行版本")
    os_type = models.CharField(max_length=64,null=True,blank=True,verbose_name="操作系统型号")
    os_release = models.CharField(max_length=64,null=True,blank=True,verbose_name="操作系统版本")
    data = models.TextField(verbose_name="资产数据")
    c_time = models.DateTimeField(auto_now_add=True,verbose_name="创建日期")
    m_time = models.DateTimeField(auto_now=True,verbose_name="更新日期")
    approved = models.BooleanField(default=False,verbose_name="是否批准")
    def __str__(self):
        return self.sn
    class Meta:
        verbose_name = "新上线待批准资产"
        verbose_name_plural = "新上线待批准资产"
        ordering = ['-c_time']





