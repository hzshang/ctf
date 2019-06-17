#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
elf =ELF("./lut")
#for bit_cnt in range(7,0,-1):
bit_cnt = 7
bit_8_data = []
mark = asm("and rax,[rbp-0x818]",arch="amd64")
test_rax= asm("test rax,rax",arch="amd64")
mov_rdx_rax = asm("mov rdx,rax",arch="amd64")
mark1 = asm("and rax,[rbp-0x818]",arch="amd64")
mark2 = asm("mov rax,[rbp-0x818]",arch="amd64")

gadgets = elf.search(mark1)
def locate_bit(m):
    cnt = 0
    while m:
        m = m>>8
        cnt+=1
    return cnt-1

#7~4
for it in gadgets:
    assert elf.read(it-0xa,2) == "\x48\xb8"
    mask = u64(elf.read(it-8,8))
    bit_num = locate_bit(mask)
    tmp = elf.read(it+0x7,3)
    if tmp == test_rax:
        num = 0
        xor_data = u64(elf.read(it + 21,8))
    else:
        assert tmp == mov_rdx_rax
        num = u64(elf.read(it+22,8))
        assert num &((1<<(bit_num*8))-1) == 0
        xor_data = u64(elf.read(it + 34,8))
    #print hex(it),hex(num),hex(xor_data)
    bit_8_data.append([num>>56,xor_data])

for i in range(0x100):
    print i,":"
    for p in bit_8_data:
        if p[0] == i:
            print hex(p[1])


#print map(hex,(list(elf.search(asm("movzx eax,al",arch="amd64")))))[:10]
#print len(list(elf.search(asm("mov rax,0xff00000000000000",arch="amd64"))))
#print len(list(elf.search(asm("mov rax,0xff0000000000",arch="amd64"))))
#print len(list(elf.search(asm("mov rax,0xff00000000",arch="amd64"))))

