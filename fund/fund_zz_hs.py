import json

import requests

"""
中证500、沪深300实时指数
"""


def zz500_real_time_info(self, name, code, prefix):
    try:
        self.head["Host"] = "www.csindex.com.cn"
        url = "https://www.csindex.com.cn/csindex-home/perf/index-perf-oneday?indexCode=" + code
        res = requests.get(url, params=None, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_result = json.loads(result_text)

        json_data = json_result['data']['intraDayHeader']

        date = json_data["tradeDate"]
        updatetime = json_data["tradeTime"].replace(":", '')
        doc = {
            "date": date,
            "balance": json_data["change"],
            "balancerate": json_data["changePct"],
            "latest": json_data["current"],
            "previous": json_data["closePre"],
            "updatetime": updatetime,
            "name": name,
            "url": [url],
            "method": "get"
        }
        doc_id = prefix + date
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)

    except Exception as e:
        self.logger.info(e)
