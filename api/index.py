# -*- coding: UTF-8 -*-
import re
import requests
import json
from http.server import BaseHTTPRequestHandler

'''
微博热搜爬取
'''


class WBO:
    def __init__(self):
        self.url = 'https://s.weibo.com/top/summary?cate=realtimehot'

    def reqs(self):
        res = requests.get(self.url)
        res.encoding = 'utf8'
        hot_title = re.findall('<tr class="">(.*?)</tr>', res.text, re.S)
        hot_all_databae = []
        for index, item in enumerate(hot_title):
            hot_T = re.search(
                '<td class="td-02">(?P<Cnode>.*?)</td>', item, re.S)
            title = re.search(
                '<a href(|_to)="(?P<link>.*?)".*?(?P<tit>.*?)</a>', hot_T.group('Cnode'), re.S)
            hot_I = re.search(
                '<td class="td-03"><i class="icon-txt icon-txt-\w+">(?P<hotI>.*?)</i></td>', item, re.S)
            hot_n = re.search('<span>(?P<CN>.*?)</span>',
                              hot_T.group('Cnode'), re.S)
            hot_N = '' if not hot_n else hot_n.group('CN')
            hot_status = '' if not hot_I else hot_I.group('hotI')
            res_obj = {
                "id": index+1,
                "title": title.group('tit'),
                "link": title.group('link'),
                "hot_count": hot_N,
                "hot_status": hot_status
            }
            hot_all_databae.append(dict(res_obj))
        return hot_all_databae


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = []
        path = self.path
        user = path.split('?tit=')[1]
        if user == 'wb':
            data = WBO().reqs()
        else:
            data.append({"message": "参数有误", "code": "-1"})
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return
