from NAS.basic_api import basic_API


class MP_normal(basic_API):

    def normal(self):
        ba = basic_API()
        data = ba.login()  # 登录
        token = ba.get_token(data)
        pic_url = ba.image("normal.jpeg")
        number = ba.get_number(token)
        res = ba.sign_up(int(number)+1, pic_url)
        return res

    def MP_delete(self):
        pass


if __name__ == "__main__":
    a = MP_normal()
    result = a.normal()
    print(result)

