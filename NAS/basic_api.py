import base64
import json
from hashlib import md5
from time import sleep

import requests
import urllib3

nas_cert = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-cert.pem"
nas_key = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-key.pem"
woop_cert = "/Users/pof/PycharmProjects/workfast/check_status/client.cert.pem"
woop_key = "/Users/pof/PycharmProjects/workfast/check_status/client.key.nopwd.pem"
nas = (nas_cert, nas_key)
woop = (woop_cert, woop_key)
urllib3.disable_warnings()

class basic_API:

    def login(self):
        url = "https://dev-nas.apiteamn.com/api/login"
        body = {"username": "admin",
                "password": "WP-nas2018"}
        r = requests.post(url=url, data=json.dumps(body), cert=nas)
        return r.json()


    def get_token(self, data):
        return data['data']['token']

    # 获取用户
    def get_number(self, token):
        url = "https://dev-nas.apiteamn.com/api/profile/search"
        body = {
            "condition": {
                "tags": [],
                "text": "johnny",
                "gender": 3,
                "min_age": None,
                "max_age": None,
                "status": 0
            },
            "page": 1
    }
        token = "Bearer " + token
        header = {"Authorization": token}
        r = requests.post(url=url, data=json.dumps(body), headers=header, cert=nas)
        return r.json()['data']['profiles'][0]['display_name'][6:]


    def image(self, file):
        url = "https://dev.apiteamn.com/api-getway/image"
        with open("/Users/pof/PycharmProjects/workfast/NAS/image/" + file, 'rb')as f:
            pic = {"image": ("01.jpeg", f.read(), "image/jpeg")}
        body = {}
        r = requests.post(url=url, data=body, files=pic, cert=woop)
        return r.json()['data']['url']


    def sign_up(self, number, image_url):
        url = "https://dev.apiteamn.com/api-getway/signup"
        user_name = "johnny" + str(number)
        password = md5(("johnny" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
        body = {
            "platform_id": user_name + "@gmail.com",
            "platform": 0,
            "token": password,
            "device": {
                "device_id": user_name,
                "device_type": 1,
                "os_version": "6.2.0",
                "device_token": "000000",
                "vpn_on": False,
                "machine": "iphone12.5",
                "language": "en-CN;q=1, zh-Hans-CN;q=0.9, ja-CN;q=0.8",
                "app_build": 60200
            },
            "basic": {
                "display_name": user_name,
                "gender": 1,
                "birthday": "1990-04-09",
                "store": 10,
                "time_zone": "CST",
                "gmt_offset": 28800
            },
            "avatar": {
                "image_name": image_url,
                "width": 1080,
                "height": 1080,
                "face_number": 1
            }
        }
        r = requests.post(url=url, data=json.dumps(body), cert=woop)
        return r.json()


    def get_pic_url(self, img_uri):
        encrypt_src_data = json.dumps({"bucket": "wooplus-stage-img", "key": img_uri})
        encrypt_data = str(encrypt_src_data).encode('utf-8')
        img_uri_encrypted = base64.b64encode(encrypt_data)
        portrait_url = 'https://image.apiteamn.com/' + img_uri_encrypted.decode('utf-8')
        # print(portrait_url)
        return portrait_url


    def get_status(self, status, sta):
        list = ["normal", " ", " ", " ", "ban", "delete", "MP-Delete"]
        sta = list[status-1]
        return sta

    def change_status(self, user_id, auth, raw_url, action, recognition):
        url = "https://dev-nas.apiteamn.com/api/portrait_next/handle"
        picture_url = basic_API().get_pic_url(raw_url)
        auth_token = "Bearer " + auth
        header = {"Authorization": auth_token}
        body = {
            "user_id": user_id,
            "album": {
                "portrait_next": {
                    "ver": 0,
                    "src": 0,
                    "pic": None
                },
                "portrait": {
                    "url": picture_url,
                    "raw_url": raw_url,
                    "status": 1,
                    "face_number": 1,
                    "height": 1080,
                    "width": 1080,
                    "created_at": 1622367975000,
                    "handled_by": {
                        "admin": "admin"
                    }
                }
            },
            "action": action,  # action:0 approve ; 1: delete
            "recognition": recognition  # 2030: feel like scam
            # feel like scam(1,2030)   approve(0,null)   porn(1,2040)  no face(1,1010)
            # under age(1,1040)  wrong gender(1,1030)   multi face(1,1020)
            # contact(1,2050)
    }
        r = requests.post(url=url, headers=header, data=json.dumps(body), cert=nas)

if __name__ == "__main__":
    ba = basic_API()
    data = ba.login()  # 登录
    # print(ba.get_pic_url("2021/05/19/60a47dadc906878e418a5fdb"))
    token = ba.get_token(data)
    pic_url = ba.image("01.jpeg")
    number = ba.get_number(token)
    res = ba.sign_up(int(number)+1, pic_url)
    uid = res['data']['user']['user_id']
    authorization = res['data']['token']
    print(res)
    sleep(2)
    ba.change_status(uid, authorization, pic_url, 1, 2030)

    # pic_url = "2021/05/30/60b35edcc906878e418a636c"
    # uid = "60b35ee720112023295d1465"
    # authorization = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjIjoxNjIyNDQ1Njc5LCJleHAiOjE2MjMwNTA0NzksImlkIjoiNjBiMzVlZTcyMDExMjAyMzI5NWQxNDY1IiwidiI6MX0.I1veImNeht9_PJDSeD2K63Mp6hchWhWhtjqv5BOGmV0"
    # ba.change_status(uid, authorization, pic_url, 1, 1020)

