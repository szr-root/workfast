from Feedback.card import Card
from Feedback.message import Message
from Feedback.photo import Photo
from Feedback.vip import VIP
from Feedback.who_like_me import WLM

photo_list = ["无法选择照片", "图片加载不了"]
card_list = ["卡片重复"]
message_list = ["发送消息失败"]
vip_list = ["无法购买vip"]
wlm_list = ["无法解锁"]
class FeedBack:
    question_list = ["photo", "card", "who-like-me", "message", "vip"]
    def question_input(self):
        print("输入问题类型:")
        q_type = input()
        return q_type

    def question_location(self, qtype):
        if qtype.lower() == "photo":
            print("photo类的问题:", photo_list)
            return Photo()
        elif qtype.lower() == "card":
            print("card类的问题:", card_list)
            return Card()
        elif qtype.lower() == "who-like-me":
            print("who-like-me类的问题:", wlm_list)
            return WLM()
        elif qtype.lower() == "message":
            print("message类的问题:", message_list)
            return Message()
        elif qtype.lower() == "vip":
            print("vip类的问题:", vip_list)
            return VIP()
        else:
            print("还没有该类型的bug记录")


    def question_type(self):
        pass

if __name__ == "__main__":
    q = FeedBack()
    print(q.question_list)
    question_type = q.question_input()
    q2 = q.question_location(question_type)
    detail = q2.more_detail()
    q2.bug_loaction(detail)
