import json
import requests
import urllib3

cert = "/Users/pof/PycharmProjects/workfast/check_status/nas-client.pem"
pwd = "878M6yN667"
cert = (cert, pwd)
urllib3.disable_warnings()


def login(env):
    if env == 0:
        url = "https://dev-nas.apiteamn.com/api/login"
        body = {"username": "admin",
                "password": "WP-nas2018"}
    else:
        url = "https://nas.apiteamn.com/api/login"
        body = {"username": "john",
                "password": "c2gU.yYZLh"}

    r = requests.post(url=url, data=json.dumps(body), verify=False)
    return r.json()


def get_token(data):
    return data['data']['token']

def searchby_id(env, uid, token):
    """
    通过user_id来查看后台profile数据
    :param env:环境判断生产还是测试  0：测试   1：生产
    :param uid: 用户的id，例：6080d9ed4c06f1a6aae4af50
    :param token: 登录后台使用的token
    :return: 返回页面json格式数据
    """
    if env == 0:
        url = "https://dev-nas.apiteamn.com/api/profile/"
    else:
        url = "https://nas.apiteamn.com/api/profile/"
    url = url + uid
    token = "Bearer " + token
    header = {"Authorization": token}
    r= requests.session().get(url=url, headers=header, verify=False)
    return r.json()


def get_status(status, sta):
    list = ["normal", " ", " ", " ", "ban", "delete", "MP-Delete"]
    sta = list[status-1]
    return sta


if __name__ == "__main__":
    env = 1  # 0:测试站  1：生产
    data = login(env)
    token = get_token(data)
    uid = input("输入用户id(空格隔开):").split()
    print(uid)
    for i in uid:
        r = searchby_id(env, i, token)
        status = r["data"]["profile"]["status"]
        name = r["data"]["profile"]["display_name"]
        stas = get_status(status, sta=" ")
        print(f"{i}   {name}   状态为 {stas}")
    # 6080d9ed4c06f1a6aae4af50 6077fbbb4c06f1a6aae4af28
    # r = search("johnny85", token)
    # print(r.text)
