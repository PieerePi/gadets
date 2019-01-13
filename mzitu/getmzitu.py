#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys
import os
import re
import traceback
import io

Hostreferer = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Referer': 'https://www.mzitu.com'
}

Picreferer = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Referer': 'https://i.meizitu.net'
}

continued_transfer = 0  # 图集已经存在并下载完成，后续图集仍继续下载；当程序非正常退出时，需要加上此选项

reversed_transfer = 0  # 从最后一个图集开始下载；缺省是从第一个图集开始下载


def get_mm_info(url):  # 获得图集最大页数和名称
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    span = soup.find_all('span')
    title = soup.find('h2', attrs={"class": "main-title"})
    div = soup.find('div', attrs={"class": "main-image"})
    img_url = div.find('img') if div else None
    for i in range(0, len(span), 1):
        if span[i].text.find('下一页') != -1:
            return span[i-1].text, title.text, img_url['src'] if img_url else None
    return span[10].text, title.text, img_url['src'] if img_url else None


def get_html(url):  # 获得页面html代码
    req = requests.get(url, headers=Hostreferer, timeout=20)
    return req.text


def get_img_url(url):  # 获取图片URL
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', attrs={"class": "main-image"})
    img_url = div.find('img') if div else None
    return img_url['src'] if img_url else None


def save_img(img_url, count, dir):  # 下载并保存图片
    if os.access(dir+'/'+str(count)+'.jpg', os.F_OK):
        print('第 ' + str(count) + ' 张图片已经存在')
        return 200
    req = requests.get(img_url, headers=Picreferer, timeout=20)
    if req.status_code != 200:
        return req.status_code
    with open(dir+'/'+str(count)+'.jpg', 'wb') as f:
        f.write(req.content)
        print('保存第 ' + str(count) + ' 张图片成功')
    return 200


def get_imgdir_count(dir):  # 获取目录中图片的数目
    imgs = 0
    for _, _, files in os.walk(dir):
        imgs = len(files)
        break
    return imgs


def download_onemm(mmhome_url):  # 下载一个图集
    page, mm_dir_name, first_img_url = get_mm_info(mmhome_url)
    # 目录名中包含有特殊字符"\ / : * ? " < > |"，替换为下划线
    mm_dir_name = re.sub(r'[\/:*?"<>|]', '_',
                         mm_dir_name+'_'+mmhome_url.split('/')[-1])
    count = 0

    if not os.path.exists('images/' + mm_dir_name):
        os.mkdir('images/' + mm_dir_name)
        print('创建新目录 \'' + mm_dir_name + '\'')
    else:
        count = get_imgdir_count('images/' + mm_dir_name)
        if count >= int(page):
            print('目录 \'' + mm_dir_name + '\' 已经存在，并已经下载完成')
            return -1
        else:
            print('目录 \'' + mm_dir_name + '\' 已经存在，但未下载完成，继续下载')

    if int(page) >= 100:
        print('目录 \'' + mm_dir_name + '\' 有超过100张图片: ' + page)
        with open('劲爆图集（大于100张）.txt', 'a', encoding='utf-8') as f:
            f.write(mm_dir_name + '\n')

    k = 1
    for k in range(1, int(page)+1, 1):
        if os.access('images/'+mm_dir_name+'/'+str(k)+'.jpg', os.F_OK):
            if k == int(page):
                return 0
            continue
        if int(page) >= 100:
            new_img_url = first_img_url[:-7] + \
                '{0:03d}'.format(k) + first_img_url[-4:]
        else:
            new_img_url = first_img_url[:-6] + \
                '{0:02d}'.format(k) + first_img_url[-4:]
        # print(new_img_url)
        if new_img_url and (new_img_url.startswith('http://') or new_img_url.startswith('https://')):
            ret = save_img(new_img_url, k, 'images/' + mm_dir_name)
            if ret != 200:
                print(new_img_url + " of '" + mm_dir_name +
                      "' " + str(k) + "_th 无法下载,新,返回码" + str(ret))
                break
        else:
            print(mmhome_url + "/" + str(k) +
                  " of '" + mm_dir_name + "' 无法下载,新")
        if k == int(page):
            return 0

    print('使用笨办法下载')
    for i in range(k, int(page)+1, 1):
        if os.access('images/'+mm_dir_name+'/'+str(i)+'.jpg', os.F_OK):
            continue
        new_img_url = get_img_url(mmhome_url + "/" + str(i))
        # print(new_img_url)
        if new_img_url and (new_img_url.startswith('http://') or new_img_url.startswith('https://')):
            ret = save_img(new_img_url, i, 'images/' + mm_dir_name)
            if ret != 200:
                print(new_img_url + " of '" + mm_dir_name +
                      "' " + str(i) + "_th 无法下载,旧,返回码" + str(ret))
        else:
            print(mmhome_url + "/" + str(i) +
                  " of '" + mm_dir_name + "' 无法下载,旧")

    return 0


