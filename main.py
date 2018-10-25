from lxml import html
import json
import os
import requests
import time

uid = '679c9c872529348a37' # uid of my father

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'}

def download_file(url, name):
    if os.path.isfile(name):
        print('skip')
        return
    r = requests.get(url, stream=True, headers=headers)
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)


url = 'https://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage'

data = {
    'jsonpCallback': 'callback_1',
    'g_tk': '5381',
    'outCharset': 'utf-8',
    'format': 'jsonp',
    'type': 'get_ugc',
    'start': 1,
    'num': '8',
    'touin': '',
    'share_uid': uid,
    'g_tk_openkey': '5381',
    '_': 1540453164802
}

while True:
    print('starting page {}'.format(data['start']))
    data['_'] = int(time.time() * 1000)
    c = requests.get(url, headers=headers, params=data)
    text = c.text[len('callback_1('):-1]
    j = json.loads(text)
    if j['code'] != 0:
        print('code error!!!')
        print(c.text)
        break

    if j['data']['has_more'] <= 0:
        print('done')
        break

    for i in j['data']['ugclist']:
        share_id = i['shareid']
        url_play = 'https://node.kg.qq.com/play?s={}&g_f=personal'.format(share_id)
        r = requests.get(url_play, headers=headers)
        tree = html.fromstring(r.text)
        script = tree.xpath('/html/body/script[1]/text()')[0]
        json_str = script[len('window.__DATA__ = '): -2]

        ja = json.loads(json_str)
        link = ja['detail']['playurl']
        name = ja['detail']['song_name']

        print('downloading {}'.format(name))

        download_file(link, name+'.m4a')

    data['start'] = data['start'] + 1


