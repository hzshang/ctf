#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
import sys
MAX_LONG = (1<<64)-1
class Rand:
    def __init__(self,append,value):
        self.append = append
        self.value = (value * 0x5851F42D4C957F2D + 0x5851F42D4C957F2E) & MAX_LONG
        self.wtf = 0x9e
    def get_rand(self):
        r = self.value
        self.value = (self.value * 0x5851F42D4C957F2D + self.append) & MAX_LONG
        tmp = ((r ^ (r >> 18))>>27)&((1<<32)-1)
        offset = r >> 59
        return (tmp>>offset)|((tmp&((1<<offset)-1))<<(32-offset))

def encrypt(flag,key):
    rand = Rand(1,key)
    def shift(t):
        for i in range(len(t)-1,0,-1):
            v = rand.get_rand()%(i+1)
            t[v],t[i] = t[i],t[v]
        return t
    def get_table(length):
        table = [x for x in range(0x100)]
        table = shift(table)
        rand.get_rand()
        rand.get_rand()
        tmp = table[:length]
        tmp.sort()
        return tmp[::-1]
    s1 = flag
    for i in range(0x10):
        s2 = get_table(len(s1))
        data = "".join([chr(ord(x)^y) for x,y in zip(s1,s2)])
        s1 = data[::-1]
    return s1

def decrypt(enc,key):
    rand = Rand(1,key)
    def shift(t):
        for i in range(len(t)-1,0,-1):
            v = rand.get_rand()%(i+1)
            t[v],t[i] = t[i],t[v]
        return t
    def get_table(length):
        table = [x for x in range(0x100)]
        table = shift(table)
        rand.get_rand()
        rand.get_rand()
        tmp = table[:length]
        tmp.sort()
        return tmp[::-1]
    pool = []
    for i in range(0x10):
        pool.append(get_table(len(enc)))
    s1 = enc
    for i in range(0x10):
        s2 = pool[-i]
        data = "".join(chr(ord(x)^y) for x,y in zip(s1,s2))
        s1 = data[::-1]
    return s1

enc = "04dd5a70faea88b76e4733d0fa346b086e2c0efd7d2815e3b6ca118ab945719970642b2929b18a71b28d87855796e344d8".decode("hex")
enc = 
#enc =  encrypt("hitcon{1123213}",1234)
enc = encrypt("b"+"c"*47+"a",1234)
print enc.encode("hex")
