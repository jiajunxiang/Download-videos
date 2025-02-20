from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time
import json


class Taobao(object):
    def __init__(self):
        # 登入以下网址即可直接跳转到购物车
        self.url = 'https://cart.taobao.com/cart.htm?'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()
    # 自动登录
    def login(self):
        # 获取保存下的cookie值
        with open('taobao_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        # 往browser里添加cookies
        for cookie in listCookies:
            cookie_dict = {
                'domain': '.taobao.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            self.driver.add_cookie(cookie_dict)

        self.driver.refresh()

        # 等待快速登录按钮出现并点击
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="fm-btn"]/button'))
        )
        self.driver.find_element(By.XPATH, '//div[@class="fm-btn"]/button').click()

    def shopping_cart(self):

            # 设定时间等待，等到时间到了立即开抢
        startTime = datetime.datetime(2022, 11, 10, 20, 0, 1)
        print('正在等待开抢...')
        while datetime.datetime.now() < startTime:
            time.sleep(1)

        # 点击全选
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="J_SelectAll1"]'))
        )
        self.driver.find_element(By.XPATH, '//div[@id="J_SelectAll1"]').click()

        # 等待结算按钮出现后点击
        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@id="J_Go"]'))
        )
        self.driver.find_element(By.XPATH, '//a[@id="J_Go"]').click()
        time.sleep(0.5)
        try:
            self.driver.find_element(By.XPATH, '//a[@id="J_Go"]').click()
        except:
            pass

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.LINK_TEXT, '提交订单'))
        )
        # 等待“提交订单”元素加载完毕后点击
        self.driver.find_element(By.LINK_TEXT, '提交订单').click()

    def run(self):
        self.login()
        self.shopping_cart()


taobao = Taobao()
taobao.run()




