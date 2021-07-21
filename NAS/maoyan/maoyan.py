import json
from hashlib import md5

import requests
import urllib3
from NAS.basic_api import basic_API

nas_cert = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-cert.pem"
nas_key = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-key.pem"
woop_cert = "/Users/pof/PycharmProjects/workfast/check_status/client.cert.pem"
woop_key = "/Users/pof/PycharmProjects/workfast/check_status/client.key.nopwd.pem"
nas = (nas_cert, nas_key)
woop = (woop_cert, woop_key)
urllib3.disable_warnings()




def test_signup_approve():
    ba = basic_API()
    nas_token = ba.get_nas_token()  # nas 登录
    num = ba.get_user_dispalyname(nas_token)  # 搜索最新的name序号
    raw_url = ba.image("01.jpeg")  # 上传图片
    signup = ba.sign_up(int(num)+1, raw_url)  # 注册
    uid = signup['data']['user']['user_id']  # 获取用户id
    ba.change_photostatus(uid, nas_token, raw_url, 0, None)  # 后台approve
