# -*- coding:utf-8 -*-
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from fund.chrome_option import get_options


# import shutil


def real_time_info(self, name, prefix, category, time_class):
    # Clean up the user data directory
    # shutil.rmtree("/tmp/unique-chrome-user-data", ignore_errors=True)

    # 创建 WebDriver
    driver = webdriver.Chrome(options=get_options())
    try:
        url = "https://www.investing.com/" + category
        # 打开网页
        driver.get(url)

        time.sleep(10)

        instrument_price_last = driver.find_element(By.ID, "last_last").text
        price_change = driver.find_elements(By.XPATH, "//span[@dir='ltr']")[1].text
        change_percent = driver.find_elements(By.XPATH, "//span[@dir='ltr']")[2].text
        trading_time_label = driver.find_elements(By.CLASS_NAME, time_class)[0].text
        update_date = datetime.strptime(str(datetime.now().year) + "/" + trading_time_label, "%Y/%d/%m")
        update_date_str = datetime.strftime(update_date, "%Y-%m-%d")

        # 获取表格数据
        # Wait for the XHR request to complete (adjust timeout as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fundsHoldings"))
        )

        # Locate the outer parent element
        fundsHoldings = driver.find_element(By.CLASS_NAME, "fundsHoldings")
        mainstockes = []

        nested_elements = fundsHoldings.find_elements(By.CLASS_NAME, "section")
        calculation = 0.00
        for nested_element in nested_elements:
            # Locate the element nested even deeper
            h3 = nested_element.find_element(By.TAG_NAME, "h3")
            # if h3 and h3.text == '主要持仓':
            if h3 and h3.text == 'Top Holdings':
                # Extract the text
                tbody = nested_element.find_element(By.TAG_NAME, "tbody")
                trs = tbody.find_elements(By.TAG_NAME, "tr")
                for tr in trs:
                    aTags = tr.find_elements(By.TAG_NAME, "a")
                    if len(aTags):
                        weight = eval(tr.find_element(By.CLASS_NAME, "center").text)
                        balance_rate = eval(
                            tr.find_elements(By.CLASS_NAME, "right")[1].text.replace("%", '').replace("+", ''))
                        mainstocke = {
                            "name": aTags[0].text,
                            "weight": weight,
                            "latest": tr.find_elements(By.CLASS_NAME, "right")[0].text.replace(",", ''),
                            "balancerate": balance_rate
                        }
                        calculation += weight * balance_rate
                        mainstockes.append(mainstocke)

        driver.quit()

        calculation = int(calculation * 100) / 10000
        doc = {
            "date": update_date_str,
            "balance": price_change.replace("+", ''),
            "balancerate": change_percent.replace("+", '').replace("(", '').replace(")", '').replace("%", ''),
            "latest": instrument_price_last.replace(",", ''),
            # "previous": instrument_price_last.replace(",", ''),
            "updatetime": "160000",
            "name": name,
            "url": [url],
            "method": "selenium",
            "mainstock": mainstockes,
            "calculation": calculation
        }

        doc_id = prefix + update_date_str
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)
    except Exception as e:
        self.logger.info(e)
        driver.quit()