#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

Hostreferer = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Host': 'www.mzitu.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.mzitu.com'
}


def get_html(url):  # 获得页面html代码
    req = requests.get(url, headers=Hostreferer, timeout=20)
    return req.text


def getAllWords():
    alltext = ""
    html = get_html("https://www.mzitu.com/")
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.find_all("a", attrs={"class": "page-numbers"}))
    all_pages = int(
        (soup.find_all("a", attrs={"class": "page-numbers"}))[3].contents[0])  # 获取总概览页面数
    page_range = range(1, all_pages + 1, 1)

    for which in page_range:
        html = get_html("https://www.mzitu.com/page/" + str(which) + "/")
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find_all("div", attrs={"class": "postlist"})
        href = div[0].find_all("a", attrs={"target": "_blank"})
        href_range = range(0, len(href), 1)
        for i in href_range:
            if i % 2 == 0:
                continue
            alltext = alltext + " " + href[i].text
        # time.sleep(1)
        # print("第" + str(which) + "页")

    # returned is a generator
    return jieba.cut(alltext)


def main():
    alltext = " ".join(getAllWords())
    # with open("mmdesc.txt", "w") as f:
    #    f.write(alltext)
    # print(alltext)
    wordcloud = WordCloud(
        font_path="c:/windows/fonts/simfang.ttf",
        background_color="black",
        width=800,
        height=600
    ).generate(alltext)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    main()
