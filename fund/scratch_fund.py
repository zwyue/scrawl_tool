from log import init_log
import requests
import json

from elasticsearch import Elasticsearch

class Fund(object):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "text/html; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }

    # 创建一个logger
    logger = init_log.logger
    client = Elasticsearch("http://localhost:9200")
    index_name = 'last_fund_real_time_price'

    def __init__(self):
        self.sess = requests.session()
        init_log.init(self,locate='../Logs\\')

    """
    北证50实时指数
    """
    def bz50_real_time_info(self,url):
        self.head["Host"]="www.bse.cn"
        res = requests.get(url, params=None, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_text = result_text.replace('null','').replace("(",'').replace(")",'')
        json_result = json.loads(json_text)

        last_json = json_result[len(json_result)-1]
        date = last_json["JSRQ"]
        doc={
            "date": date,
            "balance": last_json["ZD"],
            "balancerate": last_json["ZDF"]*100,
            "latest": last_json["SSZS"],
            "previous": last_json["ZRSP"],
            "updatetime": last_json["GXSJ"],
            "name":"北证50"
        }
        doc_id = "bz50_" + date
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-",''), document=doc)
        self.logger.info(resp)

    """
    中证500、沪深300实时指数
    """
    def zz500_real_time_info(self,name, code,id):
        self.head["Host"] = "www.csindex.com.cn"
        url = "https://www.csindex.com.cn/csindex-home/perf/index-perf-oneday?indexCode="+code
        res = requests.get(url, params=None, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_result = json.loads(result_text)

        json_data = json_result['data']['intraDayHeader']
        date = json_data["tradeDate"]
        updatetime = json_data["tradeTime"].replace(":",'')
        doc = {
            "date": date,
            "balance": json_data["change"],
            "balancerate": json_data["changePct"],
            "latest": json_data["current"],
            "previous": json_data["closePre"],
            "updatetime": updatetime,
            "name":name
        }
        doc_id = id + date
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)

    """
    富时100实时指数
    """
    def fs100_real_time_info(self, url):
        self.head["Host"] = "www.lseg.com"

        params={"id":["UKX"]}

        res = requests.post(url, json=params, headers=self.head, timeout=(10, 20))
        result_text = res.text
        json_result = json.loads(result_text)

        json_data = json_result['Data'][0]
        date = json_data["Date"] + ''
        balancerate = int((eval(json_data["Change"]) * 100 / eval(json_data["PrevClose"]))*100)/100
        doc = {
            "date": date.replace(" 00:00:00.0",''),
            "balance": json_data["Change"],
            "balancerate": balancerate,
            "latest": json_data["LastValue"],
            "previous": json_data["PrevClose"],
            "updatetime": json_data["TimeStamp"],
            "name": "富时100"
        }
        doc_id = "fs100_" + date
        resp = self.client.index(index=self.index_name, id=doc_id.replace("-", ''), document=doc)
        self.logger.info(resp)

if __name__ == '__main__':
    fund = Fund()
    fund.bz50_real_time_info("https://www.bse.cn/neeqRealController/getRealBZ50.do")
    fund.zz500_real_time_info("中证500","000905","zz500_")
    fund.zz500_real_time_info("沪深300","000300","hs300_")
    fund.fs100_real_time_info("https://www.lseg.com/api/v1/ftserussel/ticker/getindexes")