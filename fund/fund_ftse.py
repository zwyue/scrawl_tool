import requests
import json

"""
富时100实时指数
"""
def fs100_real_time_info(self, url):
    self.head["Host"] = "www.lseg.com"
    params = {"id": ["UKX"]}
    res = requests.post(url, json=params, headers=self.head, timeout=(10, 20))
    result_text = res.text
    json_result = json.loads(result_text)

    json_data = json_result['Data'][0]
    date = json_data["Date"] + ''
    balance_rate = int((eval(json_data["Change"]) * 100 / eval(json_data["PrevClose"])) * 100) / 100
    doc = {
        "date": date.replace(" 00:00:00.0", ''),
        "balance": json_data["Change"],
        "balancerate": balance_rate,
        "latest": json_data["LastValue"],
        "previous": json_data["PrevClose"],
        "updatetime": json_data["TimeStamp"],
        "name": "富时100"
    }
    doc_id = "fs100_" + date.replace(" 00:00:00.0", '')
    resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
    self.logger.info(resp)