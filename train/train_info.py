from log import init_log
import requests
from elasticsearch import Elasticsearch
import datetime
import train_public_price

class Train:
    # 创建一个logger
    logger = init_log.logger


    def __init__(self):
        self.sess = requests.session()
        init_log.init(self,locate='../Logs\\')


if __name__ == '__main__':
    train_public_price.get_train_public_price(self=Train,url="https://kyfw.12306.cn/otn/leftTicketPrice/queryAllPublicPrice?leftTicketDTO.train_date=2025-01-27&leftTicketDTO.from_station=TMK&leftTicketDTO.to_station=NJH&purpose_codes=ADULT")
    # train = Train()
    # train.create_index()
    # train_city.get_train_city(self=Train,url="https://www.12306.cn/index/otn/reservationQuery/getTrainCity")