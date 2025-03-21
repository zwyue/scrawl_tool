import requests

from es_client import init_client


class Fund:
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "text/html; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }

    def __init__(self, logger):
        self.logger = logger
        self.sess = requests.session()
        self.client = init_client.get_es_client(self)
        self.index_name = 'last_fund_real_time_price_write'

    def __del__(self):
        self.client.close()

    def execute(self):
        import fund.fund_bz50
        import fund.fund_ftse
        import fund.fund_hstech
        import fund.fund_india
        import fund.fund_investing
        import fund.fund_investing_stock
        import fund.fund_nasdaq_sp
        import fund.fund_silver
        import fund.fund_zz_hs

        fund.fund_bz50.bz50_real_time_info(self, "https://www.bse.cn/neeqRealController/getRealBZ50.do")
        fund.fund_zz_hs.zz500_real_time_info(self, "中证500", "000905", "zz500_")
        fund.fund_zz_hs.zz500_real_time_info(self, "沪深300", "000300", "hs300_")
        fund.fund_hstech.hstech_real_time_info(self,
                                               "https://www.hsi.com.hk/data/schi/rt/index-series/hstech/performance.do")
        fund.fund_ftse.fs100_real_time_info(self, "https://www.lseg.com/api/v1/ftserussel/ticker/getindexes")
        fund.fund_nasdaq_sp.nasdaq_real_time_info(self, "SPX", "标普500", "standardpoor500_")
        fund.fund_nasdaq_sp.nasdaq_real_time_info(self, "NDX", "纳斯达克100", "nasdaq100_")
        fund.fund_silver.silver_futures(self)
        fund.fund_india.nifty50_real_time_info(self, url="https://www.nseindia.com/api/marketStatus")
        fund.fund_india.bse_sensex_real_time_info(self, "16", "印度BSE SENSEX", "bsesensex")
        fund.fund_india.bse_sensex_real_time_info(self, "98", "印度BSE SENSEX 50", "bsesensex50")
        fund.fund_investing.real_time_info(self, '伦敦布伦特原油期货', "brent_oil_", "commodities/brent-oil")
        fund.fund_investing.real_time_info(self, 'WTI原油期货', "crude_oil_", "commodities/crude-oil")
        fund.fund_investing.real_time_info(self, '越南胡志明指数', "vn_", "indices/vn")
        fund.fund_investing.real_time_info(self, '越南VN30指数', "vni30_", "indices/vn-30")
        fund.fund_investing.real_time_info(self, '东南亚科技指数', "south_east_asia_tech_", "etfs/513730")
        fund.fund_investing_stock.real_time_info(self, '中欧时代先锋股票型发起式证券投资基金A', "001938_",
                                                 "funds/zhong-ou-modern-pioneer-initiatinga-holdings")

# if __name__ == '__main__':
#     Fund().execute()
