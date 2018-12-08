#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform;
import os;
import sys;
import httplib;
import urllib;
import urllib2;
import json;
import time;
import subprocess;
import requests;



# 把Cookie替换为自己的就可以了, 下面的ck参数也要改一下, 用Cookie中的ck参数替换
headers = {
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'Origin': 'https://douban.fm',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://douban.fm/mine/',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
    'Cookie': '<==  在这里填入你douban.fm的Cookie  ==>'}

################################################################################################################################################################################

# 解析cookie, 后面要用到ck参数
cookie = {}
for param in headers['Cookie'].split(';'):
    pair = param.replace(' ', '').split('=')
    cookie[pair[0]] = pair[1];

# 获取红心列表
resp = requests.get('https://douban.fm/j/v2/redheart/basic', headers=headers)
print resp.json()
print '-------------------------------------------------'
print '-------------------------------------------------'
sids=""
for song in resp.json()['songs']:
    if (sids != '') :
        sids += '|'
    sids += song['sid']
    #print song['playable'], song['sid']
body = 'sids=' + urllib.quote_plus(sids) + '&kbps=192&ck=' + cookie['ck']
print body
print '-------------------------------------------------'
print '-------------------------------------------------'

# 休息2秒之后再请求，免得被频率限制挡掉
time.sleep(5)

# 获取每首歌的url
resp = requests.post('https://douban.fm/j/v2/redheart/songs', data=body, headers=headers);
print resp.status_code, resp.text
for song in resp.json() :
    #print 'sid[' + song['sid'] + '] artist[' + song['artist'] + '] title[' + song['title'] + '] url[' + song['url'] + ']'
    cmd = 'wget ' + song['url'] + ' -O "' + song['artist'] + '_' + song['title'] + '.mp3"'
    print cmd
    subprocess.call(cmd, shell=True)
    pic = 'wget ' + song['picture'] + ' -O "' + song['artist'] + '_' + song['title'] + '.jpg"'
    print pic
    subprocess.call(pic, shell=True)

exit(0)

#