def download():
    html = get_html("https://www.mzitu.com/")
    soup = BeautifulSoup(html, 'lxml')
    all_pages = int(
        (soup.find_all("a", attrs={"class": "page-numbers"}))[3].contents[0])  # 获取总概览页面数
    page_range = range(1, all_pages+1, 1)
    if reversed_transfer == 1:
        page_range = range(all_pages, 0, -1)

    try:
        os.mkdir('images')
    except:
        pass

    for which in page_range:
        html = get_html("https://www.mzitu.com/page/" + str(which) + "/")
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find_all("div", attrs={"class": "postlist"})
        href = div[0].find_all("a", attrs={"target": "_blank"})
        href_range = range(0, len(href), 1)
        if reversed_transfer == 1:
            href_range = range(len(href)-1, -1, -1)

        for i in href_range:  # 下载一个概览页面中的24个图集
            if i % 2 == 1:  # 有重复，去掉一个
                continue
            try:
                ret = download_onemm(href[i].attrs['href'])
            except Exception as e:
                print(href[i].attrs['href'] + ' 下载失败\n')
                traceback.print_exc(file=sys.stdout)
                with open('下载失败.txt', 'a', encoding='utf-8') as f:
                    f.write(href[i].attrs['href'] + '\n')
                continue
            if ret == -1:
                if continued_transfer == 1:
                    continue
                else:
                    return


def download_failed():
    failed_list = []
    if not os.access('下载失败.txt', os.R_OK):
        return
    for line in open('下载失败.txt', 'r', encoding='utf-8'):
        failed_list.append(line.rstrip())
    os.remove('下载失败.txt')
    failed_list = list(set(failed_list))  # 去重
    failed_list.sort()
    if reversed_transfer == 0:
        failed_list.reverse()
    for i in range(0, len(failed_list), 1):
        try:
            download_onemm(failed_list[i])
        except Exception as e:
            print(failed_list[i] + ' 仍然下载失败\n')
            traceback.print_exc(file=sys.stdout)
            with open('下载失败.txt', 'a', encoding='utf-8') as f:
                f.write(failed_list[i] + '\n')
            continue


def main():
    global continued_transfer
    global reversed_transfer

    # 防止print打印出错，有可能缺省是cp936的输出，不支持韩文"韩国美女写真박시현"
    if str(type(sys.stdout)) == "<class '_io.TextIOWrapper'>" and sys.stdout.encoding.upper() != 'UTF-8':
        print('set stdout encoding to utf-8')
        sys.stdout.flush()
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding='utf-8', line_buffering=True)

    for arg in sys.argv[1:]:
        if arg == '-f':
            if not os.access('下载失败.txt', os.R_OK):
                print('getmzitu: 没有失败图集供下载，下载工作全部完成！')
                sys.exit()
            download_failed()
            print('getmzitu: 下载失败图集工作全部完成！')
            sys.exit()
        elif arg == '-c':
            continued_transfer = 1
        elif arg == '-r':
            reversed_transfer = 1
        elif arg == '-h':
            print('''命令行用法: getmzitu [-f] [-c] [-r] [-h]
             -f 仅下载失败图集
             -c 图集已经存在并下载完成，后续图集仍会检查或下载；当程序非正常退出时，需要加上此选项
             -r 从最后一个图集开始下载；缺省是从第一个图集开始下载
             -h 打印此帮助信息''')
            sys.exit()

    download()
    download_failed()

    print('getmzitu: 下载工作全部完成！')
    input('Press any key to continue...')


if __name__ == '__main__':
    main()
