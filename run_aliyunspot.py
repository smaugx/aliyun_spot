#!/usr/bin/env python
# coding=utf-8
import json
import time
import datetime
import traceback
import sys
import os
import argparse

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DeleteInstancesRequest import DeleteInstancesRequest


import config


RUNNING_STATUS = 'Running'
CHECK_INTERVAL = 3
CHECK_TIMEOUT = 180


class AliyunRunInstancesExample(object):

    def __init__(self):
        self.access_id = config.access_id
        self.access_secret = config.access_secret

        # 是否只预检此次请求。true：发送检查请求，不会创建实例，也不会产生费用；false：发送正常请求，通过检查后直接创建实例，并直接产生费用
        self.dry_run = False
        # 实例所属的地域ID
        self.region_id = config.region_id
        # 实例的资源规格
        self.instance_type = config.instance_type
        # 实例的计费方式
        self.instance_charge_type = 'PostPaid'
        # 镜像ID
        self.image_id = 'centos_7_05_64_20G_alibase_20181210.vhd'
        # 指定新创建实例所属于的安全组ID
        self.security_group_id = 'sg-j6cfty4xcvay3mcxjgit'
        # 购买资源的时长
        self.period = 1
        # 购买资源的时长单位
        self.period_unit = 'Hourly'
        # 实例所属的可用区编号
        self.zone_id = 'random'
        # 网络计费类型
        self.internet_charge_type = config.internet_charge_type
        # 虚拟交换机ID
        self.vswitch_id = 'vsw-j6cq7w7kut2hur2y685b4'
        # 实例名称
        d  = datetime.datetime.now()
        dsuffix = '{0}{1}{2}{3}'.format(d.month, d.day, d.hour, d.minute)
        self.instance_name = 'smaug-[0,3]-aliyun-{0}'.format(dsuffix)
        # 指定创建ECS实例的数量
        self.amount = config.amount
        # 指定ECS实例最小购买数量：当ECS库存数量小于最小购买数量，会创建失败；当ECS库存数量大于等于最小购买数量，按照库存数量创建
        self.minamount = config.minamount
        # 公网出带宽最大值
        self.internet_max_bandwidth_out = config.internet_max_bandwidth_out
        # 云服务器的主机名
        self.host_name = 'smaug-[0,3]-aliyun-{0}'.format(dsuffix)
        # 是否为I/O优化实例
        self.io_optimized = 'optimized'
        # 密钥对名称
        self.key_pair_name = config.key_pair_name
        # 后付费实例的抢占策略
        self.spot_strategy = config.spot_strategy
        # 设置实例的每小时最高价格
        self.spot_price_limit = config.spot_price_limit
        # 是否开启安全加固
        self.security_enhancement_strategy = 'Active'
        # 系统盘大小
        self.system_disk_size = config.system_disk_size
        # 系统盘的磁盘种类
        self.system_disk_category = config.system_disk_category
        # 释放时间 hours
        auto_release_hour = int(time.time()) + 3600 * config.auto_release_hour
        auto_release_d = datetime.datetime.fromtimestamp(auto_release_hour)
        auto_release_d = '{0}Z'.format(auto_release_d.isoformat())
        self.autoreleasetime = auto_release_d
        
        self.client = AcsClient(self.access_id, self.access_secret, self.region_id)

    def run(self):
        data = None
        try:
            ids = self.run_instances()
            data = self._check_instances_status(ids)
        except ClientException as e:
            print('Fail. Something with your connection with Aliyun go incorrect.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
        except ServerException as e:
            print('Fail. Business error.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
        except Exception:
            print('Unhandled error')
            print(traceback.format_exc())

        return data

    def run_instances(self):
        """
        调用创建实例的API，得到实例ID后继续查询实例状态
        :return:instance_ids 需要检查的实例ID
        """
        request = RunInstancesRequest()
       
        request.set_DryRun(self.dry_run)
        
        request.set_InstanceType(self.instance_type)
        request.set_InstanceChargeType(self.instance_charge_type)
        request.set_ImageId(self.image_id)
        request.set_SecurityGroupId(self.security_group_id)
        request.set_Period(self.period)
        request.set_PeriodUnit(self.period_unit)
        request.set_ZoneId(self.zone_id)
        request.set_InternetChargeType(self.internet_charge_type)
        request.set_VSwitchId(self.vswitch_id)
        request.set_InstanceName(self.instance_name)
        request.set_Amount(self.amount)
        request.set_MinAmount(self.minamount)
        request.set_InternetMaxBandwidthOut(self.internet_max_bandwidth_out)
        request.set_HostName(self.host_name)
        request.set_IoOptimized(self.io_optimized)
        request.set_KeyPairName(self.key_pair_name)
        request.set_SpotStrategy(self.spot_strategy)
        request.set_SpotPriceLimit(self.spot_price_limit)
        request.set_SecurityEnhancementStrategy(self.security_enhancement_strategy)
        request.set_SystemDiskSize(self.system_disk_size)
        request.set_SystemDiskCategory(self.system_disk_category)
        request.set_AutoReleaseTime(self.autoreleasetime)
         
        body = self.client.do_action_with_exception(request)
        data = json.loads(body)
        instance_ids = data['InstanceIdSets']['InstanceIdSet']
        print('Success. Instance creation succeed. InstanceIds: {}'.format(', '.join(instance_ids)))
        return instance_ids

    def delete_instances(self, id_list):
        """
        调用销毁实例的 API
        :return:RequestId 请求ID
        """
        request = DeleteInstancesRequest()
        request.set_accept_format('json')
        
        request.set_InstanceIds(id_list)
        # 是否只预检此次请求。true：发送检查请求，不会创建实例，也不会产生费用；false：发送正常请求，通过检查后直接创建实例，并直接产生费用
        request.set_DryRun(False)
        request.set_Force(True)
        
        response = self.client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))
        return

    def _check_instances_status(self, instance_ids):
        """
        每3秒中检查一次实例的状态，超时时间设为3分钟。
        :param instance_ids 需要检查的实例ID
        :return:
        """
        start = time.time()
        data = None
        while True:
            request = DescribeInstancesRequest()
            request.set_InstanceIds(json.dumps(instance_ids))
            body = self.client.do_action_with_exception(request)
            data = json.loads(body)
            for instance in data['Instances']['Instance']:
                if RUNNING_STATUS in instance['Status']:
                    instance_ids.remove(instance['InstanceId'])
                    print('Instance boot successfully: {}'.format(instance['InstanceId']))

            if not instance_ids:
                print('Instances all boot successfully')
                break

            if time.time() - start > CHECK_TIMEOUT:
                print('Instances boot failed within {timeout}s: {ids}'
                      .format(timeout=CHECK_TIMEOUT, ids=', '.join(instance_ids)))
                break

            time.sleep(CHECK_INTERVAL)

        # 返回实例创建信息
        return data


