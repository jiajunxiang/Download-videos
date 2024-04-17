#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/11/17/017 14:32
import asyncio
import os
import re
import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES

count = 1
def get_iframe_src(url):
    resp=requests.get(url)
    resp.encoding='utf-8'
    resp.close()
    soup=BeautifulSoup(resp.text,"html.parser")
    result=soup.find('iframe')
    src=result.get('src')
    return str(src)

def get_first_m3u8_url(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    resp.close()
    obj=re.compile(r'RESOLUTION=960x540(?P<first_m3u8_url>.*)', re.S)
    result=obj.search(resp.text)
    return result.group('first_m3u8_url').strip()

def get_key_url():
    s=''
    obj = re.compile(r'URI="(?P<key_url>.*?)"', re.S)
    with open('1.txt',mode='r',encoding='utf-8') as file:
        for line in file:
            s+=line
    file.close()
    result=obj.search(s)
    return result.group('key_url').strip()

def get_key(url):
    resp=requests.get(url)
    return resp.text.encode('utf-8')



def download_m3u8_file(url,name):
    resp = requests.get(url)
    with open(name,mode='wb') as f:
        f.write(resp.content)
    resp.close()

def merge_ts():
    #copy /b temp*.ts new.mp4
    s='copy /b F:\\pythonProject\\video\\*.ts new.mp4'
    print(s)
    os.system(s)

async def download_ts(url, name, session):
    async with session.get(url) as resp:
        # 创建一个新文件夹 movie_ts 并设置为 excluded，下载过程将不占用 pycharm 缓存
        async with aiofiles.open(f'video/{name}.ts', mode='wb') as file:
            # 将下载到的内容写入到文件中
            await file.write(await resp.content.read())
    print(f"第{name}个片段下载完毕")


async def aio_download():
    tasks=[]
    global count
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open('dianshiju.txt',mode='r',encoding='utf-8') as file:
            async for line in file:
                # 去掉前面带 # 的非 ts 数据
                if line.startswith('#'):
                    continue
                # 去掉空格和换行
                ts_url = line.strip()
                # 创建异步任务
                task = asyncio.create_task(download_ts(ts_url, count, session))
                tasks.append(task)
                count = count + 1
            # 等待任务结束
            await asyncio.wait(tasks)
            print(f'全部{count-1}个ts文件下载完毕！')

async def des_ts(name,key):
    aes=AES.new(key=key,IV=b'0000000000000000',mode=AES.MODE_CBC)
    async with aiofiles.open(f'video/{name}.ts', mode='rb') as file1,\
        aiofiles.open(f'video/temp{name}.ts', mode='wb') as file2:
        bs=await file1.read()#从源文件读取内容
        des_content=aes.decrypt(bs)
        await file2.write(des_content)#把解密好的内容写入完毕
    print(f'{name}解密处理完毕！')




async def aio_dec(key):
    tasks = []
    for i in range(1,count):
        task=asyncio.create_task(des_ts(i,key))
        tasks.append(task)
    # 等待任务结束
    await asyncio.gather(*tasks)


def main(url):
    # 1.拿到主页面的源代码，找到iframe对应的url
    iframe_url=get_iframe_src(url).split('=')[1]
    print(iframe_url)
    # 2.拿到第一层真实m3u8的地址
    first_m3u8_url=get_first_m3u8_url(iframe_url)
    real_first_m3u8_url=iframe_url.split('/2022')[0]+first_m3u8_url
    print(real_first_m3u8_url)
    # 3.根据真实m3u8的地址下载保存
    download_m3u8_file(real_first_m3u8_url,'dianshiju.txt')
    # 4.下载ts片段视频
    asyncio.run(aio_download())
    # 7.合并视频
    merge_ts()

if __name__ == '__main__':
    url='http://www.wwmulu.com/rj/poshijingying/play-1-1.html'
    main(url)