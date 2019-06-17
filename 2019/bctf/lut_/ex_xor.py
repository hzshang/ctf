#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
from parse import *
data = ELF("./lut").read(0x4991E9,0x49B2B9-0x4991E9)
for i in range(0,len(data),24):
    print data[i:i+24].encode("hex")
    ret = parse("\x48\x8B\x95{}\x48\x8B\x85{}\x48\x31\xD0\x48\x89\x85{}",data[i:i+24])
    print hex(u32(ret[0]))
    print hex(u32(ret[1]))
    print hex(u32(ret[2]))
