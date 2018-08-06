import requests
from requests.exceptions import RequestException
import re
from pyquery import PyQuery
from multiprocessing import Pool
import os

CHAPTER_ID = 0

def get_page(url, n):
    if n == 0:
        print('*' * 10)
        return None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = 'gbk'
    except Exception as e:
        print(e)
        get_page(url, n-1)
    # print(response.status_code)
    return response.text


def parse_catalog(html):
    pattern = re.compile('<dd><a href="(.*?)">.*?</a></dd>', re.S)
    items = re.findall(pattern, html)
    L = []
    for item in items:
        L.append(item)
    return L


def parse_content(html):
    doc = PyQuery(html)
    title = doc('h1').text()
    # print(title)
    content = doc('#content').text()
    # print(content)
    yield title, content


def write_to_file(title, content, chapter):
    with open('飞剑问道/%s.txt' % chapter, 'w', encoding='utf-8') as f:
        f.write(title + '\n' + content +'\n')
        print(title)


def sum_file(a):
    L = []
    for i in range(1,a+1):
        try:
            with open('飞剑问道/%s.txt' % i, 'r') as f:
                s1 = f.read()
            L.append(s1)
            # print(L)
        except Exception as e:
            print(e)
    # print(L)
    with open('飞剑问道.txt', 'a', encoding='utf-8') as f:
        for i in L:
            f.write(i)


def proxy(url,a):
    html = get_page(url, 10)
    for title, content in parse_content(html):
        write_to_file(title, content, a)    
 

def main():
    p = Pool(4)
    url = 'http://www.biquge.com.tw/17_17503/'
    html = get_page(url, 10)
    a=0
    for catalog in parse_catalog(html):
        a+=1
        p.apply_async(proxy,args=(url+catalog[10:],a))
    p.close()
    p.join()
    sum_file(a)
        

if __name__ == '__main__':
    main()
