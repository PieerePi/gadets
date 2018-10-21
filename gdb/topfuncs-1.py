#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import sys

def main():
    topfuncs = {}
    gotathreadblock = False
    if len(sys.argv) != 2 or sys.argv[1] == '-h':
        print("Usage: python topfuncs-1.py gdb_thread_apply_all_bt_output")
        return
    if sys.version_info[0] > 2:
        file = open(sys.argv[1], encoding="utf-8", errors="ignore")
    else:
        file = open(sys.argv[1])
    for line in file.readlines():
        if gotathreadblock == False:
            if line.find("Thread") == 0:
                gotathreadblock = True
        else:
            if line.find("#0") == 0:
                words = line.split()
                if len(words) >= 4:
                    if words[3] in topfuncs:
                        topfuncs[words[3]] += 1
                    else:
                        topfuncs[words[3]] = 1
            elif line.find("#") != 0:
                gotathreadblock = False
    print(topfuncs)

if __name__ == "__main__":
    main()
