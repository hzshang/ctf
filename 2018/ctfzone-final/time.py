#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
import tempfile
from subprocess import call
import random
with open("./module.S","r") as f:
    data=f.read()

#pc = random.randint(0x5000,0x1d000)
pc = 0x1ff00
source = tempfile.mktemp()+".S"

data = data%(pc&0xff000,pc&0xf00,pc&0xff000,pc&0xf00)

with open(source,"w+") as f:
    f.write(data)

call(["./make.py",source])
