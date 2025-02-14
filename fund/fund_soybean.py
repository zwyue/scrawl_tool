# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

option = webdriver.ChromeOptions()
# 开发者模式的开关，设置一下，打开浏览器就不会识别为自动化测试工具了
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument("--disable-blink-features")
option.add_argument("--disable-blink-features=AutomationControlled")

# 创建 WebDriver
driver = webdriver.Firefox()

# 打开网页
url = 'http://www.dce.com.cn/dalianshangpin/sspz/487180/index.html'  # 替换为实际网页的 URL
driver.get(url)

# 等待页面加载（可根据实际情况调整）
time.sleep(3)

network = driver.execute_script("return window.performance.getEntries();")
for data in network:
    if data["name"].startswith("http"):
        print(data["name"])
        time.sleep(0.1)

time.sleep(2)
driver.quit()