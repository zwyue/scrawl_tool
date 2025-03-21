import json
from datetime import datetime

import requests

"""
nasdaq100/标普500 实时指数
"""


def nasdaq_real_time_info(self, symbol, name, prefix):
    try:
        self.head["Host"] = "api.nasdaq.com"
        url = "https://api.nasdaq.com/api/quote/" + symbol + "/chart?assetclass=index"
        res = requests.get(url, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_result = json.loads(result_text)

        json_data = json_result['data']
        timeAsOf = json_data["timeAsOf"]
        strptime = datetime.strptime(timeAsOf, '%b %d, %Y').date()
        strftime = datetime.strftime(strptime, "%Y-%m-%d")
        balance_rate = json_data['percentageChange'].replace("+", '').replace("%", '')
        balance = json_data["netChange"].replace("+", '')

        doc = {
            "date": strftime,
            "balance": balance.replace(",", ''),
            "balancerate": balance_rate,
            "latest": json_data["lastSalePrice"].replace(",", ''),
            "previous": json_data["previousClose"].replace(",", ''),
            "updatetime": "160000",
            "name": name,
            "url": [url],
            "method": "get"
        }

        doc_id = prefix + strftime
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)
    except Exception as e:
        self.logger.info(e)
