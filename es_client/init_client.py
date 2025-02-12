from elasticsearch import Elasticsearch
import json
from log import init_log

logger = init_log.logger

def get_es_client(self):
    init_log.init(self, locate='../Logs\\')

    with open("../doc/account.json") as file:
        try:
            data = json.load(file)
            account = data['elastic']['name']
            password = data['elastic']['password']
            cert = data['elastic']['ca_cert']
            host = data['elastic']['host']

            self.account = account
            self.password = password
            self.cert = cert
            self.host = host

        except Exception as e:
            logger.info('...... read account.json fail ......')
            logger.info(e)
        finally:
            file.close()

    return Elasticsearch(self.host,ca_certs=self.cert,basic_auth=(self.account, self.password))
