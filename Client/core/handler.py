# !usr/bin/env python3
# -*- coding:utf-8 -*- 
"""
@project = CMDB
@file = handler
@author = Easton Liu
@time = 2018/12/9 22:28
@Description: 

"""
import json
import urllib.parse
import urllib.request
from Client.core.info_collection import InfoCollection
from Client.conf import settings

class ArgvHandler(object):
    def __init__(self,args):
        self.args = args
        self.parse_args()
    def parse_args(self):
        if len(self.args) > 1 and hasattr(self,self.args[1]):
            func = getattr(self,self.args[1])
            func()
        else:
            self.help_msg()
    def help_msg(self):
        '''
        帮助说明
        :return:
        '''
        msg = '''
                collect_data   收集硬件信息
                report_data    收集硬件信息并汇报
              '''
        print(msg)
    @staticmethod
    def collect_data():
        '''
        收集硬件信息，用于测试
        :return:
        '''
        info = InfoCollection().collect()
        print(info)
    @staticmethod
    def report_data():
        '''
        收集硬件信息并上报
        :return:
        '''
        info = InfoCollection().collect()
        data = {'asset_data':json.dumps(info)}
        print(data)
        url = "http://%s:%s%s" % (settings.Params.get('server'),settings.Params.get('port'),settings.Params.get('url'))
        print('正在将数据发送至： [%s]  ......' % url)
        try:
            data_encode = urllib.parse.urlencode(data).encode()
            respose = urllib.request.urlopen(url,data=data_encode,timeout=settings.Params.get("request_timeout"))
            print("\033[31;1m发送完毕！\033[0m ")
            message = respose.read().decode()
            print("返回结果：%s" % message)
        except Exception as e:
            print("\033[31;1m发送失败，%s\033[0m" % e)

