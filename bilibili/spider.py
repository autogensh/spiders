# -*- coding: utf-8 -*-
import json as JSON
import time
import os
from urllib import request
import gzip


def process(html):
    print(html)
    json = JSON.loads(html)
    for item in json['data']['items']:
        for i, pic in enumerate(item['pictures']):
            time.sleep(2)
            doc_id = item['doc_id']
            imgurl = pic['img_src']
            ext = os.path.splitext(imgurl)[1]
            title = item['title']
            if (title == ''):
                title = item['description']
            filename = '%d_%s%s' % (doc_id, title, ext)
            print('downloading image: %s ...' % filename)
            imgreq = request.Request(imgurl, headers=headers)
            imgres = request.urlopen(imgreq)
            with open('./images/' + filename, 'wb') as imgfile:
                imgfile.write(imgres.read())
                imgfile.flush()
                imgfile.close()
            print('downloading succeed')


if __name__ == '__main__':
        
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://space.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Referer': 'https://space.bilibili.com/6823116/album',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5',
    }

    for i in range(0, 8):
        if i == 2:
            continue
        url = r'https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid=6823116&page_num=%d&page_size=30&biz=all' % i
        req = request.Request(url, headers=headers)
        print('processing: ' + url)
        res = request.urlopen(req)
        html = gzip.decompress(res.read()).decode("utf-8")
        process(html)
        print()
        print('=======================================================-===================')
        print()
