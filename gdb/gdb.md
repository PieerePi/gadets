## gdb

### 使用python扩展gdb

#### 用法

```
$ gdb binary core
(gdb) source ~/bin/topfuncs.py
(gdb) topfuncs
{'InitSipEndPt': 1, 'nanosleep': 14, 'accept': 1, '__lll_lock_wait': 1, 'poll': 42, 'epoll_wait': 2, 'select': 1}
(gdb)
```

- topfuncs.py，分析`thread apply all bt`的输出（没有full参数，加了会比较慢），统计各线程调用堆栈的最后一个函数
- 可将`source ~/bin/topfuncs.py`放到~/.gdbinit文件中，让gdb启动时自动加载
- [Extending GDB using Python](https://sourceware.org/gdb/current/onlinedocs/gdb/Python.html)，官方最新版本的gdb的python扩展说明文档，比较新，CentOS 6.5环境与其有一些出入

#### 运行环境

- CentOS 6.5
  - Python 2.6.6 (r266:84292, Jan 22 2014, 09:42:36)
  - [GCC 4.4.7 20120313 (Red Hat 4.4.7-4)] on linux2

### 非扩展的另一个版本

#### 用法

```
$ python ~/bin/topfuncs-1.py
Usage: python topfuncs-1.py gdb_thread_apply_all_bt_output
$ gdb binary core
(gdb) set logging on
Copying output to gdb.txt.
(gdb) thread apply all bt
(gdb) set logging off
Done logging to gdb.txt.
(gdb) shell
$ python ~/bin/topfuncs-1.py gdb.txt
{'InitSipEndPt': 1, 'nanosleep': 14, 'accept': 1, '__lll_lock_wait': 1, 'poll': 42, 'epoll_wait': 2, 'select': 1}
$ exit
exit
(gdb)
```
