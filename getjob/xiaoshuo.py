# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 19:38:03 2018

@author: Python
"""

import re
import time
import requests


def get_one_page(url):
    headers = {"User-Agent": "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        #        print(response.content.decode('utf-8'))
        return response.content.decode('utf-8')
    return None


# def parse_one_page(html):
#    data = json.loads(html)
#    print(data)
def parse_one_page(html,m):
    pattern = re.compile('<div id="content">(\s\S*)')
    #    print(html)
    items = re.findall(pattern, html)
    m=m-107463
    zhengze = re.compile('第'+str(m)+'章(\s\S*)')
    print(zhengze)
    title = re.findall(zhengze,html)
    print(items[0])
    print(title[1][:-1])

    pattern = re.compile('<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;')
    p1 = re.subn(pattern, '\r\n', items[0], 10000)
    pattern = re.compile('&nbsp;&nbsp;&nbsp;&nbsp;')
    p2 = re.subn(pattern, '', p1[0], 10000)

    a = '第'+str(m)+'章'+ title[1][:-1]+'.txt'
    with open('./note/'+a,'a')as f:
       f.write(p2[0])
    pattern = re.compile('<div id="content">([\w\W]*)')
    p = re.findall(pattern,p1[0])
def main():
    Nzhang =0
    while Nzhang <=10:
        diyi = 107464
        Hzhang= diyi+Nzhang
        url='https://www.biquke.com/bq/22/22585/'+str(Hzhang)+'.html'
        parse_one_page(get_one_page(url),Hzhang)
        Nzhang+=1
if __name__=="__main__":
    main()
