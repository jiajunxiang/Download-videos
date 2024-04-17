#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/11/16/016 20:44
#根据m3u8文件下载ts切片
import asyncio
import aiofiles
import aiohttp


async def download_ts(url, name, session):
    async with session.get(url) as resp:
        # 创建一个新文件夹 movie_ts 并设置为 excluded，下载过程将不占用 pycharm 缓存
        async with aiofiles.open(f'movie_ts/{name}.ts', mode='wb') as file:
            # 将下载到的内容写入到文件中
            await file.write(await resp.content.read())
    print(f"第{name}个片段下载完毕")


async def download_movie():
    tasks = []
    n=1
    # 从 m3u8 文件中获取每个 ts 文件的下载地址
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open('镇魂街.m3u8', mode='r', encoding='utf-8') as f:
            async with aiofiles.open("movie_ts/movie.txt", mode='w', encoding='utf-8') as file:
                async for line in f:
                    # 去掉前面带 # 的非 ts 数据
                    if line.startswith('#'):
                        continue
                    # 去掉空格和换行
                    ts_url = line.strip()
                    # 更改路径
                    ts_path = f"file F:/pythonProject/movie_ts/{n}.ts"
                    await file.write(ts_path + "\n")
                    # 创建异步任务
                    task = asyncio.create_task(download_ts(ts_url, n, session))
                    tasks.append(task)
                    n=n+1
        # 等待任务结束
            await asyncio.wait(tasks)




if __name__ == '__main__':
    asyncio.run(download_movie())
    print('爬取完毕!')