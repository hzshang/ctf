from pwn import *
context.log_level="debug"

re=remote("keygenme.ctfcompetition.com",1337)
pro=process("./emu")



while True:
	data=re.recvline()[:-1]
	pro.sendlineafter("input:",data)
	pro.recvuntil("data:")
	sha=pro.recvline()[:-1]
	re.sendline(sha)
	re.recvuntil("OK\n")
