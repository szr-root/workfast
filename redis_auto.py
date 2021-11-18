import json
from hashlib import md5
from time import sleep

import requests
from sshtunnel import SSHTunnelForwarder
import redis

nas_cert = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-cert.pem"
nas_key = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-key.pem"
woop_cert = "/Users/pof/PycharmProjects/workfast/check_status/client.cert.pem"
woop_key = "/Users/pof/PycharmProjects/workfast/check_status/client.key.nopwd.pem"
nas = (nas_cert, nas_key)
woop = (woop_cert, woop_key)

host_jump = "ec2-18-162-52-149.ap-east-1.compute.amazonaws.com"
port_jump = 22
ssh_pkey = '/Users/pof/.ssh/id_rsa'
host_redis = "stage.z1p6ym.ng.0001.ape1.cache.amazonaws.com"
port_redis = 6379


def get_nas_token():
    url = "https://dev-nas.apiteamn.com/api/login"
    body = {"username": "admin",
            "password": "WP-nas2018"}
    r = requests.post(url=url, data=json.dumps(body), cert=nas)
    return r.json()['data']['token']


def get_user_dispalyname(token, uid):
    url = "https://dev-nas.apiteamn.com/api/profile/" + uid
    nas_token = "Bearer " + token
    header = {"Authorization": nas_token}
    r = requests.get(url=url, headers=header, cert=nas)
    return r.json()['data']['profile']['display_name']


# 增加read_at时间，使账号成为老用户（存在曝光数据）
def who_like_me_read(user_token):
    url = "https://dev.apiteamn.com/api-getway/cards/who-liked-me/read"
    body = {
        "last_created_at": 1631525177000,
        "gmt_offset": 28800
    }
    user_token = "Bearer " + user_token
    header = {"Authorization": user_token}
    requests.post(url=url, data=json.dumps(body), headers=header)


def login(user_name, password):
    url = "https://dev.apiteamn.com/api-getway/login"
    password = md5((password + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
    body = {
        "platform_id": user_name,
        "platform": 0,
        "token": password,
        "device": {
            "device_id": "device_" + user_name,
            "device_type": 3,
            "machine": "postman",
            "language": "en-CN;q=1, zh-Hans-CN;q=0.9, ja-CN;q=0.8",
            "os_version": "1.0.0",
            "vpn_on": True,
            "app_build": 60300
        }
    }
    login_response = requests.post(url, json.dumps(body), cert=woop)
    return login_response.json()


# 删除曝光数据
def del_redis_ly_info(uid):
    print(r.delete('{%s}:c:ly:info' % uid))


# 获取ly：info信息
def get_redis_ly_info(uid):
    print('获取ly-info信息...')
    ly_info = (r.hgetall('{%s}:c:ly:info' % uid))
    print(ly_info)
    print('已完成...\n')
    return ly_info


# 消除ly-info信息，制造free trial
def del_ly_info(uid):
    print('消除ly-info信息，制造free trial...')
    del_redis_ly_info(uid)
    print('已完成...重新登录即有free-tral\n')


# 设置up640_ft_at 时间，让free_trail结束时间提前
def set_redis_updata_time(uid):
    ly_info = get_redis_ly_info(uid)
    print('调整free-trail时间')
    updata_time = ly_info['up640_ft_at']
    new_time = int(updata_time) - 43140
    # set_redis_updata_time(new_time, uid)
    r.hset("{%s}:c:ly:info" % uid, "up640_ft_at", str(new_time))
    print('已完成...等待客户端自动拉取ly-info信息刷新\n')


def has_lucky_draw(user_token):
    url = 'https://dev.apiteamn.com/api-getway/cards/likes-you/info'
    params = {'check_upgrade': 0, 'gmt_offset': 28800}
    user_token = "Bearer " + user_token
    header = {"Authorization": user_token}
    r = requests.get(url=url, params=params, headers=header, cert=woop)
    # print(r.json())
    return r.json()


def lucky_draw(user_token):
    url = 'https://dev.apiteamn.com/api-getway/cards/likes-you/lucky'
    body = {
        "last_user_id": "61246f78e5d21dbf9a5e49cc",
        "gmt_offset": 28800
    }
    user_token = "Bearer " + user_token
    header = {"Authorization": user_token}
    r = requests.post(url=url, data=json.dumps(body), headers=header, cert=woop)
    # print(r.json())
    return r.json()


# 检查liked-info详细信息
def step0_get_liked_info(nas_token, uid):
    liked_list = (r.zrangebyscore('{%s}:c:c:s:liked' % uid, min=float('-inf'), max=float('inf'), withscores=True))
    print('获取liked详细数据...   共有 %s liked数据' % len(liked_list))
    for i in range(0, len(liked_list)):
        user = liked_list[i]
        name = get_user_dispalyname(nas_token, user[0])
        time = str(user[1])
        if user[1] < 0:
            if time[:4] == '-9.2':
                print("{} ({})于{} 被block或者被ban，delete或者你删除了他,不会出现在likes you列表里'".format(name, user[0], time))
            else:
                print('与 {} ({})于{} 形成match'.format(name, user[0], time))
        else:
            print('{} ({})于{} 单向like了你'.format(name, user[0], time))
    print('已完成...\n')


def step1_create_free_trail(uid, user_token):
    del_ly_info(uid)
    who_like_me_read(user_token)


def step2_free_trail_over(uid):
    set_redis_updata_time(uid)


def step3_add_lucky_draw(uid):
    """
    HSET "{611c8b87cde406bab071975e}:c:ly:info" "had_draw" "T"
    HSET "{611c8b87cde406bab071975e}:c:ly:info" "drawn_at" "1634786923"（时间戳为前一天）
    """
    print('增加抽奖次数')
    r.hset("{%s}:c:ly:info" % uid, "had_draw", "T")
    r.hset("{%s}:c:ly:info" % uid, "drawn_at", "1634786923")
    print('已完成...等待客户端自动拉取刷新\n')


server = SSHTunnelForwarder(
    ssh_address_or_host=(host_jump, 22),  # ssh地址
    ssh_username='ubuntu',
    ssh_pkey=ssh_pkey,
    remote_bind_address=(host_redis, 6379)
)
server.start()

r = redis.Redis(host='localhost', port=server.local_bind_port, decode_responses=True)
print(r, '  redis 连接成功...\n')

if __name__ == '__main__':
    user_info = login('johnny770@gmail.com', 'johnny')
    uid = user_info['data']['user']['user_id']
    user_token = user_info['data']['token']
    nas_token = get_nas_token()

    step0_get_liked_info(nas_token, uid)
    # step1_create_free_trail(uid, user_token)

    # step2_free_trail_over(uid)

    # step3_add_lucky_draw(uid)

    # server.close()

    #  # 测试抽奖随机不会抽到传递的参数
    #
    # for i in range(0, 100):
    #     step3_add_lucky_draw(uid)
    #     res = has_lucky_draw(user_token)
    #
    #     if res['data']['has_lucky_draw'] == True:
    #         print('存在抽奖机会')
    #         lucky_Card = lucky_draw(user_token)
    #         sleep(1)
    #
    #         if lucky_Card['data']['type'] == 1:
    #             print('VIP折扣卡')
    #             continue
    #         if lucky_Card['data']['type'] == 2:
    #             print(lucky_Card['data']['user']['id'])
    #             if lucky_Card['data']['user']['id'] == "61246f78e5d21dbf9a5e49cc":
    #                 print('抽到重复卡片')
    #                 break
    #     else:
    #         print('无抽奖机会')
    #         step3_add_lucky_draw(uid)
    #     sleep(1)
