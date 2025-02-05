import requests
from bs4 import BeautifulSoup
from log import init_log

# 创建一个logger
class Raddit:
    logger = init_log.logger

    def __init__(self):
        init_log.init(self)
        self.logger.info(f"...... enter a website ...... ")
        head = {
            "Host": "www.reddit.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51",
                "Accept": "text/html, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "text/html; charset=utf-8",
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive"
        }
        self.logger.info(f"...... enter a website ...... ")
        res = requests.get("https://www.reddit.com/r/GetMotivated/comments/2db9z9/i_dont_know_what_that_dream_is_that_you_have_text/", params=None, headers=head, timeout=(10, 20))

        soup = BeautifulSoup(res.text, 'lxml')

        # contant = soup.find(attrs={"class" :"_292iotee39Lmt0MkQZ2hPV RichTextJSON-root"}).text

        content_p = soup.findAll(attrs={"class" :"_1qeIAgB0cPwnLhDF9XSiJM"})

        fo = open("doc/speech/speech_dream.txt","a",encoding='utf-8')
        try :
            for content in content_p :
                fo.write( '\n' +content.text + '\n' )
        except Exception as e:
            self.logger.info(f"...... 文件写入失败 ")
            self.logger.info(e)
        finally :
            fo.close()


if __name__ == '__main__':
    Raddit()