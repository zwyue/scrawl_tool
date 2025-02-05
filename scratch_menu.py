import requests
from log import init_log
import json


class Menu(object):
    # 创建一个logger
    logger = init_log.logger

    def __init__(self):
        self.sess = requests.session()
        init_log.init(self)

    def menu(self,url):
        res = requests.get(url, params=None, headers=None, timeout=(10, 20))
        result_text = res.text
        json_result = json.loads(result_text)
        dish_list = json_result.get('Data').get('DishList')

        for dish in dish_list :
            fo = open("doc/menu.txt", "a", encoding='utf-8')
            try :
                fo.write(dish.get('DishName')+"\n")
            except Exception as e :
                self.logger.error("...... 文件写入失败 ......")
                self.logger.error(e)
            finally :
                fo.close()

        self.logger.info("...... 写入结束 ......")
            
if __name__ == '__main__':
    menu = Menu() 
    menu.menu("http://v2.caimomo.com/WeiXinWeb/AjaxHandler.ashx?methodName=GetDishInfo&GroupID=11997&StoreID=1199705&IsWaiMai=0&MemberID=")