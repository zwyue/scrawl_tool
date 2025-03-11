import json

from elasticsearch import Elasticsearch


def get_es_client(self, locate="../account.json"):
    try:
        with open(locate) as file:
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
        self.logger.info('...... read account.json fail ......')
        self.logger.info(e)
    finally:
        file.close()

    return Elasticsearch(self.host, ca_certs=self.cert, basic_auth=(self.account, self.password))
