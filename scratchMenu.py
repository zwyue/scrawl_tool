import requests
import init_log
import json


class Menu(object):
    # 创建一个logger
    logger = init_log.logger

    def __init__(self):
        self.sess = requests.session()
        init_log.init(self)

    def menu(self,url):
        res = requests.get(url, params=None, headers=None, timeout=(10, 20))
        resultText = res.text
        jsonResult = json.loads(resultText)
        dishList = jsonResult.get('Data').get('DishList')
        dishName = []

        for dish in dishList : 
            try :
                fo = open("C:\\Users\\zwyli\\IdeaProjects\\html\\menu\\menu.txt","a",encoding='utf-8')
                fo.write(dish.get('DishName')+"\n")
                # fo.write("\'"+dish.get('DishName')+"\',\n")
            except Exception :
                self.logger.error("...... 文件写入失败 ......")
            finally :
                fo.close()       
            
if __name__ == '__main__':
    menu = Menu() 
    menu.menu("http://v2.caimomo.com/WeiXinWeb/AjaxHandler.ashx?methodName=GetDishInfo&GroupID=11997&StoreID=1199705&IsWaiMai=0&MemberID=")