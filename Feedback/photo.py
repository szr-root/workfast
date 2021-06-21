class Photo:
    list = ["无法选择照片", "图片加载不了", "自拍挑战无法使用"]

    def more_detail(self):
         detail = input()
         return detail

    def bug_loaction(self, detail):
        if detail == "无法选择照片":
            print("确认一下手机型号")
