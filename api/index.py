# -*- coding: UTF-8 -*-
import re, requests, json
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

'''
微博热搜爬取
'''


class WBO:
    def __init__(self):
        self.url = 'https://s.weibo.com/top/summary?cate=realtimehot'
        self.headers = {
            "Cookie": "SINAGLOBAL=2991298991739.324.1624166232383; SUB=_2AkMXhkisf8NxqwJRmfkVyWjgZYh0yAzEieKh2rl3JRMxHRl-yT9jqncjtRB6PAZmQxLGgpci2mPosQesVaFGF5U1Ro-W; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WW17gR2n9Dm9khJkkBaVpHl; UOR=,,www.google.com; _s_tentry=-; Apache=2652566463566.881.1634179765161; ULV=1634179765187:4:1:1:2652566463566.881.1634179765161:1629545690965; WBStorage=6ff1c79b|undefined",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        }

    def reqs(self):
        res = requests.get(self.url, headers=self.headers)
        res.encoding = 'utf8'
        hot_title = re.findall('<tr class="">(.*?)</tr>', res.text, re.S)
        hot_all_databae = []
        for index, item in enumerate(hot_title):
            hot_T = re.search(
                '<td class="td-02">(?P<Cnode>.*?)</td>', item, re.S)
            title = re.search(
                '<a href(|_to)="(?P<link>.*?)".*?>(?P<tit>.*?)</a>', hot_T.group('Cnode'), re.S)
            hot_I = re.search(
                '<td class="td-03"><i class="icon-txt icon-txt-\w+">(?P<hotI>.*?)</i></td>', item, re.S)
            hot_n = re.search('<span>(?P<CN>.*?)</span>',
                              hot_T.group('Cnode'), re.S)
            hot_N = '' if not hot_n else hot_n.group('CN')
            hot_status = '' if not hot_I else hot_I.group('hotI')
            res_obj = {
                "id": index + 1,
                "title": title.group('tit'),
                "link": title.group('link'),
                "hot_count": hot_N,
                "hot_status": hot_status
            }
            hot_all_databae.append(dict(res_obj))
        return hot_all_databae


'''
百度热搜爬取
'''


class BDU:
    def __init__(self):
        self.url = 'https://top.baidu.com/board?tab=realtime'

    def reqs(self):
        res = requests.get(self.url)
        html = BeautifulSoup(res.text, 'html.parser')
        content = html.find_all('div', attrs={'class': 'category-wrap_iQLoo horizontal_1eKyQ'})
        hot_all_databae = []
        for index, item in enumerate(content):
            a = item.select('.title_dIF3B')
            tit = item.select('.c-single-text-ellipsis')
            img = item.select('img')[0]['src']
            hot_count = item.select('.hot-index_1Bl1a')
            content = item.select('.hot-desc_1m_jR')[0].get_text()[:-6]
            res_obj = {
                "id": index + 1,
                "title": tit[0].get_text(),
                "link": a[0]['href'],
                "hot_count": hot_count[0].get_text(),
                "cover": img,
                'content': content
            }
            hot_all_databae.append(dict(res_obj))
        return hot_all_databae


class S_360:
    def __init__(self):
        self.url = 'https://trends.so.com/top/realtime'

    def reqs(self):
        res = requests.get(self.url)
        hot_all_search = []
        data = {
            "update": res.json()['data']['update'],
            "result": []
        }
        for index, item in enumerate(res.json()['data']['result']):
            item['link'] = 'https://www.so.com/s?ie=utf-8&src=zhishu&q=%s' % item['query']
            data['result'].append(item)
        hot_all_search.append(dict(data))
        return hot_all_search


# 监听路由
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = []
        path = self.path
        user = path.split('?tit=')[1]
        if user == 'wb':
            data = WBO().reqs()
        elif user == 'bd':
            data = BDU().reqs()
        elif user == '360':
            data = S_360().reqs()
        else:
            data.append({"message": "参数有误", "code": "-1"})
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return


