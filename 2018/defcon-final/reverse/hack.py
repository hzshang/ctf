#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="error"

pwn_file="./reverse"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    r=process([pwn_file,"10.13.37.2","--numpad"])
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def dex(data):
    return disasm(data.decode("hex"))

r.sendlineafter("(press 1 to insert coin)","1")
r.sendlineafter("Round 1","1")

while True:
    line = r.recvline()
    if "-------------------------------------------------"  in line:
        r.recvline()
        break
pool=[]

while True:
    line=r.recvline()
    pool.append(line)
    if "-----------------------------------------"  in line:
        break

for i in pool:
    if "?????" in i:
        line=i
        break

start=i.find(": ")+2
end=i.find("\x1b")
code=i[start:end].decode("hex")
ret=disasm(code,arch="amd64")
print ret.encode("hex")
print ret
ret.find("")

while True:
    line=r.recvline()
    if "(" in line:
        break

ans=[line]
while True:
    data=r.recvline()
print ans

