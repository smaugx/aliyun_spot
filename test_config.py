# coding=utf-8

access_id = 'your_access_id'
access_secret = 'your_access_secret'
ssh_key_file = "~/.ssh/your_key"

# 实例所属的地域ID
region_id = 'cn-hongkong'
# 网络计费类型
internet_charge_type = 'PayByTraffic'
# 指定创建ECS实例的数量
amount = 1
# 指定ECS实例最小购买数量：当ECS库存数量小于最小购买数量，会创建失败；当ECS库存数量大于等于最小购买数量，按照库存数量创建
minamount = 1
# 公网出带宽最大值
internet_max_bandwidth_out = 2
# 密钥对名称
key_pair_name = 'alitemptop'
# 后付费实例的抢占策略
spot_strategy = 'SpotWithPriceLimit'
# 设置实例的每小时最高价格
spot_price_limit = 0.03
# 系统盘大小
system_disk_size = '20'
# 系统盘的磁盘种类
system_disk_category = 'cloud_efficiency'
# 释放时间 hours
auto_release_hour = 24 * 3
