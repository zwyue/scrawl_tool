# -*- coding:utf-8 -*-

import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

from fund.chrome_option import get_options


# import shutil


def real_time_info(self, name, prefix, category):
    try:
        # Clean up the user data directory
        # shutil.rmtree("/tmp/unique-chrome-user-data", ignore_errors=True)

        # 创建 WebDriver
        driver = webdriver.Chrome(options=get_options())

        url = "https://cn.investing.com/" + category
        # 打开网页
        driver.get(url)

        time.sleep(10)

        instrument_price_last = driver.find_elements(By.XPATH, "//div[@data-test='instrument-price-last']")[0].text
        price_change = driver.find_elements(By.XPATH, "//span[@data-test='instrument-price-change']")[0].text
        change_percent = driver.find_elements(By.XPATH, "//span[@data-test='instrument-price-change-percent']")[0].text
        trading_time_label = driver.find_elements(By.TAG_NAME, 'time')[0].text
        prev_close = driver.find_elements(By.XPATH, "//dd[@data-test='prevClose']")[0].text
        time_element = driver.find_element(By.TAG_NAME, 'time')
        datetime_value = time_element.get_attribute('datetime')
        date = datetime_value[0:10]

        if trading_time_label.find('/') > -1:
            strptime = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M:%S.000Z')
            update_time = datetime.strftime(strptime, "%H%M%S")
        else:
            update_time = trading_time_label.replace(":", '')

        driver.close()
        doc = {
            "date": date,
            "balance": price_change.replace("+", ''),
            "balancerate": change_percent.replace("+", '').replace("(", '').replace(")", '').replace("%", ''),
            "latest": instrument_price_last.replace(",", ''),
            "previous": prev_close.replace(",", ''),
            "updatetime": update_time,
            "name": name,
            "url": [url],
            "method": "selenium"
        }

        doc_id = prefix + date
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)
    except Exception as e:
        self.logger.info(e)
