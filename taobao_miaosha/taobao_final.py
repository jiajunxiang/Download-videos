import  datetime
import  time
import  pyttsx3
from selenium import  webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


sound=pyttsx3.init()
#语速控制默认200
sound.setProperty('rate',150)
#音量控制范围0.0~1.0
sound.setProperty('volume',1)

#秒杀时间
times='2022-11-03 18:06:10'
s = ChromeService(executable_path=ChromeDriverManager().install())
browser=webdriver.Chrome(service=s)
browser.maximize_window()#窗口最大化
browser.get('http://www.taobao.com')
time.sleep(2)#缓冲
browser.find_element(By.LINK_TEXT,'亲，请登录').click()
print("请扫码")
time.sleep(15)#缓冲
browser.get('https://cart.taobao.com/cart.htm')
time.sleep(5)#缓冲

#是否全选购物车
while 1==1:
    if(browser.find_element(By.ID,'J_SelectAll1')):
        browser.find_element(By.ID, 'J_SelectAll1').click()
        break
while 1==1:
    #获取电脑现在的时间
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(now)
    #判断是不是到了秒杀时间
    if now>times:
        #点击结算按钮
        while 1==1:
            try:
                if(browser.find_element(By.LINK_TEXT,'结 算')):
                    print('here')
                    browser.find_element(By.LINK_TEXT,'结 算').click()
                    print("主人，结算提交成功，我已经帮你抢到商品了，请及时支付订单")
                    sound.say("主人，结算提交成功，我已经帮你抢到商品了，请及时支付订单")
                    sound.runAndWait()
                    break
            except:
                pass
        #点击提交订单按钮
        while 1==1:
            try:
                if browser.find_element(By.CLASS_NAME,'go-btn'):
                    print('提交订单成功！')
                    browser.find_element(By.CLASS_NAME,'go-btn').click()
                    sound.say("宝贝已抢到，请等待收货")
                    sound.runAndWait()
                    break
            except:
                pass


