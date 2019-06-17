#!/usr/bin/env python
# coding=utf-8

import pickle
from struct import pack

def enc(x):
    global lut
    res = 0
    for i in xrange(8):
        res ^= lut[i][x&0xff]
        x >>= 8
    return res
def g(x):
    global lut
    res = 0
    x=x>>32
    for i in xrange(4,8):
        res ^= lut[i][x&0xff]
        x >>= 8
    return res

def f(x):
    global lut
    res = 0
    for i in xrange(4):
        res ^= lut[i][x&0xff]
        x >>= 8
    return res

lut = pickle.load(file('./lut.pl', 'rb'))
print hex(enc(1))
# for i in xrange(1<<32):
