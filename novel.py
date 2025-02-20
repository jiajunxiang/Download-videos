#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/11/15/015 22:24
import json
import aiofiles
import aiohttp
import asyncio
import requests

"""
1.同步操作：访问getCatalog拿到所有章节的name和cid
https://dushu.baidu.com/api/pc/getDetail?data={"book_id":"4306063500"}
2.异步操作：访问getChapterContent下载所有的文章内容
https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":1}
"""
async def getCatalog(url):
    resp=requests.get(url)
    result=resp.json()
    resp.close()
    for item in result['data']['novel']['items']:#items就是对应每一个章节的name和cid
        title=item['title']
        cid=item['cid']
        tasks=[
            asyncio.create_task(getChapterContent(cid,book_id,title))
        ]
    await asyncio.wait(tasks)

async def getChapterContent(cid,book_id,title):
    data={
        "book_id": book_id,
        "cid": f"{book_id}|{cid}",
        "need_bookinfo": 1
    }
    data=json.dumps(data)
    url='https://dushu.baidu.com/api/pc/getChapterContent?data='+data
    print(url)
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as response:
            result=await response.json()
            content = result['data']['novel']['content']
            async with aiofiles.open(f"西游记/{title}.txt",mode='w',encoding='utf-8') as f:
                await f.write(content)


if __name__ == '__main__':
    book_id='4306063500'
    url='https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"'+book_id+'"}'
    asyncio.run(getCatalog(url))
    print('爬取西游记小说完毕!')