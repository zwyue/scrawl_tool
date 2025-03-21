import os

from elasticsearch import Elasticsearch


def get_es_client(self):
    try:
        self.account = os.environ.get("ES_NAME")
        self.password = os.environ.get("ES_PASSWORD")
        self.cert = os.environ.get("ES_CA_CERT")
        self.host = os.environ.get("ES_HOST")
    except Exception as e:
        self.logger.info('...... read account.json fail ......')
        self.logger.info(e)

    return Elasticsearch(self.host, ca_certs=self.cert, basic_auth=(self.account, self.password))
