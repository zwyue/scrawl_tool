# -*- coding:utf-8 -*-

import time

from selenium import webdriver

# 创建 WebDriver
driver = webdriver.Firefox()

# 打开网页
url = 'http://www.dce.com.cn/dalianshangpin/sspz/487180/index.html'  # 替换为实际网页的 URL
driver.get(url)

# 等待页面加载（可根据实际情况调整）
time.sleep(60)

network = driver.execute_script(
    "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

for data in network:
    name = data["name"]
    if name.startswith("http"):
        if name.find('.png') > -1:
            time.sleep(0.1)
            continue
        if name.find('.jpg') > -1:
            time.sleep(0.1)
            continue
        if name.find('.css') > -1:
            time.sleep(0.1)
            continue
        if name.find('.gif') > -1:
            time.sleep(0.1)
            continue
        if name.find('.ico') > -1:
            time.sleep(0.1)
            continue
        if name.find('.html') > -1:
            time.sleep(0.1)
            continue
        if name.find('.js') > -1:
            time.sleep(0.1)
            continue
        print(data["name"])
        time.sleep(0.2)

time.sleep(20)

# browser_log = driver.get_log('browser')
#
# print(browser_log)

driver.quit()
