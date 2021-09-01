from time import sleep

from selenium import webdriver

chrome_driver = '/Users/pof/Documents/driver/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_driver)
driver.implicitly_wait(5)
driver.get("https://dev-nas.apiteamn.com/login?redirect=/")
driver.find_element_by_id("userName").send_keys("admin")
driver.find_element_by_id("password").send_keys("WP-nas2018")
driver.find_element_by_xpath('//*[@id="root"]/div/form/div[3]/button').click()
sleep(5)
driver.quit()
