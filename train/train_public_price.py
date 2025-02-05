import requests
import json
from elasticsearch.helpers import bulk

from elasticsearch import Elasticsearch
from log import init_log

def get_train_public_price(self, url):
    init_log.init(self)
    res = requests.get(url, params=None, headers=None, timeout=(10, 20))
    result_text = res.text
    json_result = json.loads(result_text)
    data = json_result.get('data')

    client = Elasticsearch("http://localhost:9200")

    index_name = 'train_public_price'
    logger = init_log.logger

    bulk_data = []
    # index in range(len(fruits))
    logger.info(len(data))
    for index in range(len(data)):
        try:
            bulk_item = {
                    '_index': index_name,
                    '_id': index,
                    # '_routing': 5,
                    # 'pipeline': 'my-ingest-pipeline',
                    '_source': data[index]
            }
            bulk_data.append(bulk_item)
            # doc = item
            # self.client.index(index=index_name, id='1', document=doc)
        except Exception as e:
            logger.info("... save wrong ...")

    logger.info(len(bulk_data))
    bulk(client, bulk_data)

