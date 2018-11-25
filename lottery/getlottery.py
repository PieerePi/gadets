import urllib.request
from bs4 import BeautifulSoup
import json

old_data_list = []
data_list = []

all_pages = 0
which = 1

lastest_issue = 0
new_issues = 0

try:
    with open('lottery.json', 'r') as f:
        old_data_list = json.load(f)
        f.close()
    lastest_issue = 0 if len(old_data_list) == 0 else int(
        old_data_list[0]['issue'])
    print('The lastest issue in DB is ' + str(lastest_issue) + '.')
except IOError as e:
    lastest_issue = 0

while True:
    #url = "http://kaijiang.zhcw.com/zhcw/html/ssq/list" + ("" if which == 1 else "_"+ str(which)) + ".html"
    url = "http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=" + \
        str(which)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "lxml")
    if which == 1:
        all_pages = int(((soup.find_all("p", attrs={"class": "pg"})[
                        0]).find_all("strong")[0]).get_text())
        print('Total page online is ' + str(all_pages) + '.')
    print('  - Start downloading page ' + url)
    trs = soup.find_all("tr")
    for tr in trs[2:-1]:
        tds = tr.find_all("td")
        ems = tds[2].find_all("em")
        if int(tds[1].get_text()) <= lastest_issue:
            all_pages = 0  # 停止往下抓取网页和存入新的期数
            break
        data_list.append({
            'date': tds[0].get_text(),
            'issue': tds[1].get_text(),
            'r1': ems[0].get_text(),
            'r2': ems[1].get_text(),
            'r3': ems[2].get_text(),
            'r4': ems[3].get_text(),
            'r5': ems[4].get_text(),
            'r6': ems[5].get_text(),
            'blue': ems[6].get_text()
        })
        new_issues = new_issues + 1
    which = which + 1
    if which > all_pages:
        break

if new_issues != 0:
    data_list.extend(old_data_list)
    json.dump(data_list, open('lottery.json', 'w'))

print('Done! Totally ' + str(new_issues) + ' issues added!')
