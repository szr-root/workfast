import json

import requests
import urllib3

nas_cert = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-cert.pem"
nas_key = "/Users/pof/PycharmProjects/workfast/check_status/nas-client-key.pem"
woop_cert = "/Users/pof/PycharmProjects/workfast/check_status/client.cert.pem"
woop_key = "/Users/pof/PycharmProjects/workfast/check_status/client.key.nopwd.pem"
nas = (nas_cert, nas_key)
woop = (woop_cert, woop_key)
urllib3.disable_warnings()

accounts = []
accounts_all = []

class basic_API:
    def get_prod_token(self):
        url = "https://nas.apiteamn.com/api/login"
        body = {"username": "john",
                "password": "c2gU.yYZLh"}
        r = requests.post(url=url, data=json.dumps(body), cert=nas)
        return r.json()['data']['token']


    def get_shared_account(self, ban_id):
        nas_token = basic_API.get_prod_token(self)
        url = "https://nas.apiteamn.com/api/profile/" + ban_id + "/shared_account"
        nas_token = "Bearer " + nas_token
        header = {"Authorization": nas_token}
        r = requests.get(url=url, headers=header, cert=nas)
        account = r.json()['data']['accounts']
        print("关联账号有 " + str(len(account)) + " 个")
        for i in range(0, len(account)):
            if r.json()['data']['accounts'][i]['status'] != 6:
                if r.json()['data']['accounts'][i]['status'] not in accounts_all:
                    accounts_all.append(r.json()['data']['accounts'][i]['status'])
                for j in range(0, len(accounts_all)):
                    url = "https://nas.apiteamn.com/api/profile/" + ban_id + "/shared_account"
                    r2 = requests.get(url=url, headers=header, cert=nas)
                    account2 = r2.json()['data']['accounts']
                    for i in range(0, len(account2)):
                        if r2.json()['data']['accounts'][i]['status'] == 5:
                            if r2.json()['data']['accounts'][i]['status'] not in accounts_all:
                                accounts.append(r2.json()['data']['accounts'][i]['status'])

        # make_normal 将被ban的账号恢复normal


    def make_normal(self, accounts):
        nas_token = basic_API.get_prod_token(self)
        nas_token = "Bearer " + nas_token
        header = {"Authorization": nas_token}
        body = {
            'current_status': 5,
            'reason': None
        }
        for uid in accounts:
            url = "https://nas.apiteamn.com/api/user/" + uid + "/1"
            r = requests.post(url=url, data=json.dumps(body), headers=header, cert=nas)
            print(r.json())
        return None

if __name__ == "__main__":

    #恢复ban
    ba = basic_API()
    ban_id = "6002698378254500b9eb66d1"  # 6079336ad0845d2d5d603e2a johnnyR
    ba.get_shared_account(ban_id)
    print(accounts)
    ba.make_normal(accounts)
