#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import gdb

class TopFuncs(gdb.Command):
    def __init__(self):
        super(self.__class__, self).__init__("topfuncs", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)

    def invoke(self, args, from_tty):
        lines = gdb.execute("thread apply all bt", to_string=True).splitlines()
        printTopFuncs(lines)

def printTopFuncs(lines):
    topfuncs = {}
    gotathreadblock = False
    for line in lines:
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

TopFuncs()
