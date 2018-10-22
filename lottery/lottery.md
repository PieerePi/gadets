## 双色球开奖结果抓取

### 用法

```
>python getlottery.py
Total page online is 117.
  - Start downloading page http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=1
  - ...
  - Start downloading page http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=117
Done! Totally 2328 issues added!

>python getlottery.py
The lastest issue in DB is 2018122.
Total page online is 117.
  - Start downloading page http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=1
Done! Totally 0 issues added!

```

- [getlottery.py](getlottery.py)，将抓取的结果存放在文件lottery.json中

### 运行环境要求

- python 3
- 安装了BeautifulSoup

### TODO

- 使用python数学和图形工具（NumPy/pandas/matplotlib/IPython），做一些数据分析和可视化展示
