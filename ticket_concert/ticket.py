# -*- coding: utf-8 -*-
#autor:Oliver0047
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep
import time
import pickle
import os
import json
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# https://www.cnblogs.com/mq0036/p/18079976 第7点
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("D:/projects/backup/practice/scrawl_tool/ticket_concert/ticket.py"))))

from log import init_log

damai_url="https://www.damai.cn/"
login_url="https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"

class Concert(object):
    # 创建一个logger
    logger = init_log.logger
    def __init__(self,name,date,price,place,real_name,method=1):
        init_log.init(self,locate='../Logs\\')
        self.name=name#歌星
        self.date=date#日期序号优先级，比如，如果第二个时间可行，就选第二个，不然就选其他,最终只选一个
        self.price=price#票价序号优先级,道理同上
        self.place=place#地点
        self.status=0#状态,表示如今进行到何种程度
        self.login_method=method#{0:模拟登录,1:Cookie登录}自行选择登录方式
        self.real_name=real_name#实名者序号
        self.uid = None
        self.upw = None
        self.usr_name = None

    def set_account(self):
        # 读入用户名与密码和昵称
        with open("../doc/account.json") as file:
            try:
                data = json.load(file)
                self.uid = data['damai']['name']
                self.upw = data['damai']['password']
                self.usr_name = data['damai']['nickname']
            except Exception as e:
                self.logger.info('...... read account.json fail ......')
                self.logger.info(e)
            finally:
                file.close()
            
    def get_cookie(self):
       self.driver.get(damai_url)
       self.logger.info("###请点击登录###")
       while self.driver.title.find('大麦网-全球演出赛事官方购票平台')!=-1:
           sleep(1)
       print("###请扫码登录###")
       while self.driver.title=='中文登录':
           sleep(1)
       self.logger.info("###扫码成功###")
       pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
       self.logger.info("###Cookie保存成功###")
    
    def set_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))#载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain':'.damai.cn',#必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as exception:
            self.logger.error(exception)
            
    def login(self):
        if self.login_method==0:
            self.driver.get(login_url)#载入登录界面
            self.logger.info('###开始登录###')
            try:    
                element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, 'alibaba-login-box')))
            except Exception as exception:
                self.logger.error(exception)
                self.logger.info('###定位不到登录框###')
            self.driver.switch_to.frame('alibaba-login-box')#里面这个是iframe的id
            self.driver.find_element(By.ID,'fm-login-id').send_keys(self.uid)
            self.driver.find_element(By.ID,'fm-login-password').send_keys(self.upw)
            self.driver.find_element(By.TAG_NAME,"button").click()
            try:
                ActionChains(self.driver).click_and_hold(self.driver.find_element(By.ID,'nc_1_n1z')).perform()#按住滑块不动
                # ActionChains(self.driver).move_by_offset(xoffset=250, yoffset=0).perform()#直接到终点，可能速度太快，会被系统判错误操作
                for i in range(2):
                    ActionChains(self.driver).move_by_offset(xoffset=10, yoffset=0).perform()#再慢慢滑两步
                    sleep(0.1)
                ActionChains(self.driver).release().perform()#松开点击
                sleep(1)#滑完了之后稍等下，让系统判断完毕
                self.driver.find_element(By.TAG_NAME,"button").click()
                self.driver.switch_to.default_content()
            except Exception as exception:
                self.logger.error(exception)
        elif self.login_method==1:            
            if not os.path.exists('cookies.pkl'):#如果不存在cookie.pkl,就获取一下
                self.get_cookie()
            else:
                self.driver.get(damai_url)
                self.set_cookie()
     
    def enter_concert(self):
        print('###打开浏览器，进入大麦网###')
        # options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        self.driver=webdriver.Firefox()#默认火狐浏览器
        self.driver.maximize_window()
        self.login()#先登录再说
        self.driver.refresh()   
        try:
            locator = (By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/a[2]/div")
            element = WebDriverWait(self.driver, 3).until(EC.text_to_be_present_in_element(locator,self.usr_name))
            self.status=1
            print("###登录成功###")
        except:
            self.status=0
            print("###登录失败###")              
        if self.status==1:
            self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div[4]/input')[0].send_keys(self.name)#搜索栏输入歌星
            self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div[4]/div[1]')[0].click()#点击搜索
            try:    
                element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, 'category_filter_id')))
                kinds=element.find_elements(By.TAG_NAME,'li')#选择演唱会类别
                for k in kinds:
                    if k.text == '演唱会':
                        k.click()
                        break
            except Exception as exception:
                self.logger.error(exception)

            lists=self.driver.find_elements(By.ID,'content_list')[0].find_elements(By.TAG_NAME,'li')#获取所有可能演唱会
            titles=[]
            links=[]
            #注释的代码表示用图形界面手动选择演唱会，可以自行体会
    #        root = Tk()
    #        root.title("选择演唱会") 
    #        v = IntVar()
    #        v.set(1)
            self.choose_result=0
    #        def selection():
    #            self.choose_result=v.get()
    #            root.destroy()
            for li in lists:
                word_link=li.find_element(By.TAG_NAME,'h3')
                titles.append(word_link.text)
                temp_s=word_link.get_attribute('innerHTML').find('href')+6
                temp_e=word_link.get_attribute('innerHTML').find('target')-2
                links.append(word_link.get_attribute('innerHTML')[temp_s:temp_e])
                if li.find_element(By.TAG_NAME,'h3').text.find(self.place)!=-1:#选择地点正确的演唱会
                    self.choose_result=len(titles)
                    break
    #            b = Radiobutton(root,text = titles[-1],variable = v,value = len(titles),command=selection)
    #            b.pack(anchor = W)
    #        root.mainloop()
    #        while self.choose_result==0:
    #            sleep(1)
            self.url="https:"+links[self.choose_result-1]
            self.driver.get(self.url)#载入至购买界面
            self.status=2
            print("###选择演唱会###")
    
    def choose_ticket(self):
        if self.status==2:
            self.num=1#第一次尝试
            time_start=time.time() 
            while self.driver.title.find('订单结算')==-1:#如果跳转到了订单结算界面就算这部成功了
                if self.num!=1:#如果前一次失败了，那就刷新界面重新开始
                    self.status=2
                    self.driver.get(self.url)
                try:    
                    element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "performList")))
                    datelist = element.find_elements(By.TAG_NAME, 'li')
                    for i in self.date:  # 根据优先级选择一个可行日期
                        j = datelist[i - 1].get_attribute('class')
                        if j == 'itm':
                            datelist[i - 1].click()
                            sleep(1)
                            break
                        elif j == 'itm itm-sel':
                            break
                        elif j == 'itm itm-oos':
                            continue
                except Exception as exception:
                    print(exception)

                price_list=self.driver.find_element(By.ID,"priceList").find_elements(By.TAG_NAME,'li')#根据优先级选择一个可行票价
                for i in self.price:
                    j=price_list[i-1].get_attribute('class')
                    if j=='itm':
                        price_list[i-1].click()
                        sleep(2)
                        break
                    elif j=='itm itm-sel':
                        break
                    elif j=='itm itm-oos':
                        continue
                print("###选择演唱会时间与票价###")
                cart=self.driver.find_element(By.ID,'cartList')
                try:#各种按钮的点击
                    try:
                        cart.find_element(By.CLASS_NAME,'ops').find_element(By.LINK_TEXT,"立即预定").click()
                        self.status=3
                    except:
                        cart.find_element(By.CLASS_NAME,'ops').find_element(By.LINK_TEXT,"立即购买").click()
                        self.status=4
                except:
                    cart.find_element(By.CLASS_NAME,'ops').find_element(By.LINK_TEXT,"选座购买").click()
                    self.status=5
                self.num+=1
                try:
                    element = WebDriverWait(self.driver, 3).until(EC.title_contains('订单结算'))
                except:
                    print('###未跳转到订单结算界面###')                
            time_end=time.time()
            print("###经过%d轮奋斗，共耗时%f秒，抢票成功！请确认订单信息###"%(self.num-1,round(time_end-time_start,3)))
    
    def check_order(self):
        if self.status in [3,4,5]:
            print('###开始确认订单###')
            print('###默认购票人信息###')  
            rn_button=self.driver.find_elements(By.XPATH,'/html/body/div[3]/div[3]/div[2]/div[2]/div/a')
            if len(rn_button)==1:#如果要求实名制
                print('###选择实名制信息###')
                rn_button[0].click()
                #选择实名信息   
                try:
                    tb = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[12]/div')))
                    lb = tb.find_elements(By.TAG_NAME, 'label')[self.real_name]  # 选择第self.real_name个实名者
                    lb.find_elements(By.TAG_NAME, 'td')[0].click()
                    tb.find_element(By.CLASS_NAME, 'one-btn').click()
                except Exception as exception:
                    print("###实名信息选择框没有显示###")
                    print(exception)

            print('###默认选择付款方式###')
            print('###确认商品清单###')
            rn_button=self.driver.find_elements(By.XPATH,'/html/body/div[3]/div[3]/div[3]/div[2]/div[2]/div/div/h2/a[1]')
            if len(rn_button)==1:#如果要求实名制
                print('###选择购票人信息###')
                rn_button[0].click()
                #选择实名信息
                try:
                    tb = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[13]/div')))
                    lb = tb.find_elements(By.TAG_NAME, 'label')[self.real_name]  # 选择第self.real_name个实名者
                    lb.find_elements(By.TAG_NAME, 'td')[0].click()
                    tb.find_element(By.CLASS_NAME, 'one-btn').click()
                except Exception as exception:
                    print("###实名信息选择框没有显示###")
                    print(exception)

            print('###不选择订单优惠###')
            print('###请在付款完成后下载大麦APP进入订单详情页申请开具###')
            self.driver.find_element(By.ID,'orderConfirmSubmit').click()#同意以上协议并提交订单
            try:
                element = WebDriverWait(self.driver, 5).until(EC.title_contains('支付'))
                self.status=6
                print('###成功提交订单,请手动支付###')
            except Exception as exception:
                print('###提交订单失败,请查看问题###')
                print(exception)

    def finish(self):
        self.driver.quit()
                

if __name__ == '__main__':
    con=None
    try:
        con=Concert('张杰',[1],[2],'上海',1,method=0)#具体如果填写请查看类中的初始化函数
        con.set_account()
        con.enter_concert()
        con.choose_ticket()
        con.check_order()
    except Exception as e:
        print(e)
    finally:
        con.finish()
