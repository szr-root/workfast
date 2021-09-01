# from urllib.request import urlopen
# from bs4 import BeautifulSoup
#
# html = urlopen("http://www.pythonscraping.com/pages/page3.html")
# if html is None:
#     print("url is not found")
# else:
#     bsobj = BeautifulSoup(html.read(), features="html.parser")
#     nameList = bsobj.findAll("table", {"id": "giftList"})
#     print(nameList)
#     nameList2 = bsobj.find("table", {"id": "giftList"}).children
#     print(nameList2)
#     for child in bsobj.find("table", {"id": "giftList"}).children:
#         print(child)


from hashlib import md5

password = md5(("johnny" + "9BE72424-F231-477D-B4E4-0DEEE7E52606").encode()).hexdigest()
print(password)

# a1 = ["x", "y"]
# a2 = ["1", "2"]
# for result in ("%s%s" % (n1, n2)for n1 in a1 for n2 in a2):
#     print(result)
# for result2 in ('%s%s'%(a1,a2)):
#     print(result2)

# import os
#
# baseDir = os.path.join(os.getcwd(), "static")
# print(baseDir)
