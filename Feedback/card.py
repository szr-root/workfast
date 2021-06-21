class Card:

    def more_detail(self):
        detail = input()
        return detail

    def bug_loaction(self, detail):
        if detail == "无法选择照片":
            print("确认一下手机型号")
