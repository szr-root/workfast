import base64
import json

dev = "wooplus-stage-img"
prod = "wooplus-prod-img"

while True:
    img_uri = input("输入url：")
    encrypt_src_data = json.dumps({"bucket": prod, "key": img_uri})
    encrypt_data = str(encrypt_src_data).encode('utf-8')
    img_uri_encrypted = base64.b64encode(encrypt_data)
    portrait_url = 'https://image.apiteamn.com/' + img_uri_encrypted.decode('utf-8')
    print(portrait_url)
