#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/11/16/016 20:44
import datetime
import re
import time

import aiofiles
import aiohttp
import requests

header={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        'Connection': 'close',

}
proxie = {
    "https": "59.110.7.43:3129",
    "http": "59.110.7.43:3129",
}
def send_url(u,method,data=None):
    if method=='GET':
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        res=requests.get(url=u,headers=header)
        #print(res.status_code)  # 如果代理可用则正常访问，不可用报以上错误
        res.close()
        return res
    else:
        res=requests.post(url=u,headers=header,proxies=proxie)
        print(res.status_code)  # 如果代理可用则正常访问，不可用报以上错误
        res.close()
        return res
"""
url='https://www.puerth.com/vodplay/74499-1-1.html'
obj=re.compile(r'<div class="stui-player__video clearfix">.*?"url":"(?P<url>.*?)"',re.S)
html=send_url(url,'GET').text
#print(html)
result=obj.search(html)
url1=result.group('url').replace('\\','')
print(url1)

url2=send_url(url1,'GET').text.split("\n")[2]
print(url2)

m3u8_url=url1[:21]+str(url2)
print(m3u8_url)

with open('镇魂街.m3u8',mode='wb') as f:
    f.write(send_url(m3u8_url,'GET').content)

"""
n=1
with open('镇魂街.m3u8',mode='r',encoding='utf-8') as f:
    print('开始时间：')
    t1=datetime.datetime.now()
    for l in f:
        line=l.strip()
        if line.startswith('#'):
            continue
        print(line)
        resp = requests.get(line)
        f=open(f"video/{n}.ts",mode='wb')
        f.write(resp.content)
        n+=1
        print(f'完成第{n}个片段！')
    f.close()
    print('结束时间：')
    t2=datetime.datetime.now()
    print('总耗时：'+t2-t1)
