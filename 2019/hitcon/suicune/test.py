#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
import subprocess
import string

def enc(data,key):
    proc = subprocess.Popen(["./suicune",data,str(key)],stdout = subprocess.PIPE)
    out,err = proc.communicate()
    return out[:-1]

def dec(data,key):
    proc = subprocess.Popen(["./a.out",data,str(key)],stdout = subprocess.PIPE)
    out, err = proc.communicate()
    return out[:-1]

def genestr(n):
    pool = string.printable
    for a in pool:
        for b in pool:
            yield a+b


for raw in genestr(5):
    ct = enc(raw,1234)
    pt = dec(ct,1234)
    assert pt == raw






