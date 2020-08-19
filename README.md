# aliyun_spot
自动创建阿里云抢占式实例。

# [支持一下作者，购买阿里云](https://www.aliyun.com/minisite/goods?userCode=c5nuzwoj)

# 背景
阿里云抢占式实例应该属于阿里云的一种闲置资源利用，性价比非常高，每小时的价格在 0.01 ~ 0.05 每小时，具体根据不同的配置和地域有差别，流量价格小于 1元/G.

抢占式实例最高可以以**一折的价格购买 ECS 实例，并能稳定持有该实例至少一个小时**。一个小时后，当市场价格高于您的出价或资源供需关系变化时，**抢占式实例会被自动释放**，请做好数据备份工作。

**非常适合爬虫**

**非常适合爬虫**

**非常适合爬虫**

也适合程序员个人日常开发使用，上班来创建，下班释放，开销基本可以控制在在 1毛 ~ 2 毛。

对于我来说，最近在写一个爬虫，看了很多代理都很贵，免费的又不稳定，正好了解到阿里云的抢占式实例，所以非常满足我的需求。

但是要注意，这个实例是有可能被释放的，但是不用担心，比如**香港地区的释放率最近（2020-08-19）小于 3%. 另外，每个人可以最大创建 100 个实例**，所以还是不用太担心。

# 脚本功能
## 自动创建阿里云抢占式实例
支持以下一些参数：

+ 实例所属地域
+ 创建的实例数量
+ 公网出口带宽最大值
+ 实例付费的策略和每小时最大价格
+ 系统盘大小
+ 释放时间（hours）

## 手动释放一个或者多个实例
可以使用脚本提前释放一个或者多个实例



# 如何使用

```
$ python run_aliyunspot.py
usage: run_aliyunspot.py [-h] [-c {true,false}] [-r {true,false}] [-l {true,false}] [-s SPOTID]

aliyunspot, 自动创建阿里云抢占式实例,支持自动/手动释放

optional arguments:
  -h, --help            show this help message and exit
  -c {true,false}, --create {true,false}
                        create aliyun spot instance and run instance
  -r {true,false}, --release {true,false}
                        release aliyun spot instance
  -l {true,false}, --list {true,false}
                        list local record aliyun spot instance
  -s SPOTID, --spotid SPOTID
                        aliyun spot instance_id for release, if more than one, use "," to cut-off
```


1 克隆仓库

```
$ git clone https://github.com/smaugx/aliyun_spot.git
$ cd aliyun_spot
$ virtualenv -p python3 vv
$ source vv/bin/activate
$ pip install -r requirements.txt
```

2  调整配置

```
$ cp test_config.py config.py
# 打开配置文件，根据你自己的需求修改里面的配置选项
$ vim config.py
```

当然你也可以不用修改其他配置，只需要把你的 **access_id** 和 **access_secret** 填进去就可以，以及 **key_pair_name** 填进去。（见后文章节 #阿里云官网操作# ）

**默认创建的是香港地区的抢占式实例，内存 500MB, 1 CPU, 系统盘 20GB, 按流量计费（1元/G), 公网出口带宽 10Mbps, 1 小时候自动释放。**

> 2020-08-19 上述默认配置的实例价格在 ￥ 0.018 /时。


3 创建实例

```
$ python run_aliyunspot.py -c true

will create and run aliyun spot instance

Success. Instance creation succeed. InstanceIds: i-j6ci3ugz59bvb3y41uf4
Instance boot successfully: i-j6ci3ugz59bvb3y41uf4
Instances all boot successfully


InstanceId:i-j6ci3ugz59bvb3y41uf4
InstanceName:smaug-000-aliyun-8192314
HostName:smaug-000-aliyun-8192314
PublicIp:8.210.168.220
KeyPairName:aliyunspot
CreationTime:2020-08-19T15:14Z
AutoReleaseTime:2020-08-20T00:14Z
now you can use ssh: ssh -i ~/.ssh/aliyunspot.pem root@8.210.168.220

```

如上，创建成功。然后接下来就可以使用 ssh 登录：

```
$ ssh -i ~/.ssh/~/.ssh/aliyunspot.pem root@8.210.245.226
```

4 列出实例

```
$ python run_aliyunspot.py -l true
will list local record instance

['i-j6ci3ugz59bvb3y41uf4', 'i-j6ca8vgb7qexh4w1zlya']
```

注意，上面仅仅是把之前创建并保存的实例信息从文件当中读取出来，并没有与 aliyun 交互。

5 释放实例

```
$ python run_aliyunspot.py -r true -s i-j6ce2by63lt3n4xq1ygk
will release aliyun spot instance


will release aliyun instance:

['i-j6ce2by63lt3n4xq1ygk']
{"RequestId":"284754E1-EE8A-4DBB-B440-B59B8A594EAC"}
```

# [阿里云官网操作](https://www.aliyun.com/minisite/goods?userCode=c5nuzwoj)

上面提到了几个配置是需要在阿里云官网操作的。

**阿里云官网的使用还是挺复杂的，因为功能太多了，花费了我至少一个上午的时间才熟悉了整个操作，完成了整个脚本**

**所以整理了这个脚本方便大家使用，对阿里云的操作只需要下面几个：**

+ 注册一个阿里云账号，这个不用说了吧
+ 充值 100 元以上，比如 130 元。因为创建实例账号里至少要 100 元
+ 点击 [https://ram.console.aliyun.com/overview](https://ram.console.aliyun.com/overview) 创建一个用户组，分配权限 AliyunECSFullAccess 和 AliyunVPCFullAccess
+ 还是上一步的页面，添加 ram 子账号，添加到刚才创建的用户组，这个账号会用来编程访问 aliyun API
+ 还是上一步的页面，为这个ram 子账号创建 AccessKey。**记得保存好**。
+ 在 [https://ecs.console.aliyun.com/](https://ecs.console.aliyun.com/) 页面选择 网络与安全-密钥对，创建密钥对 aliyunspot (名字任意），会自动下载这个私钥，**记得保存好，一般要放到 ~/.ssh 目录下，并且记得  `chmod 600 aliyunspot.pem`**


OK, 到这里基本上得到了我们脚本里需要的几个配置：

+ access_id
+ access_secret
+ key_pair_name


把上述几个配置填到 config.py 中即可。

然后开始创建和管理你的实例吧！！

然后开始创建和管理你的实例吧！！

然后开始创建和管理你的实例吧！！


