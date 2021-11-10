import json
from hashlib import md5
from time import sleep

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
        user1 = ba.sign_up(int(num), ba.image("male.jpg"))
        sleep(1)
        num = int(num) + 1
        user2 = ba.sign_up(num, ba.image("female.jpg"))
        self.user1_token = user1['data']['token']
        self.user2_token = user2['data']['token']
        self.user1_id = user1['data']['user']['user_id']
        self.user2_id = user2['data']['user']['user_id']
        self.user1_gender = user1['data']['user']['gender']
        self.user2_gender = user2['data']['user']['gender']
        self.user1_name = user1['data']['user']['display_name']
        self.user2_name = user2['data']['user']['display_name']
        self.user1_info = [self.user1_id, self.user1_name, self.user1_gender]
        self.user2_info = [self.user2_id, self.user2_name, self.user2_gender]
        self.comment_id = ''
        self.moment_id = ''

        sleep(1)

    @pytest.mark.run(order=1)
    def test_like_list(self):
        ba.slide_like(self.user1_token, self.user2_id)  # user1 like user2
        assert self.user2_id == ba.get_latest_likeList(self.user1_token)  # check user1's like_list
        sleep(1)

    @pytest.mark.run(order=2)
    def test_who_like_me(self):
        assert self.user1_id == ba.get_who_likeme(self.user2_token)
        sleep(1)

    @pytest.mark.run(order=3)
    def test_match(self):
        match_info = ba.slide_like(self.user2_token, self.user1_id)  # user2 like user1
        assert self.user1_id == match_info['data']['matches'][0]['id']
        sleep(1)

    @pytest.mark.run(order=4)
    def test_block(self):
        assert self.user2_id == ba.block(self.user1_token, self.user2_id)  # user1 block user2
        sleep(1)

    @pytest.mark.run(order=5)
    def test_block_delete(self):
        assert 'success' == ba.block_delete(self.user1_token, self.user2_id)
        sleep(1)

    @pytest.mark.run(order=6)
    def test_post_moment(self):
        post_moment_result = ba.send_moment(self.user1_token)  # return [moment_id, message]
        self.moment_id = post_moment_result[0]
        assert 'success' == post_moment_result[1]
        sleep(1)

    @pytest.mark.run(order=7)
    def test_like_moment(self):
        assert 'success' == ba.like_moment(self.user2_token, self.moment_id, self.user1_info)
        sleep(1)

    @pytest.mark.run(order=8)
    def test_comment_moment(self):
        # return [comment_id, message]
        comment_moment_result = ba.comment_moment(self.user2_token, self.moment_id, self.user1_info)
        self.comment_id = comment_moment_result[0]
        assert 'success' == comment_moment_result[1]
        sleep(1)

    @pytest.mark.run(order=9)
    def test_delete_comment(self):
        assert 'success' == ba.delete_comment(self.user1_token, self.comment_id, self.moment_id)
        sleep(1)

    @pytest.mark.run(order=10)
    def test_delete_moment(self):
        assert 'success' == ba.delete_moment(self.user1_token, self.moment_id)
        sleep(1)

    @pytest.mark.run(order=11)
    def test_change_main_photo(self):
        pass

    @pytest.mark.run(order=12)
    def test_edit_profile(self):  # 加幅图。填问题等。
        pass

    @pytest.mark.run(order=13)
    def test_upload_video(self):
        ba.upload_video(self.user1_token)

    @pytest.mark.run(order=14)
    def test_verify(self):
        pass

    @pytest.mark.run(order=15)
    def test_delete_user(self):
        pass
