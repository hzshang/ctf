#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
from subprocess import call
context.log_level="debug"
crc= 0x74d7f2d0
crc=0xcc0b89f6
cmd = "arm-linux-gnueabihf-gcc -c low.S -o asm.o"
if call(cmd.split(' ')) !=0:
    print "gcc fail"
    exit(0)

cmd = "arm-linux-gnueabihf-objcopy -j .shellcode -Obinary asm.o bin"
if call(cmd.split(' '))!=0:
    print "objcopy fail"
    exit(0)

import base64
with open("bin","r") as f:
    code = f.read()
print base64.b64encode(code)


