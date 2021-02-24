from datetime import datetime, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import json
import platform
import requests
from lxml import etree
import pytesseract
from PIL import Image
import urllib.request
import io
import os.path
import init_log

class SpokenAndWritten(object):
    head = {
        "Host": "www.tjxz.cc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51",
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "text/html; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }

    # 创建一个logger
    logger = init_log.logger

    def __init__(self):
        self.sess = requests.session()
        init_log.init(self)

    def list_page(self,day_limit,url,save_path,start_page,if_read_pic):

        is_continue= True 

        while(is_continue) :
            self.logger.info(f"...... 第 {start_page} 页 ......")

            if start_page == 1 :
                res = requests.get(url, params=None, headers=self.head, timeout=(10, 20))
            else :
                res = requests.get(url+'/page/'+str(start_page), headers=self.head, timeout=(10, 20))

            html = etree.HTML(res.text)


            result_page = html.xpath("//*[@class='page-numbers']/text()")
            last_page = 1
            if result_page == None :
                return
            else :
                last_page = int(result_page[-1])
                
            if start_page > 1 :
                curent_page = html.xpath("//*[@class='page-numbers current']/text()")
                if int(curent_page[0]) > last_page :
                    last_page = int(curent_page[0])

            pageNum = last_page
            self.logger.info(f"...... 获取分页 页数 : {pageNum} ")


            results = html.xpath('//h3[contains(@class,"entry-title mh-loop-title")]//a/@href')
            update_time = html.xpath("//*[@class='mh-loop-header']//*[@class='mh-meta-date updated']/text()")

            latest = datetime.strptime(update_time[-1], "%Y年%m月%d日")
            is_continue = latest >= datetime.strptime(day_limit, "%Y-%m-%d") 

            for result in results:
                self.detail_page(result,save_path,if_read_pic)

            if(is_continue) :
                start_page = start_page + 1
                is_continue = start_page <= pageNum
            
    def detail_page(self, detail_url,save_path,if_read_pic):
        self.logger.info("...... 详情页面 ......")
        res = requests.get(detail_url, headers=self.head, timeout=(10, 20))
        soup = BeautifulSoup(res.text, 'lxml')

        strongs = soup.article
        title = soup.find(attrs={"class" :"entry-title"}).text
        title = title.replace(",","-").replace("、","-").replace("|","-").replace(' ', '')

        self.logger.info(f"...... 文章标题 {title} ......")

        img_text_chi = ''

        article = strongs.text
        if if_read_pic :
            try :
                text_img = soup.find('strong',text='影视用例').parent.find_next_siblings()[0].next.get('src')

                self.logger.info(f"...... 获取文章影视用例图片 地址 {text_img}......")

                url_img = urllib.request.urlopen(text_img)
                temp_img = io.BytesIO(url_img.read())
                image = Image.open(temp_img)

                img_text_chi_contain = pytesseract.image_to_string(image, lang='chi_sim')
                img_text_eng = pytesseract.image_to_string(image)

                for chi in img_text_chi_contain :
                    if u'\u4e00' <= chi <= u'\u9fff':
                        img_text_chi = img_text_chi + chi

                img_text_eng = img_text_eng.rsplit('\n\x0c')[0].split('\n')[-1]
            except Exception :
                self.logger.error("...... 获取文章影视用例图片失败 ......")

            if len(img_text_chi) == 0 :
                self.logger.info("...... 未解析成功图片文字 ......")
            else :
                article_split = strongs.text.split('\n影视用例\n\n')
                article = article_split[0] + '\n影视用例\n\n' + img_text_chi + '\n\n' + img_text_eng + '\n\n\x0c' + article_split[1]
            
        try :
            self.logger.info("...... 写入文件 ......")
            fo = open(save_path + title+".txt","w",encoding='utf-8')
            fo.write( article + '\n')
        except Exception :
            self.logger.error("...... 文件写入失败 ......")
        finally :
            fo.close()
        
if __name__ == '__main__':
    sw = SpokenAndWritten() 
    sw.list_page(time.strftime("%Y-%m-%d"),"https://www.tjxz.cc/tag/te-words","doc/words_detail/",1,True)
    sw.list_page(time.strftime("%Y-%m-%d"),"https://www.tjxz.cc/tag/synonyms","doc/words_distinguish/",1,False)
    sw.list_page(time.strftime("%Y-%m-%d"),"https://www.tjxz.cc/tag/speech","doc/speech/",1,False)
    # sw.list_page('2018-01-01',"https://www.tjxz.cc/tag/synonyms","doc/words_distinguish/",1)
    # SpokenAndWritten().list_page('2019-01-01')