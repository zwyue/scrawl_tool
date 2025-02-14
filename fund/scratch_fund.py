import requests

from es_client import init_client
from log import init_log

import fund_silver
import fund_nasdaq_sp
import fund_ftse
import fund_bz50
import fund_zz_hs


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
    logger = init_log.logger

    def __init__(self):
        init_log.init(self, locate='../Logs\\')
        self.sess = requests.session()
        self.client = init_client.get_es_client(self)
        self.index_name = 'last_fund_real_time_price'

    def __del__(self):
        self.client.close()

if __name__ == '__main__':
    fund = Fund()
    fund_bz50.bz50_real_time_info(fund,"https://www.bse.cn/neeqRealController/getRealBZ50.do")
    fund_zz_hs.zz500_real_time_info(fund,"中证500", "000905", "zz500_")
    fund_zz_hs.zz500_real_time_info(fund,"沪深300", "000300", "hs300_")
    fund_ftse.fs100_real_time_info(fund,"https://www.lseg.com/api/v1/ftserussel/ticker/getindexes")
    fund_nasdaq_sp.nasdaq_real_time_info(fund,"SPX", "标普500", "standardpoor500_")
    fund_nasdaq_sp.nasdaq_real_time_info(fund,"NDX", "纳斯达克100", "nasdaq100_")
    fund_silver.silver_futures(fund)
