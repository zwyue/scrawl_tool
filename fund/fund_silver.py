from datetime import datetime
import requests
import json

"""
白银期货
"""

def silver_futures(self):
    self.head["Host"] = "www.shfe.com.cn"

    timestamp = str(int(datetime.now().timestamp()*1000))
    # step1: query yesterday's price
    url1 = "https://www.shfe.com.cn/data/tradedata/future/delaymarket/delayed_market_data_ag_history.dat?params=%22"+timestamp
    res1 = requests.get(url1, headers=self.head, timeout=(10, 20))
    result_text = res1.text
    json_result = json.loads(result_text)

    json_data = json_result['ci_data']
    data_yesterday = json_data[len(json_data)-2]

    close_price = data_yesterday['CLOSEPRICE']

    # step2: query today's price
    url2 = "https://www.shfe.com.cn/data/tradedata/future/delaymarket/delaymarket_ag.dat?params=" + timestamp
    res2 = requests.get(url2,headers=self.head, timeout=(10, 20))
    result2_text = res2.text
    json_result2 = json.loads(result2_text)
    json_data2 = json_result2['delaymarket'][0]
    last_price = json_data2['lastprice']

    time = json_data2['updatetime']
    strftime = time[0:10]
    updatetime = time[11:19].replace(":",'')
    balance = eval(last_price) - close_price
    balance_rate = int((balance/close_price)*10000)/100

    doc = {
        "date": strftime,
        "balance": balance,
        "balancerate": balance_rate,
        "latest": last_price,
        "previous": close_price,
        "updatetime": updatetime,
        "name": "白银期货"
    }

    doc_id = "silver_futures_" + strftime
    resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
    self.logger.info(resp)