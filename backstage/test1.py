from time import sleep

from selenium import webdriver

from NAS.basic_api import basic_API

ba = basic_API()

chrome_driver = '/Users/pof/Documents/driver/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_driver)
driver.implicitly_wait(5)
driver.get("https://dev-nas.apiteamn.com/login?redirect=/profile")
driver.find_element_by_id("userName").send_keys("admin")
driver.find_element_by_id("password").send_keys("WP-nas2018")
driver.find_element_by_xpath('//*[@id="root"]/div/form/div[3]/button').click()

num = ba.get_user_dispalyname(ba.get_nas_token())
user1 = ba.sign_up(num, ba.image("01.jpeg"))
user1_token = user1['data']['token']
user1_id = user1['data']['user']['user_id']
user1_name = user1['data']['user']['display_name']

driver.refresh()
x = driver.find_element_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]/td[2]')
print(x.text)
if x.text == user1_name:
    print("success")

sleep(5)
driver.quit()
