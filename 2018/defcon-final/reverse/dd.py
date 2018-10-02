#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.


from pwn import *

def choose(code,lists):
    code=code.decode("hex")
    if code[0]== "\xe8":
        for idx in range(len(lists)):
            if "call" in lists[idx]:
                return idx

    for idx in range(len(lists)):
        i=lists[idx]
        try:
            data=asm(i,arch="amd64")
        except Exception as e:
            data=asm(i,arch="x86")
        finally:
            if data == code:
                return idx
    """
    data64=disasm(code.decode("hex"),arch="amd64")
    data32=disasm(code.decode("hex"))
    idx=data64.find("    ")
    while True:
        if data64[idx] != ' ':
            break
        idx+=1

    data=data[idx:].lower()
    data=data.replace("ptr","")
    data=data.replace(" ","")
    for idx in range(len(lists)):
        line=lists[idx]
        line=line.replace(" ","")
        if data in line:
            return idx
    print "error"
    """
    return None

if __name__ == "__main__":
    stri="""[0] 0x1ffea5: 4d8b26             mov     r12, qword [r14],
    [7] xor     ecx, ecx,
    [8] test    eax, eax,
    [9] mov     rdi, qword [r12+0x48],
    [10] mov     rdi, rbx,
    [11] jne     0x345c36"""
    lists=stri.split("\n")
    print choose("4c89ee",lists)
