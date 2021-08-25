import base64
import json
import random
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


class BasicApi:
    """
        desc: nas后台登录
        params: env,使用环境，env=='prod' 表示生产站；其他表示测试站
        use: get_nas_token('prod')
        return： nas登录获取的token
    """

    def get_nas_token(self, env):
        if env == 'prod':
            url = "https://nas.apiteamn.com/api/login"
            body = {"username": "john",
                    "password": "c2gU.yYZLh"}
        else:
            url = "https://dev-nas.apiteamn.com/api/login"
            body = {"username": "admin",
                    "password": "WP-nas2018"}
        r = requests.post(url=url, data=json.dumps(body), cert=nas)
        return r.json()['data']['token']

    """
        desc: 上传图片接口，但不保存到profile
        params: file：图片名，放在/Users/pof/PycharmProjects/workfast/NAS/image/ 下
                env:环境
        use: url = image('01.jpeg')
        return： 获取的image的url值
    """

    def image(self, env, file):
        if env == 'prod':
            url = "https://apiteamn.com/api-getway/image"
        else:
            url = "https://dev.apiteamn.com/api-getway/image"
        with open("/Users/pof/PycharmProjects/workfast/NAS/image/" + file, 'rb')as f:
            pic = {"image": ("01.jpeg", f.read(), "image/jpeg")}
        body = {}
        r = requests.post(url=url, data=body, files=pic, cert=woop)
        return r.json()['data']['url']

    """
        desc: 注册接口
        params: env：环境
                username:用户名称，同样也是用户邮箱@的前半部分
                password:密码
                gender：性别 1:男；2：女
        use: user = sign_up('prod',johnny570,johnny,1,'01.jpeg')
        return： 获取注册后user信息
    """

    def sign_up(self, env, username, password, gender, pic):
        if env == 'prod':
            url = "https://dev.apiteamn.com/api-getway/signup"
        else:
            url = "https://apiteamn.com/api-getway/signup"
        image_url = BasicApi().image(env, pic)
        password = md5((password + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
        body = {
            "platform_id": str(username) + "@gmail.com",
            "platform": 0,
            "token": password,
            "device": {
                "device_id": "device_" + str(username),
                "device_type": 1,
                "os_version": "6.2.0",
                "device_token": "000000",
                "vpn_on": False,
                "machine": "iphone12.5",
                "language": "en-CN;q=1, zh-Hans-CN;q=0.9, ja-CN;q=0.8",
                "app_build": 60200
            },
            "basic": {
                "display_name": username,
                "gender": gender,
                "birthday": "1997-05-07",
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

    """
        desc: 获取图片实际的url值
        params: img_url：通过image()接口上传的图片url
                env：环境；env=='prod' 表示生产站，其他表示测试站
        use: get_pic_url(img_url,'prod')
        return： base64编码过后实际的url
    """

    def get_pic_url(self, img_uri, env):
        if env == 'prod':
            bucket = "wooplus-stage-img"
        else:
            bucket = "wooplus-prod-img"
        encrypt_src_data = json.dumps({"bucket": bucket, "key": img_uri})
        encrypt_data = str(encrypt_src_data).encode('utf-8')
        img_uri_encrypted = base64.b64encode(encrypt_data)
        portrait_url = 'https://image.apiteamn.com/' + img_uri_encrypted.decode('utf-8')
        return portrait_url

    # 创建视频id
    def create_video_id(self, token):
        url = "https://dev-nas.apiteamn.com/api-getway/user/create-auth-video"
        token = "Bearer " + token
        headers = {
            'App-Version': 60200,
            "Authorization": token
        }
        r = requests.post(url, headers=headers)
        return r.json()['data']['video_id']

    # upload视频
    def upload_video(self, video, video_id, token):
        url = "https://dev-nas.apiteamn.com/api-getway/user/upload-auth-video"
        token = "Bearer " + token
        headers = {
            'App-Version': 60200,
            "Authorization": token
        }
        body = {
            "video_id": video_id,
            "part_number": 1,
            "video_file": video
        }
        r = requests.post(url=url, data=json.dumps(body), files=video, headers=headers)
        return r.json()

    # 验证上传完成
    def complete_video(self, video_id, token):
        body = {
            "video_id": video_id,
            "part_info": [
                {
                    "part_number": 1,
                    "part_size": 1519868
                }
            ],
            "cover_at": 4000,
            "duration": 10,
            "action_confirm": False  # AI4
        }
        headers = {
            'App-Version': 60200,
            "Authorization": token
        }
        return False

    """
        desc: 登录接口
        params: uname:用户名
                password：密码
        use: login(johnny670@gmail.com,johnny)
        return： base64编码过后实际的url
    """
    def login(self, uname, password):
        url = "https://dev-nas.apiteamn.com/api-getway/login"
        body = {
            "platform_id": uname + '@gmail.com',
            "platform": 0,
            "token": password,
            "device": {
                "device_id": "device_"+str(uname),
                "device_type": 3,
                "machine": "iphone7",
                "language": "en-CN;q=1, zh-Hans-CN;q=0.9, ja-CN;q=0.8",
                "os_version": "1.0.0",
                "device_token": "000000",
                "vpn_on": False,
                "app_build": 60200
            }
        }
        r = requests.post(url, json.dumps(body), cert=woop)

    """
        desc: 批量创建会话
        params: uid:被会话的人的id
                number：需要建立会话的条数。通过读取token文档，选取auto_test进行建立
                type: 会话建立类型 2-Say Hi会话；4-Vip会话
        use: create_chat('6124704ae5d21dbf9a5e49cf'，50)
        return： null
    """
    def create_chat(self, uid, number, chat_type):
        with open('../user_data/user_token.txt', 'r') as f:
            tokens = f.readlines()
        url = "https://dev.apiteamn.com/api-getway/conversation/create"
        for i in range(0, number):
            auth_token = tokens[i].replace("\n", "")
            header = {"Authorization": auth_token}
            body = {
                "target_id": uid,
                "type": chat_type,  # 2-Say Hi  4-VIP会话
            }
            r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
            print(r.json())

    """
        desc: 批量block
        params: token：需要进行block一堆人的用户token
        use: block_many(eyJhbGciOiJIUzI1NiIsInR5cCI6... ，50)
        return： null
    """
    def block_many(self, token, number):
        url = "https://dev.apiteamn.com/api-getway/user/block/add"
        auth_token = "Bearer " + token
        header = {"Authorization": auth_token}
        with open('../user_data/user_id.txt', 'r') as f:
            ids = f.readlines()
        for i in range(0, number):
            user_id = ids[i].replace("\n", "")
            body = {
                "target_id": user_id
            }
            r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
            print(r.json())


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


# 被批量like
def belike_many(userid, arry):
    with open('../user_data/user_token.txt', 'r') as f:
        tokens = f.readlines()
    with open('../user_data/user_name.txt', 'r') as f2:
        names = f2.readlines()
    for i in range(arry[0], arry[1]):
        auth_token = tokens[i].replace("\n", "")
        name = names[i].replace('\n', '')
        header = {"Authorization": auth_token}
        bodys = {"liked": [userid]}
        r = requests.post(url="https://dev.apiteamn.com/api-getway/cards/slide", headers=header, data=json.dumps(bodys),
                          cert=woop)
        print(f"ok!{name} liked you!")


# 批量say hi
def sayHi_many(uid, arry):
    with open('../user_data/user_token.txt', 'r') as f:
        tokens = f.readlines()
    for i in range(arry[0], arry[1]):
        auth_token = tokens[i].replace("\n", "")
        header = {"Authorization": auth_token}
        bodys = {
            "target_id": uid,
            "type": 2,  # 2-Say Hi  4-VIP会话
        }
        r = requests.post(url="https://dev.apiteamn.com/api-getway/conversation/create", headers=header,
                          data=json.dumps(bodys), cert=woop)
        print(r.json())


# 上传图片
def image(file):
    url = "https://dev.apiteamn.com/api-getway/image"
    with open("/Users/pof/PycharmProjects/workfast/NAS/image/" + file, 'rb')as f:
        pic = {"image": ("01.jpeg", f.read(), "image/jpeg")}
    body = {}
    r = requests.post(url=url, data=body, files=pic, cert=woop)
    return r.json()['data']['url']


# 注册一批账号
def sign_autotest():
    url = "https://dev.apiteamn.com/api-getway/signup"
    password = md5(("johnny" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
    for number in range(80, 101):
        gender = random.randint(1, 2)
        if gender == 1:
            image_url = image("male.jpg")
        else:
            image_url = image("female.jpg")
        user_name = "johnny_autotets" + str(number)  # username 是 johnny+number：johnny515
        body = {
            "platform_id": user_name + "@gmail.com",
            "platform": 0,
            "token": password,
            "device": {
                "device_id": "device_" + str(number),
                "device_type": 1,
                "os_version": "6.2.0",
                "device_token": "000000",
                "vpn_on": False,
                "machine": "iphone12.5",
                "language": "en-CN;q=1, zh-Hans-CN;q=0.9, ja-CN;q=0.8",
                "app_build": 60800
            },
            "basic": {
                "display_name": user_name,
                "gender": gender,
                "birthday": "1997-04-09",
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
        print(r.json())
        # return r.json()


# 注册+approve
def signup_approve():
    ba = basic_API()
    nas_token = ba.get_nas_token()  # nas 登录
    num = ba.get_user_dispalyname(nas_token)  # 搜索最新的name序号
    raw_url = ba.image("01.jpeg")  # 上传图片
    signup = ba.sign_up(int(num) + 1, raw_url)  # 注册
    uid = signup['data']['user']['user_id']  # 获取用户id
    ba.change_photostatus(uid, nas_token, raw_url, 0, None)  # approve
    print("ok")


# 注册+强制认证
def signup_tbv():
    ba = basic_API()
    nas_token = ba.get_nas_token()  # nas 登录
    num = ba.get_user_dispalyname(nas_token)  # 搜索最新的name序号
    raw_url = ba.image("01.jpeg")  # 上传图片
    signup = ba.sign_up(int(num) + 1, raw_url)  # 注册
    uid = signup['data']['user']['user_id']  # 获取用户id
    ba.change_photostatus(uid, nas_token, raw_url, 1, 2030)  # tbv


# 批量注入视频
def authvideo():
    ba = basic_API()
    nas_token = ba.get_nas_token()  # nas 登录


if __name__ == "__main__":
    """
    #恢复ban
    # ba = basic_API()
    # ban_id = "6002698378254500b9eb66d1"  # 6079336ad0845d2d5d603e2a johnnyR
    # accounts = ba.get_shared_account(ban_id)
    # print(accounts)
    # ba.make_normal(accounts)
    """

    # belike_many("6124a7f759f2c5f8651576d8", [0, 10])  # 0-100可用
    # sayHi_many("611dbb20cde406bab071976e", [0, 3])
    # get_profile()

    # with open('../user_data/user_id.txt', 'r') as f:
    #     print(f.readlines())
    #     s = f.readlines()
    #     for r in s:
    #         r.replace("\n", "")
    #     print(s)
    #     for i in range(0, 3):
    #         print(f.readlines()[i])

    # print(sign_autotest())
    # sign_autotest()
