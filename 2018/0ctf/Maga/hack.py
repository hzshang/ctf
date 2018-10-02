#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from pwn import *
import re
import StringIO
context.log_level="debug"

maga=process("./maga")
PATH=0
OBSTACLE=1
PALACE=2
VISITED=3


def map_num(c):
    if c is '#':
        return OBSTACLE
    elif c is 'X':
        return PALACE
    elif c is '.':
        return PATH

def get_ans(table):
    io = StringIO.StringIO()
    io.write("%d %d\n"%table.shape)
    np.savetxt(io,table,fmt="%d")
    io.write("\n")
    maga.send(io.getvalue())
    return maga.recvline()

conn=remote("202.120.7.219",12321)

for i in range(1,9):
    conn.recvline_startswith("Level %d"%i)
    conn.recvline()
    data=map(map_num,"|".join(conn.recvlines(i+2)).split("|"))
    table=np.reshape(data,(i+2,i+2))
    conn.send(get_ans(table))

conn.interactive()