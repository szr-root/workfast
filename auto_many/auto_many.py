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
        pass

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

    """
        desc: 被批量like
        params: userid：被批量like的一群人
                number：需要被like的数量
        use:beliked_many(6124704fe5d21dbf9a5e49d3，50)
        return： null
    """
    def beliked_many(self, userid, number):
        with open('../user_data/user_token.txt', 'r') as f:
            tokens = f.readlines()
        with open('../user_data/user_name.txt', 'r') as f2:
            names = f2.readlines()
        url = "https://dev.apiteamn.com/api-getway/cards/slide"
        for i in range(0, number):
            auth_token = tokens[i].replace("\n", "")
            name = names[i].replace('\n', '')
            header = {"Authorization": auth_token}
            bodys = {"liked": [userid]}
            r = requests.post(url=url, headers=header, data=json.dumps(bodys),
                              cert=woop)
            print(r.json())
            print(f"ok!{name} liked you!")

    """
        desc: 批量点赞moment
        params: number：需要被like的数量
                moment_id，media_id：当前moment则相同，点赞他人评论，则media_id为评论的id
                target_author：作者的id，名字，性别
        use:  ba.moment_like(100, "611f27bf20c513ef91a91b17", "611f27bf20c513ef91a91b17",
                    ["611e1b53935e8dded0b6b2e5", "Ashley2045", 2])
        return： null
    """
    def moment_like(self, number, moment_id, media_id, target_author):
        with open('../user_data/user_token.txt', 'r') as f:
            tokens = f.readlines()
        url = "https://dev.apiteamn.com/api-getway/moment/like"
        body = {
                "moment_id": moment_id,
                "media_id": media_id,
                "target_author": {
                    "id": target_author[0],
                    "name": target_author[1],
                    "gender": target_author[2]
                }
        }
        for i in range(0, number):
            auth_token = tokens[i].replace("\n", "")
            header = {"Authorization": auth_token}
            r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
            print(r.json())

        """
            desc: 评论moment
            params: number：需要被like的数量
                    moment_id，media_id：当前moment则相同，点赞他人评论，则media_id为评论的id
                    target_author：作者的id，名字，性别
            use:  ba.moment_like(100, "611f27bf20c513ef91a91b17", "611f27bf20c513ef91a91b17",
                        ["611e1b53935e8dded0b6b2e5", "Ashley2045", 2])
            return： null
        """
    def comment_moment(self, number, moment_id, media_id, target_author):
        with open('../user_data/user_token.txt', 'r') as f:
            tokens = f.readlines()
        url = "https://dev.apiteamn.com/api-getway/moment/comment"
        body = {
                "moment_id": moment_id,
                "media_id": media_id,  # 一级评论id
                "content": "好耶！",
                "target_author": {
                    "id": target_author[0],
                    "name": target_author[1],
                    "gender": target_author[2],
                    "avatar": None,
                    "deep_link": None
                }
                # "reference": {  # 要at的评论的作者
                #     "author": {
                #         "id": target_author[0],
                #         "name": target_author[1],
                #         "gender": target_author[2]
                #     },
                #     "id": target_author[0],  # 要at的评论id
                #     "content": "好耶"  # 要at的评论内容
                # }
        }
        for i in range(0, number):
            auth_token = tokens[i].replace("\n", "")
            header = {"Authorization": auth_token}
            r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
            print(r.json())
    """
        desc: 快速发送moment
        params: number：需要发送的数量
        use:  send_moment(10)
        return： null
    """
    def send_moment(self, number):
        url = "https://dev.apiteamn.com//api-getway/moment/"
        body = {
            "kind": 101,
            "topic_id": "5e0852a7679ece6f95e231f6",
            "location": {
                "lat": 30.5971505,
                "lon": 104.0608851
            },
            "address": "Chengdu Shi, Sichuan Sheng, China"
        }
        with open('../user_data/user_token.txt', 'r') as f:
            tokens = f.readlines()
        for i in range(0, number):
            token = tokens[i].replace("\n", "")
            header = {"Authorization": token}
            r = requests.post(url=url, headers=header, data=json.dumps(body), cert=woop)
            print(r.json())


if __name__ == "__main__":
    """
    #恢复ban
    # ba = basic_API()
    # ban_id = "6002698378254500b9eb66d1"  # 6079336ad0845d2d5d603e2a johnnyR
    # accounts = ba.get_shared_account(ban_id)
    # print(accounts)
    # ba.make_normal(accounts)
    """
    ba = BasicApi()
    # ba.beliked_many("6125a9aea192feff42662db3", 10)  # 0-100可用
    # ba.create_chat("6125a9aea192feff42662db3", 10, 4)
    # sayHi_many("611dbb20cde406bab071976e", [0, 3])
    # get_profile()
    ba.block_many("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjIjoxNjMwMjk3NzEyLCJleHAiOjE2MzA5MDI1MTIsImlkIjoiNjEyODY1MzEwMThlZWU3ODg1NGU0ZTRlIiwidiI6MX0.bWYouuNXVTV67SQnPmQRFjUzeYOxWKuNfcD2lW_ISao",30)
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

    # ba.moment_like(100, "611f27bf20c513ef91a91b17", "611f27bf20c513ef91a91b17",
    #                ["611e1b53935e8dded0b6b2e5", "Ashley2045", 2])

    # ba.comment_moment(101, "611f27bf20c513ef91a91b17", "611f27bf20c513ef91a91b17",
    #                 ["611e1b53935e8dded0b6b2e5", "Ashley2045", 2])

    # ba.send_moment(20)
