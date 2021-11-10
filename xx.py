# import paramiko
import json
from hashlib import md5

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

# private_key = paramiko.RSAKey.from_private_key_file(ssh_pkey)
# paramiko.pkey.PKey()

server = SSHTunnelForwarder(
    ssh_address_or_host=(host_jump, 22),  # ssh地址
    ssh_username='ubuntu',
    ssh_pkey=ssh_pkey,
    remote_bind_address=(host_redis, 6379)
    )
server.start()


def get_nas_token():
    url = "https://dev-nas.apiteamn.com/api/login"
    body = {"username": "admin",
            "password": "WP-nas2018"}
    r = requests.post(url=url, data=json.dumps(body), cert=nas)
    return r.json()['data']['token']


def get_user_dispalyname(nas_token, uid):
    url = "https://dev-nas.apiteamn.com/api/profile/"+uid
    nas_token = "Bearer " + nas_token
    header = {"Authorization": nas_token}
    r = requests.get(url=url, headers=header, cert=nas)
    return r.json()['data']['profile']['display_name']


def who_like_me_read(token):
    url = "https://dev.apiteamn.com/api-getway/cards/who-liked-me/read"
    body = {
        "last_created_at": 1631525177000,
        "gmt_offset": 28800
    }
    header = {"Authorization": token}
    requests.post(url=url, data=json.dumps(body), header=header)


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
    r = requests.post(url, json.dumps(body), cert=woop)
    print(r.json())


r = redis.Redis(host='localhost', port=server.local_bind_port, decode_responses=True)
print(r)
# print(r.zrangebyscore('{6184929b2831f986094cb076}:c:c:s:liked', min=float('-inf'), max=float('inf'), withscores=True))
# liked_list = r.zrangebyscore('{6184929b2831f986094cb076}:c:c:s:liked', min=-float('inf'), max=float('inf'), withscores=True)
# print(len(liked_list))

# 删除曝光数据
# print(r.delete('{613f1938d55d2105ec445bd3}:c:ly:info'))
login('johnny717@gmail.com', 'johnny')

"""
token = get_nas_token()

for i in range(0, len(liked_list)):
    if liked_list[i][1] < 0:
        print(liked_list[i][0])
        time = str(liked_list[i][1])
        if time[:4] == '-9.2':
            name = get_user_dispalyname(token, liked_list[i][0])
            print("{}({}) 被block或者被ban，delete或者你删除了他'".format(name, liked_list[i][0]))
        else:
            print(liked_list[i][0]+' match')
    else:
        print(liked_list[i][0]+'  like了你')

print('ok')
server.close()
"""