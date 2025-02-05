import json
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from log import init_log


class SVC:
    # 创建一个logger
    logger = init_log.logger

    def __init__(self):
        init_log.init(self)
        self.url = 'https://web.shanbay.com/web/account/login/'
        option = webdriver.ChromeOptions()
        # 开发者模式的开关，设置一下，打开浏览器就不会识别为自动化测试工具了
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument("--disable-blink-features")
        option.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=option)
        self.driver.maximize_window()
        self.driver_wait = WebDriverWait(self.driver, 20)
        self.location = {}
        self.size = {'width': 260, 'height': 160}
        self.BORDER = 40
        self.account=None
        self.password=None

    def __del__(self):
        self.driver.close()

    def open(self, account, password):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.driver.get(self.url)
        account_container = self.driver_wait.until(EC.presence_of_element_located((By.ID, 'input-account')))
        password_container = self.driver_wait.until(EC.presence_of_element_located((By.ID, 'input-password')))
        account_container.send_keys(account)
        password_container.send_keys(password)
        self.account = account
        self.password = password

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
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()
        self.logger.info('...... finish moving ......')

    def set_account(self):
        if self.account is None:
            with open("doc/account.json") as file:
                try:
                    data = json.load(file)
                    account = data['shanbay']['name']
                    password = data['shanbay']['password']
                    self.open(account, password)
                except Exception as e:
                    self.logger.info('...... read account.json fail ......')
                    self.logger.info(e)
                finally:
                    file.close()

    def crack(self):
        # 滚动标签ID
        slide_block_element = self.driver.find_elements(By.CLASS_NAME, 'nc-lang-cnt')

        if slide_block_element:
            is_login = self.slide_block(slide_block_element)
        else:
            is_login = True
        if is_login:
            self.write_txt()


    def slide_block(self, block):
        track = self.get_track(268)
        self.logger.info(f'...... 滑动轨迹 {track} ......')
        self.move_to_gap(block, track)
        success = False
        try:
            success = self.driver_wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'nc-lang-cnt'), '验证通过'))
        except Exception as e:
            self.logger.error(e)

        # 失败后重试
        if not success:
            error_msg = self.driver.find_elements(By.CLASS_NAME, 'error-msg')
            if error_msg:
                """
                重试
                """
                self.logger.error(error_msg)
                return True
            else:
                return False
        else:
            return True


    def login(self):
        """
        登录
        :return: None
        """
        try:
            submit = self.driver_wait.until(EC.element_to_be_clickable((By.ID, 'button-login')))
            submit.click()
            self.logger.info('...... 登录成功 ......'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            time.sleep(5)
            self.logger.info('...... 程序继续 ......'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

            error_msg = self.driver.find_elements(By.CLASS_NAME, 'error-msg')
            if error_msg:
                self.logger.info(error_msg[0].text)
                time.sleep(10)
                self.login()
            return True
        except Exception as e:
            self.logger.info(e)
            return False

    def write_txt(self):
        self.logger.info('...... locate element ......')
        famous_saying_element = self.driver.find_element(By.ID, 'quote')
        if famous_saying_element:
            famous_saying = famous_saying_element.text
            self.logger.info("...... 写入文件 ......")
            self.logger.info(famous_saying)
            fo = open("doc/famous_saying.txt", "a", encoding='utf-8')
            write_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            try:
                fo.write('\n' + famous_saying + '\n' + write_time + '\n')
            except Exception as e:
                self.logger.error("...... 文件写入失败 ......")
                self.logger.error(e)
            finally:
                fo.close()

if __name__ == '__main__':
    self = SVC()
    self.set_account()
    self.login()
    self.crack()
