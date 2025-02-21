import json

import requests

"""
nasdaq100/标普500 实时指数
"""


def hstech_real_time_info(self, url):
    self.head["Host"] = "www.hsi.com.hk"
    res = requests.get(url, headers=self.head, timeout=(10, 20))
    result_text = res.text
    json_result = json.loads(result_text)

    json_data = json_result['indexSeriesList'][0]['indexList'][0]
    request_date = json_data["lastUpdate"]
    date = request_date[0:10]
    time = request_date[11:19].replace(":", '')
    balance_rate = json_data['changePercentage'].replace("+", '')
    balance = json_data["changeValue"].replace("+", '')
    index_value = json_data["indexValue"]
    previous_close = json_data["previousClose"]
    name = json_data["indexName"]
    doc = {
        "date": date,
        "balance": balance,
        "balancerate": balance_rate,
        "latest": index_value,
        "previous": previous_close,
        "updatetime": time,
        "name": name
    }

    doc_id = "hstech_" + date
    resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
    self.logger.info(resp)
