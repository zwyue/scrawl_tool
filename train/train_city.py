import requests
import json

def get_train_city(self, url):
    res = requests.get(url, params=None, headers=None, timeout=(10, 20))
    result_text = res.text
    json_result = json.loads(result_text)
    bsg_city_list = json_result.get('data').get('bsgCityList')

    try:
        with open("../doc/bsg_city_list.json", 'a', encoding='utf-8') as file:
            json.dump(bsg_city_list, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"写入文件 时发生异常: {e}")