def create_aliyun_spot():
    data = AliyunRunInstancesExample().run()
    for instance in data['Instances']['Instance']:
        ecs_info_file = "./ecs/ecs.{0}".format(instance.get("InstanceId"))
        with open(ecs_info_file, 'w') as fout:
            fout.write(json.dumps(instance, indent=4))

        print("\n")
        print("InstanceId:{0}".format(instance.get("InstanceId")))
        print("InstanceName:{0}".format(instance.get("InstanceName")))
        print("HostName:{0}".format(instance.get("HostName")))
        print("PublicIp:{0}".format(instance.get("PublicIpAddress").get("IpAddress")[0]))
        print("KeyPairName:{0}".format(instance.get("KeyPairName")))
        print("CreationTime:{0}".format(instance.get("CreationTime")))
        print("AutoReleaseTime:{0}".format(instance.get("AutoReleaseTime")))
        print("instance info saved in file:{0}".format(ecs_info_file))

        print("now you can use ssh: ssh -i {0} root@{1}".format(config.ssh_key_file, instance.get("PublicIpAddress").get("IpAddress")[0]))


def list_local_aliyun_spot():
    id_list = []
    for item in os.listdir("./ecs"):
        abs_item = os.path.join("./ecs", item)
        if not item.startswith('ecs.'):
            continue

        with open(abs_item, 'r') as fin:
            instance = json.loads(fin.read())
            spotid = instance.get("InstanceId")
            if spotid not in id_list:
                id_list.append(spotid)
    return id_list


def release_aliyun_spot(release_id_list):
    print("\nwill release aliyun instance:\n")
    print(release_id_list)
    try:
        AliyunRunInstancesExample().delete_instances(release_id_list)
        for spotid in release_id_list:
            ecs_info_file = "./ecs/ecs.{0}".format(spotid)
            if os.path.exists(ecs_info_file):
                os.remove(ecs_info_file)
    except Exception as e:
        print('catch exception:{0}'.format(e))

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description='aliyunspot, 自动创建阿里云抢占式实例,支持自动/手动释放' 
    parser.add_argument('-c', '--create', help='create aliyun spot instance and run instance',choices=['true', 'false'] , default='false')
    parser.add_argument('-r', '--release', help='release aliyun spot instance',choices=['true', 'false'] , default='false')
    parser.add_argument('-l', '--list', help='list local record aliyun spot instance',choices=['true', 'false'] , default='false')
    parser.add_argument('-s', '--spotid', help='aliyun spot instance_id for release, if more than one, use "," to cut-off ', type=str, default='')

    args = parser.parse_args()

    if args.create == 'true':
        print('will create and run aliyun spot instance\n')
        create_aliyun_spot()
    elif args.release == 'true':
        print("will release aliyun spot instance\n")
        if not args.spotid:
            print("you must give one or more instance id(s)")
            sys.exit(-1)
        sp_id = args.spotid.split(',')
        release_id_list = []
        for item in sp_id:
            if not item:
                continue
            release_id_list.append(item)
        release_aliyun_spot(release_id_list)
    elif args.list == 'true':
        print("will list local record instance\n")
        id_list = list_local_aliyun_spot()
        print(id_list)
    else:
        parser.print_help()
