# 批量获取用户id
import json
from hashlib import md5

import requests
import urllib3

nas_cert = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-cert.pem"
nas_key = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-key.pem"
woop_cert = "/Users/pof/PycharmProjects/workfast/check_status/client.cert.pem"
woop_key = "/Users/pof/PycharmProjects/workfast/check_status/client.key.nopwd.pem"
nas = (nas_cert, nas_key)
woop = (woop_cert, woop_key)
urllib3.disable_warnings()


def get_nas_token():
    url = "https://dev-nas.apiteamn.com/api/login"
    body = {"username": "admin",
            "password": "WP-nas2018"}
    r = requests.post(url=url, data=json.dumps(body), cert=nas)
    return r.json()['data']['token']


def getuserid_many():
    url = "https://dev.apiteamn.com/api-getway/login"
    password = md5(("johnny" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
    user_names = []
    user_ids = []
    for i in range(300, 320):
        user_names.append('johnny' + str(i))
    for user_name in user_names:
        user_name = user_name + "@gmail.com"
        body = {
                "platform_id": user_name,
                "platform": 0,
                "token": password,
                "device": {
                    "device_id": "johnny9999",
                    "device_type": 3,
                    "machine": "postman",
                    "language": "en-CN;q=1, zh-Hans-CN;q=0.9, ja-CN;q=0.8",
                    "os_version": "1.0.0",
                    "device_token": "{{device_token}}",
                    "vpn_on": True,
                    "app_build": 60200
                }
        }
        r = requests.post(url, json.dumps(body), cert=woop)
        print(r.json())
        user_id = r.json()['data']['user']['user_id']
        user_ids.append(user_id)
    return user_ids

# 批量block
def block_many(user_ids):
    url = "https://dev.apiteamn.com/api-getway/user/block/add"
    auth_token = "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjIjoxNjI1NjIyODQ2LCJleHAiOjE2MjYyMjc2NDYsImlkIjoiNjBjOTYyZmJlNTQyY2EyMThlMDY3NDUxIiwidiI6MX0.YSadl-HyGMIT5aLGgtCytL5oIx7DHG2vIDPIlkiAEIw"
    header = {"Authorization": auth_token}
    for user_id in user_ids:
        body = {
            "target_id": user_id
        }
        r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
        print(r.json())


if __name__ == "__main__":
    token = get_nas_token()  # 登录
    user_ids = getuserid_many()
    block_many(user_ids)
