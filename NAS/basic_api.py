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


class basic_API:
    # nas后台登录
    def get_nas_token(self):
        url = "https://dev-nas.apiteamn.com/api/login"
        body = {"username": "admin",
                "password": "WP-nas2018"}
        r = requests.post(url=url, data=json.dumps(body), cert=nas)
        return r.json()['data']['token']

    # 生产站后台登录！！！！！！！注意
    def get_prod_token(self):
        url = "https://nas.apiteamn.com/api/login"
        body = {"username": "john",
                "password": "c2gU.yYZLh"}
        r = requests.post(url=url, data=json.dumps(body), cert=nas)
        return r.json()['data']['token']

    # 通过后台搜索，获取最新用户johnny*  的display_name
    def get_user_dispalyname(self, nas_token):
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
        nas_token = "Bearer " + nas_token
        header = {"Authorization": nas_token}
        r = requests.post(url=url, data=json.dumps(body), headers=header, cert=nas)
        return r.json()['data']['profiles'][0]['display_name'][6:]

    # 上传image,获取image的url /api-getway/image
    def image(self, file):
        url = "https://dev.apiteamn.com/api-getway/image"
        with open("/Users/pof/PycharmProjects/workfast/NAS/image/" + file, 'rb')as f:
            pic = {"image": (file, f.read(), "image/jpg")}
        body = {}
        r = requests.post(url=url, data=body, files=pic, cert=woop)
        return r.json()['data']['url']

    # 注册接口，需要传递johnny * 名字和 图片的url
    # 图片url通过 image接口获取
    def sign_up(self, number, image_url):
        number = int(number) + 1
        url = "https://dev.apiteamn.com/api-getway/signup"
        user_name = "johnny" + str(number)  # username 是 johnny+number：johnny515
        password = md5(("johnny" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
        body = {
            "platform_id": user_name + "@gmail.com",
            "platform": 0,
            "token": password,
            "device": {
                "device_id": "device_" + str(user_name),
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
                "gender": random.randint(1, 2),
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

    #  获取图片的实际url
    def get_pic_url(self, img_uri):
        encrypt_src_data = json.dumps({"bucket": "wooplus-stage-img", "key": img_uri})
        encrypt_data = str(encrypt_src_data).encode('utf-8')
        img_uri_encrypted = base64.b64encode(encrypt_data)
        portrait_url = 'https://image.apiteamn.com/' + img_uri_encrypted.decode('utf-8')
        return portrait_url

    # 获取用户状态
    def get_status(self, status, sta):
        list = ["normal", " ", " ", " ", "ban", "delete", "MP-Delete"]
        sta = list[status - 1]
        return sta

    def get_ban_accounts(self, nas_token):
        url = "https://dev-nas.apiteamn.com/api/profile/search"
        nas_token = "Bearer " + nas_token
        header = {"Authorization": nas_token}
        body = {"condition":{"tags":[],"gender":3,"min_age":None,"max_age":None,"status":"5"},"page":1}
        r = requests.post(url=url, headers=header,data=json.dumps(body), cert=nas)

        accounts = r.json()['data']['profiles']
        ban_accouts = []
        for i in range(0, len(accounts)):
            ban_accouts.append(accounts[i]['id'])
        return ban_accouts

    # 获取关联账号
    def get_shared_account(self, ban_id, env):
        if env == 'prod':
            nas_token = basic_API.get_prod_token(self)
            url = "https://nas.apiteamn.com/api/profile/" + ban_id + "/shared_account"
        else:
            nas_token = basic_API.get_nas_token(self)
            url = "https://dev-nas.apiteamn.com/api/profile/" + ban_id + "/shared_account"
        nas_token = "Bearer " + nas_token
        header = {"Authorization": nas_token}
        r = requests.get(url=url, headers=header, cert=nas)
        account = r.json()['data']['accounts']
        accounts = []
        print("关联账号有 " + str(len(account)) + " 个")
        for i in range(0, len(account)):
            if r.json()['data']['accounts'][i]['status'] == 5:
                accounts.append(account[i]['id'])
        print("其中被状态为ban的有" + str(len(accounts)) + " 个,将对接下来的账号进行恢复normal")
        return accounts

    # make_normal 将被ban的账号恢复normal
    def make_normal(self, accounts, nas_token):
        # if env == 'prod':
        #     nas_token = basic_API.get_prod_token(self)
        #     uri = "https://nas.apiteamn.com/api/user/"
        # else:
        #     nas_token = basic_API.get_nas_token(self)
        #     uri = "https://dev-nas.apiteamn.com/api/user/"
        uri = "https://dev-nas.apiteamn.com/api/user/"
        nas_token = "Bearer " + nas_token
        header = {"Authorization": nas_token}
        body = {
            'current_status': 5,
            'reason': None
        }
        for uid in accounts:
            url = uri + uid + "/1"
            data = json.dumps(body)
            try:
                r = requests.post(url=url, data=data, headers=header, cert=nas)
                print(r.json())
            except:
                print(uid, data)
        return None

    # 创建视频id
    def create_video_id(self, token):
        url = "https://dev-nas.apiteamn.com/api-getway/user/create-auth-video"
        token = "Bearer " + token
        headers = {
            'App-Version': 60200,
            "Authorization": token
        }
        r = requests.post(url, headers=headers, cert=woop)
        return r.json()['data']['video_id']

    # upload视频
    def upload_auth_video(self, video, video_id, token):
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
        r = requests.post(url=url, data=json.dumps(body), files=video, headers=headers, cert=woop)
        return r.json()

    # 验证上传完成
    def complete_video(self, video_id, token):
        token = "Bearer " + token
        url = "https://dev-nas.apiteamn.com/api-getway/user/complete-auth-video"
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
        r = requests.post(url=url, data=json.dumps(body), headers=headers, cert=woop)
        return r.json()

    # 更改仅更换主图的用户状态
    def change_photostatus(self, user_id, auth, raw_url, action, recognition):
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

    def slide_like(self, auth_token, uid):
        url = "https://dev.apiteamn.com/api-getway/cards/slide"
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        body = {
            "liked": [uid]
        }
        r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
        return r.json()

    def get_latest_likeList(self, auth_token):
        url = "https://dev.apiteamn.com/api-getway/cards/like-list"
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        r = requests.get(url=url, headers=header, cert=woop)
        return r.json()['data']['list'][0]['profile']['id']

    def get_who_likeme(self, auth_token):
        url = "https://dev.apiteamn.com/api-getway/cards/who-liked-me"
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        r = requests.get(url=url, headers=header, cert=woop)
        return r.json()['data']['list'][0]['profile']['id']

    def block(self, auth_token, user_id):
        url = "https://dev.apiteamn.com/api-getway/user/block/add"
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        body = {
            "target_id": user_id
        }
        temp = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
        url2 = "https://dev.apiteamn.com/api-getway/user/block/list"
        r = requests.get(url=url2, headers=header, cert=woop)
        return r.json()['data']['block_list'][0]['user']['user_id']

    def block_delete(self, auth_token, user_id):
        url = "https://dev.apiteamn.com/api-getway/user/block/delete"
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        body = {
            "target_id": user_id
        }
        r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
        return r.json()['message']

    def send_moment(self, auth_token):
        url = "https://dev.apiteamn.com/api-getway/moment"
        body = {
            "kind": 101,
            "location": {
                "lat": 30.5971505,
                "lon": 104.0608851
            },
            "address": "Chengdu Shi, Sichuan Sheng, China"
        }
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
        return [r.json()['data']['id'], r.json()['message']]

    def like_moment(self, auth_token, moment_id, target_author):
        url = "https://dev.apiteamn.com/api-getway/moment/like"
        body = {
                "moment_id": moment_id,
                "media_id": moment_id,
                "target_author": {
                    "id": target_author[0],
                    "name": target_author[1],
                    "gender": target_author[2]
                }
        }
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
        print(r.json())
        return r.json()['message']

    def comment_moment(self, auth_token, moment_id, target_author):
        url = "https://dev.apiteamn.com/api-getway/moment/comment"
        body = {
                "moment_id": moment_id,
                "media_id": moment_id,  # 一级评论id
                "content": "👿我，秦始皇，打钱╭(╯ε╰)╮",
                "target_author": {
                    "id": target_author[0],
                    "name": target_author[1],
                    "gender": target_author[2],
                    "avatar": None,
                    "deep_link": None
                }
        }
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
        print(r.json())
        return [r.json()['data']['id'], r.json()['message']]

    def delete_moment(self, auth_token, moment_id):
        url = "https://dev.apiteamn.com/api-getway/moment/" + moment_id
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        r = requests.delete(url=url, headers=header, cert=woop)
        return r.json()['message']

    def delete_comment(self, auth_token, comment_id, moment_id):
        url = "https://dev.apiteamn.com/api-getway/moment/comment" + comment_id
        auth_token = "Bearer " + auth_token
        header = {"Authorization": auth_token}
        body = {
                "target_id": comment_id,
                "moment_id": moment_id}
        r = requests.delete(url=url, headers=header, data=json.dumps(body), cert=woop)
        return r.json()['message']

    def upload_video(self, auth_token):
        with open("/Users/pof/PycharmProjects/workfast/NAS/image/video.mp4", 'rb')as f:
            video = {"video": (f.read(), "mp4")}
        video_file = video
        auth_token = "Bearer " + auth_token
        video_id = basic_API.create_video_id(self, auth_token)
        basic_API.upload_auth_video(self, video_file, video_id, auth_token)
        basic_API.complete_video(self, video_id, auth_token)


# 获取批量用户info,将name，id，token写入文件
def get_many_userinfo(arry):
    url = "https://dev.apiteamn.com/api-getway/login"
    password = md5(("johnny" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
    user_names = []
    tokens = []
    names = []
    ids = []
    for i in range(arry[0], arry[1]):
        user_names.append('johnny_autotets' + str(i))
    for user_name in user_names:
        user_name = user_name + "@gmail.com"
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
                "device_token": "{{device_token}}",
                "vpn_on": True,
                "app_build": 60200
            }
        }
        r = requests.post(url, json.dumps(body), cert=woop)
        print(r.json())
        token = r.json()['data']['token']
        name = r.json()['data']['user']['display_name']
        _id = r.json()['data']['user']['user_id']
        # ids.append(_id)
        # names.append(name)
        auth_token = "Bearer " + token
        # tokens.append(auth_token)
        with open("../user_data/user_name.txt", 'a') as f1:
            f1.write(name + '\n')
        with open("../user_data/user_id.txt", 'a') as f2:
            f2.write(_id + '\n')
        with open("../user_data/user_token.txt", 'a') as f3:
            f3.write(auth_token + '\n')
    # return [names, ids, tokens]


# 如果token过期了可以直接只保存token
def refresh_token(num):
    url = "https://dev.apiteamn.com/api-getway/login"
    password = md5(("johnny" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
    user_names = []
    with open("../user_data/user_token.txt", 'w') as clear_f:
        clear_f.write("")
    for i in range(0, num):
        user_names.append('johnny_autotets' + str(i))
    for user_name in user_names:
        user_name = user_name + "@gmail.com"
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
                "device_token": "{{device_token}}",
                "vpn_on": True,
                "app_build": 60300
            }
        }
        r = requests.post(url, json.dumps(body), cert=woop)
        print(r.json())
        token = r.json()['data']['token']
        auth_token = "Bearer " + token
        with open("../user_data/user_token.txt", 'a') as f3:
            f3.write(auth_token + '\n')


# 获取profile并修改后台状态
def get_profile():
    with open('../user_data/user_token.txt', 'r') as f:
        tokens = f.readlines()
    with open('../user_data/user_id.txt', 'r') as f2:
        ids = f2.readlines()
    nas_token = basic_API().get_nas_token()
    for i in range(0, 101):
        auth_token = tokens[i].replace("\n", "")
        uid = ids[i].replace("\n", "")
        header = {"Authorization": auth_token}
        url = "https://dev.apiteamn.com/api-getway/user/profile/" + uid
        r = requests.get(url=url, headers=header, cert=woop)
        status = r.json()['data']['profile']['album']['portrait']['status']
        raw_url = r.json()['data']['profile']['album']['portrait']['url']
        if status == 1:
            basic_API().change_photostatus(uid, nas_token, raw_url, 0, None)
            print(r.json()['data']['profile']['basic']['display_name'])


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
        r = requests.post(url="https://dev.apiteamn.com/api-getway/cards/slide", headers=header, data=json.dumps(bodys), cert=woop)
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
        r = requests.post(url="https://dev.apiteamn.com/api-getway/conversation/create", headers=header, data=json.dumps(bodys), cert=woop)
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

# md5加密
def get_password():
    password = md5(("nancyy" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
    print(password)



if __name__ == "__main__":
    ba = basic_API()
    nas_token = ba.get_nas_token()
    # username = ba.get_user_dispalyname(nas_token)
    # print(username)

    # with open('../user_data/user_token.txt', 'w') as f:
    #     f.write("")

    # refresh_token(20)

    # r = ba.block("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjIjoxNjMwNDY0NjkxLCJleHAiOjE2MzEwNjk0OTEsImlkIjoiNjEyZGZlZjkxY2UxMmE5OWQxZjc0NWU0IiwidiI6MX0.MvQIsqhUo3W6nkwZaQsr_F7P9kmCjztzw3VzfKhoFRA", "612f4026248c19b3c955178a")
    # x = ba.send_moment("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjIjoxNjMxNjA5NTU0LCJleHAiOjE2MzIyMTQzNTQsImlkIjoiNjE0MDVkNzQ2M2RmYWZjYmIzZTBkNjdmIiwidiI6MX0.NBy0M71t5tUg1f7aPrwc140VVPWkY4wKCyBlhapfFmw")
    # print(x)
    # #恢复ban
    # ban_id = "6170e6c01ff0ceb7dafaa7b6"  # 6079336ad0845d2d5d603e2a johnnyR
    # accounts = ba.get_shared_account(ban_id, 'test')
    # print(accounts)
    # ba.make_normal(accounts, 'test')
    for i in range(0, 50):
        ban_ids = ba.get_ban_accounts(nas_token)
        ba.make_normal(ban_ids, nas_token)



    # belike_many("6131efe2c3842e0bd07e9aad", [0, 10])  # 0-100可用
    # sayHi_many("6131efe2c3842e0bd07e9aad", [0, 3])
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
    # refresh_token()
