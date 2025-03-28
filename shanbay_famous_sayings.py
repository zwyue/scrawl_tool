import json
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Shanbay:

    def __init__(self, logger, user_data_dir):
        self.logger = logger
        self.url = 'https://web.shanbay.com/web/account/login/'
        options = Options()
        # 开发者模式的开关，设置一下，打开浏览器就不会识别为自动化测试工具了
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-data-dir=" + user_data_dir)
        options.add_argument("--incognito")
        options.add_argument("--enable-logging")
        options.add_argument("--v=1")

        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver_wait = WebDriverWait(self.driver, 20)
        self.location = {}
        self.size = {'width': 260, 'height': 160}
        self.BORDER = 40
        self.account = None
        self.password = None

    def __del__(self):
        self.logger.info("......scratch shanbay finish......")

    def open(self, file):
        if self.account is None:
            with open(file) as file:
                try:
                    data = json.load(file)
                    account = data['shanbay']['name']
                    password = data['shanbay']['password']

                    self.account = account
                    self.password = password

                except Exception as e:
                    self.logger.info('...... read account.json fail ......')
                    self.logger.info(e)
                finally:
                    file.close()
        """
        打开网页输入用户名密码
        :return: None
        """
        self.driver.get(self.url)

    @staticmethod
    def get_track(distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track_list = []
        # 当前位移

        i = 0

        while i < distance / 134:
            track_list.append(43)
            track_list.append(42)
            track_list.append(134 - 43 - 42)
            i = i + 1

        return track_list

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        self.logger.info('...... start moving ......')
        try:
            ActionChains(self.driver).click_and_hold(slider).perform()
            for x in track:
                ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.driver).release().perform()
            self.logger.info('...... finish moving ......')
        except Exception as e:
            self.logger.error(e)

    def crack(self):
        # 滚动标签ID
        # slide_block_element = self.driver.find_elements(By.CLASS_NAME, 'nc-lang-cnt')
        slide_block_element = self.driver.find_elements(By.ID, 'nc_1_n1z')

        is_login = True
        if slide_block_element:
            is_login = self.slide_block(slide_block_element[0])
        if is_login:
            self.write_txt()

    def slide_block(self, block):
        track = self.get_track(268)
        self.logger.info(f'...... 滑动轨迹 {track} ......')
        self.move_to_gap(block, track)

        nc_lang_cnt = self.driver.find_elements(By.CLASS_NAME, 'nc-lang-cnt')
        if nc_lang_cnt:
            try:
                return self.driver_wait.until(
                    EC.text_to_be_present_in_element((By.CLASS_NAME, 'nc-lang-cnt'), '验证通过'))
            except Exception as e:
                self.logger.error(e)
                return self.login()
        else:
            no_captcha_background_cover = self.driver.find_elements(By.ID, 'no-captcha-background-cover')
            if no_captcha_background_cover:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element((By.ID, "no-captcha-background-cover"))
                )
            return self.login()

        # 失败后重试
        # if not success:
        #     error_msg = self.driver.find_elements(By.CLASS_NAME, 'error-msg')
        #     if error_msg:
        #         """
        #         重试
        #         """
        #         self.logger.error(error_msg)
        #         return True
        #     else:
        #         return False
        # else:
        #     return True

    def set_account(self):
        account_container = self.driver_wait.until(EC.presence_of_element_located((By.ID, 'input-account')))
        password_container = self.driver_wait.until(EC.presence_of_element_located((By.ID, 'input-password')))
        account_container.send_keys(self.account)
        time.sleep(2)
        password_container.send_keys(self.password)
        time.sleep(1)

    def login(self):
        try:
            submit = self.driver_wait.until(EC.element_to_be_clickable((By.ID, 'button-login')))
            self.logger.info('...... 点击登录 ......' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            submit.click()
            time.sleep(2)
            error_msg = self.driver.find_elements(By.CLASS_NAME, 'error-msg')
            if error_msg:
                text = error_msg[0].text
                self.logger.info(text + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                if text == '验证失败，请重试～':
                    self.driver.refresh()
                    time.sleep(5)
                    self.set_account()
                    self.login()
            time.sleep(5)
            return True
        except Exception as e:
            self.logger.info(e)
            return False

    def write_txt(self):
        self.logger.info('...... locate element ......')
        famous_saying_elements = self.driver.find_elements(By.ID, 'quote')
        if famous_saying_elements:
            famous_saying = famous_saying_elements[0].text
            self.logger.info("...... 写入文件 ......")
            self.logger.info(famous_saying)
            fo = None
            try:
                doc_date = time.strftime('%Y%m', time.localtime(time.time()))
                file_path = "doc/shanbay/famous_saying_" + doc_date + ".txt"
                fo = open(file_path, "a", encoding='utf-8')
                write_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                fo.write('\n' + famous_saying + '\n' + write_time + '\n')
            except Exception as e:
                self.logger.error("...... 文件写入失败 ......")
                self.logger.error(e)
            finally:
                fo.close()

# if __name__ == '__main__':
# self = Shanbay()
# self.open()
# self.set_account()
# self.login()
# self.crack()
# time.sleep(5)
