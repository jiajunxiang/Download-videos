#!/usr/bin/env python
# -*- coding: utf-8 -*-
#根据m3u8文件直接下载视频而且视频没有加密
# @Time : 2023/1/11/011 17:23
import asyncio
import os
import re
import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES

count = 1

def download_m3u8_file(url,name):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    resp = requests.get(url,headers=header)
    print(resp.status_code)
    with open(name,mode='wb') as f:
        f.write(resp.content)
    resp.close()

def merge_ts():
    #copy /b temp*.ts new.mp4
    s='copy /b F:\\pythonProject\\video\\temp*.ts 去风的地方.mp4'
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



if __name__ == '__main__':
    url='https://pcvideotestws.titan.mgtv.com/c1/2023/01/04_0/AD664E6648838648B173611C0656C7AD_20230104_1_1_1049_mp4/14CDA3DADCDFFF116BB2354FFFD63ED3.m3u8?arange=0&pm=mXd5j3J7iCvBZIIlkSwXoMn31JuYry02xHINz8WG7~NGfv8B7FG_5ve_ZSz~ZNIf5BPxB2sEXaKS5c1ymHpt2uAmC5c0CUt~B9oBQJz4BA~6itjEgJG4ttVPsFKz8Hak8wuwow7EAirnZoqOcaKKS_H9qmUM1LUFON2gQpFINvWScQAEvRRtYvp9WhwVDTgXlQWwvFZiujgVbh5IpRKhwfLjzjVOB3J5wsIva1owCmakfEguW4D51r7QBpXuSXip6gK3iZ6NESU~3ECtCxgNq20tqXMD50Q0Nu8j7f9DzHbL4QxpiLebC1OtfabH3w6F~ijWFpMQSJRh0C_k5Au2fnSqeQJIZTEEjzhdC2Go2uJTal0Cem7M2tAVZ9H4Dcf4kIXO8Z4Vr9Qzuw6iPbTymJyof6w_RnpxURxl~0TujPNPo_dWAIjQUYW5YcYIkejy&mr=dBq8vUWjGHv4nj28~fFxJ8XEWtOSmPYw4ifl33Gw~JxF1grQsDT8qa5y2al2yAugWubyxG3UPr1hxjnYScYFUz_hDVHWoDOOzlOW5XbKIZoHmYmBgc16zE2gQhbCjGzXVBoy3DpJ5MBy7qnLtMM6CEQMkRGMrXvwvq51NXagHPP33IwxHnZNwN7kK3FKuCI3AK4Bx9bO0yMHRG3c26h7XHW85LF8_12hv8pts2yHmFLa9BP7mGozLKNGGOn2gmY_Im7cYC5minKTxHrOTRCAM0Zqz7JJQifF0wW2YM_V_XTEHM8cqMnNm0J4LWmtDIjjYJowFZJEH1ouTxK9hy_yvKCFygzKkZ2gw0XZ6DFYVzQwph3j7Usr0GfXlgpKDwvMLK~P2L9lcRn42IPTgQCqBGw91tNXMy9sz4LvBteQIfLZvpXhgHfi9AV2PZwyeVLCEYnyIq~mdoEnUv3Jzj_Vxjj9QxW44Zko1Ave4qO~nnb8IpOcPxGZJdTrgkbt88NjlkR5T_3FFeIVe7StX2SS1GojvIKOsur6bVvvF_7mVWc_cWHxc1NvTMuuFDT2zboHHKRbg4nQt6iYpN0PNKes4Za2I8FiMGzLs4d7AaINTq5iWQNAcMEdPhBpwjUL0vJ3pr27j7ViMK8LFPR7~7QuUg--&uid=null&scid=25060&cpno=6i06rp&ruid=aaf6f62edd0f4921&sh=1'
    # 1.拿到真实m3u8的地址
    download_m3u8_file(url, 'dianshiju.txt')
    # # 2.下载ts片段视频
    # asyncio.run(aio_download())
    # # 3.合并视频
    # merge_ts()