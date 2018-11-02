#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import gdb

class TopFuncs(gdb.Command):
    def __init__(self):
        super(self.__class__, self).__init__("topfuncs", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)

    def invoke(self, args, from_tty):
        lines = gdb.execute("thread apply all bt", to_string=True).splitlines()
        printTopFuncs(lines, args)

def printTopFuncs(lines, args):
    topfuncs = {}
    gotathreadblock = False
    searchfunc = ""
    funcids = []
    threadid = ""
    argv = gdb.string_to_argv(args)
    if len(argv) != 0:
        searchfunc = argv[0]
    for line in lines:
        if gotathreadblock == False:
            if line.find("Thread") == 0:
                gotathreadblock = True
                words = line.split()
                threadid = words[1]
        else:
            if line.find("#0") == 0:
                words = line.split()
                if len(words) >= 4:
                    if words[3] in topfuncs:
                        topfuncs[words[3]] += 1
                        if words[3] == searchfunc:
                            funcids.append(threadid)
                    else:
                        topfuncs[words[3]] = 1
                        if words[3] == searchfunc:
                            funcids.append(threadid)
            elif line.find("#") != 0:
                gotathreadblock = False
    if len(argv) == 0:
        print(topfuncs)
    else:
        print(funcids)

TopFuncs()
