import json

import requests

"""
北证50实时指数
"""


def bz50_real_time_info(self, url):
    try:
        self.head["Host"] = "www.bse.cn"
        res = requests.get(url, params=None, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_text = result_text.replace('null', '').replace("(", '').replace(")", '')
        json_result = json.loads(json_text)

        last_json = json_result[len(json_result) - 1]
        date = last_json["JSRQ"]
        doc = {
            "date": date,
            "balance": last_json["ZD"],
            "balancerate": last_json["ZDF"] * 100,
            "latest": last_json["SSZS"],
            "previous": last_json["ZRSP"],
            "updatetime": last_json["GXSJ"],
            "name": "北证50",
            "url": [url],
            "method": "get"
        }
        doc_id = "bz50_" + date
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)
    except Exception as e:
        self.logger.info(e)