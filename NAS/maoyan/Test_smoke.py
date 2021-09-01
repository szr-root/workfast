import json
from hashlib import md5
import pytest
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

ba = basic_API()


class TestSmoke:
    def setup_class(self):
        num = ba.get_user_dispalyname(ba.get_nas_token())
        user1 = ba.sign_up(num, ba.image("01.jpeg"))
        num = int(num) + 1
        user2 = ba.sign_up(num, ba.image("02.jpeg"))
        self.user1_token = user1['data']['token']
        self.user2_token = user2['data']['token']
        self.user1_id = user1['data']['user']['user_id']
        self.user2_id = user2['data']['user']['user_id']

    @pytest.mark.run(order=1)
    def test_like_list(self):
        ba.slide_like(self.user1_token, self.user2_id)  # user1 like user2
        assert self.user2_id == ba.get_latest_likeList(self.user1_token)  # check user1's like_list

    @pytest.mark.run(order=2)
    def test_who_like_me(self):
        assert self.user1_id == ba.get_who_likeme(self.user2_token)

    @pytest.mark.run(order=3)
    def test_match(self):
        match_info = ba.slide_like(self.user2_token, self.user1_id)  # user2 like user1
        assert self.user1_id == match_info['data']['matches'][0]['id']

    @pytest.mark.run(order=4)
    def test_block(self):
        assert self.user2_id == ba.block(self.user1_token, self.user2_id)  # user1 block user2

