# !usr/bin/env python3
# -*- coding:utf-8 -*- 
"""
@project = CMDB
@file = sys_info
@author = Easton Liu
@time = 2018/12/8 20:54
@Description: 获取Linux系统信息

"""
import subprocess

def collect():
    filter_key = ['Manufacturer', 'Serial Number', 'Product Name', 'UUID', 'Wake-up Type']
    raw_data = {}
    for key in filter_key:
        res = subprocess.Popen("sudo dmidecode -t system | grep '%s'" % key,stdout=subprocess.PIPE,shell=True)
        res = res.stdout.read().decode()
        data_list = res.split(":")
        if len(data_list) == 2:
            raw_data[key] = data_list[1].strip()
        else:
            raw_data[key] = ' '
    data = dict()
    data['manufacturer'] = raw_data['Manufacturer']
    data['asset_type'] = 'server'
    data['model'] = raw_data['Product Name']
    data['sn'] = raw_data['Serial Number']
    data['uuid'] = raw_data['UUID']
    data['wake_up_type'] = raw_data['Wake-up Type']
    data.update(get_cpu_info())
    data.update(get_os_info())
    data.update(get_ram_info())
    data.update(get_nic_ifo())
    data.update(get_disk_info())
    return data

def get_os_info():
    '''
    获取操作系统信息
    :return:dic
    '''
    distributor = subprocess.Popen("lsb_release -a|grep 'Distributor ID'",stdout=subprocess.PIPE,shell=True)
    distributor = distributor.stdout.read().decode().split(':')
    release = subprocess.Popen("lsb_release -a|grep 'Description'",stdout=subprocess.PIPE,shell=True)
    release = release.stdout.read().decode().split(":")
    data = {
        'os_distribution':distributor[1].strip() if len(distributor) >1 else '',
        'os_release':release[1].strip() if len(release) >1 else '',
        'os_type':'linux'
    }
    return data

def get_cpu_info():
    '''
    获取CPU信息
    :return: dic
    '''
    base_cmd = 'cat /proc/cpuinfo'
    raw_data = {
        'cpu_model':"%s|grep 'model name'|head -1" % base_cmd,
        'cpu_count':"%s|grep 'processor'|wc -l" % base_cmd,
        'cpu_core_count':"%s|grep 'cpu cores' |awk -F: '{SUM +=$2} END {print SUM}'" % base_cmd
    }
    for key,cmd in raw_data.items():
        try:
            cmd_res = subprocess.Popen(raw_data[key],stdout=subprocess.PIPE,shell=True)
            raw_data[key] = cmd_res.stdout.read().decode().strip()
        except:
            raw_data[key]=''
    data = {
        'cpu_model':raw_data['cpu_model'].split(':')[1].strip(),
        'cpu_count':raw_data['cpu_count'],
        'cpu_core_count':raw_data['cpu_core_count']
    }
    return data

def get_ram_info():
    '''
    获取内存信息
    :return: dic
    '''
    raw_data = subprocess.Popen("sudo dmidecode -t memory",stdout=subprocess.PIPE,shell=True)
    raw_list = raw_data.stdout.read().decode().split('\n')
    raw_ram_list = []
    item_list = []
    for line in raw_list:
        if line.startswith("Memory Device"):
            raw_ram_list.append(item_list)
            item_list = []
        else:
            item_list.append(line)
    raw_ram_list.append(item_list)
    ram_list = []
    for item in raw_ram_list:
        ram_item_to_dic = {}
        for i in item:
            d = i.split(':')
            if len(d)==2:
                k,v = d
                if k == 'Size':
                    ram_item_to_dic['capacity'] = v.split()[0].strip()
                if k == 'Type':
                    ram_item_to_dic['model'] = v.strip()
                if k == 'Manufacturer':
                    ram_item_to_dic['manufacturer'] = v.strip()
                if k == 'Serial Number':
                    ram_item_to_dic['sn'] = v.strip()
                if k == 'Asset Tag':
                    ram_item_to_dic['asset_tag'] = v.strip()
                if k == 'Locator':
                    ram_item_to_dic['slot'] = v.strip()
        ram_list.append(ram_item_to_dic)
    ram_data = {'ram':ram_list}
    ram_total_size = subprocess.Popen("cat /proc/meminfo|grep MemTotal",stdout=subprocess.PIPE,shell=True)
    ram_total_size = ram_total_size.stdout.read().decode().split(':')
    if len(ram_total_size) == 2:
        total_gb_size = int(ram_total_size[1].split()[0])/1024**2
        ram_data['ram_szie'] = total_gb_size
    return ram_data

def get_nic_ifo():
    '''
    获取网卡信息
    :return:
    '''
    raw_data = subprocess.Popen("ifconfig -a",stdout=subprocess.PIPE,shell=True)
    raw_data = raw_data.stdout.read().decode().split('\n')
    nic_dic = {}
    next_ip_line = False
    last_mac_addr = None
    for line in raw_data:
        if next_ip_line:
            next_ip_line = False
            nic_name = last_mac_addr.split()[0].strip()
            mac_addr = last_mac_addr.strip('HWaddr')[1].strip()
            raw_ip_addr = line.split('inet addr:')
            raw_bcast = line.split('Bcast:')
            raw_netmask = line.split('Mask:')
            if len(raw_ip_addr) == 2:
                ip_addr = raw_ip_addr[1].split()[0]
                bcast = raw_bcast[1].split()[0]
                netmask = raw_netmask[1].split()[0]
            else:
                ip_addr = None
                bcast = None
                netmask = None
            if mac_addr not in nic_dic:
                nic_dic[mac_addr] = {
                    'name':nic_name,
                    'mac':mac_addr,
                    'bcast':bcast,
                    'netmask':netmask,
                    'boding':0,
                    'model':'unknown',
                    'ip_addr':ip_addr
                }
            else:
                if '%s_boding_addr1' % mac_addr not in nic_dic:
                    random_mac_addr = '%s_boding_addr1' % mac_addr
                else:
                    random_mac_addr = '%s_boding_addr2' % mac_addr
                nic_dic[random_mac_addr] = {
                    'name': nic_name,
                    'mac': random_mac_addr,
                    'bcast': bcast,
                    'netmask': netmask,
                    'boding': 1,
                    'model': 'unknown',
                    'ip_addr': ip_addr
                }
        if 'HWaddr' in line:
            next_ip_line = True
            last_mac_addr = line
    nic_list = []
    for k,v in nic_dic.items():
        nic_list.append(v)
    data = {
        'nic':nic_list
    }
    return data

def get_disk_info():
    '''
    获取磁盘信息
    :return:
    '''
    # raw_data = subprocess.Popen("sudo hdparm -i /dev/sda | grep Model",stdout=subprocess.PIPE,shell=True)
    # raw_data = raw_data.stdout.read().decode()
    # data_list = raw_data.split(',')
    # model = data_list[0].split('=')[1].strip()
    # sn = data_list[2].split('=')[1].strip()
    # size_data = subprocess.Popen("sudo fdisk -l /dev/sda | grep Disk | head -1",stdout=subprocess.PIPE,shell=True)
    # size_data = size_data.stdout.read().decode()
    # size = size_data.split(":")[1].strip().split(",")[0].strip()
    disk_dict = dict()
    disk_dict["model"] = 'dell'
    disk_dict["sn"] = '123654'
    disk_dict["size"] = '800'
    data = {
        'physical_disk_driver':[disk_dict]
    }
    return data

if __name__ == '__main__':
    d = collect()
    print(d)




