import json
from datetime import datetime

import requests

"""
印度 nifty50 实时指数
"""


def nifty50_real_time_info(self, url):
    try:
        self.head["Host"] = "www.nseindia.com"
        res = requests.get(url, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_result = json.loads(result_text)

        json_data = json_result['indicativenifty50']
        market_state_0 = json_result['marketState'][0]
        date_time = market_state_0["tradeDate"]

        strptime = datetime.strptime(date_time, '%d-%b-%Y %H:%M')
        strftime = datetime.strftime(strptime, "%Y-%m-%d")
        updatetime = datetime.strftime(strptime, "%H%M%S")
        balance_rate = market_state_0['percentChange']
        balance = market_state_0["variation"]

        doc = {
            "date": strftime,
            "balance": balance,
            "balancerate": balance_rate,
            "latest": market_state_0["last"],
            "previous": json_data["finalClosingValue"],
            "updatetime": updatetime,
            "name": "印度nifty50",
            "url": [url],
            "method": "get"
        }

        doc_id = "nifty50_" + datetime.strftime(strptime, "%Y%m%d")
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)
    except Exception as e:
        self.logger.info(e)

"""
印度 SENSEX相关 实时指数
"""


def bse_sensex_real_time_info(self, code, name, prefix):
    try:
        self.head["Host"] = "api.bseindia.com"
        self.head["referer"] = "https://www.bseindia.com/"
        url = 'https://api.bseindia.com/BseIndiaAPI/api/GetLinknew/w?code=' + code
        res = requests.get(url, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_result = json.loads(result_text)

        date_time = json_result["DT_TM"]

        strptime = datetime.strptime(date_time, '%d %b %Y | %H:%M')
        strftime = datetime.strftime(strptime, "%Y-%m-%d")
        updatetime = datetime.strftime(strptime, "%H%M%S")
        balance_rate = json_result['ChgPer'].replace("+", '').replace(",", '')
        balance = json_result["Chg"].replace("+", '').replace(",", '')

        doc = {
            "date": strftime,
            "balance": balance,
            "balancerate": balance_rate,
            "latest": json_result["CurrValue"].replace(",", ''),
            "previous": json_result["Prev_Close"].replace(",", ''),
            "updatetime": updatetime,
            "name": name,
            "url": [url],
            "method": "get"
        }

        doc_id = prefix + datetime.strftime(strptime, "%Y%m%d")
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)
    except Exception as e:
        self.logger.info(e)
