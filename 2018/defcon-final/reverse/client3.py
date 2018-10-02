#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context.log_level="debug"
def choose(code,lists):
    code=code.decode("hex")
    tmp=[]
    for idx in range(len(lists)):
        if "call" in lists[idx]:
            call_idx=idx
        else:
            tmp.append(lists[idx])

    lists=tmp
    if code[0]== "\xe8":
        return call_idx

    for idx in range(len(lists)):
        i=lists[idx]
        i=i.replace("word","word ptr")
        i=i.replace("byte","byte ptr")

        data=""
        log.debug("asm code:%s"%i)
        log.debug(disasm(code))
        log.debug(disasm(code,arch="amd64"))

        try:
            data=asm(i.replace("rel ","rip+"),arch="amd64")
        except Exception as e:
            data=asm(i.replace("rel ","eip+"),arch="x86")
        finally:
            log.debug(data.encode("hex"))
            log.debug(code.encode("hex"))
            if data in code or code in data:
                return idx


#context(log_level="DEBUG")
key = open("./reverse", "rb").read()
key = key[0xff100:]

def crypt(rand_byte, data):
    k = key[ord(rand_byte)*32:]
    
    retv = ""
    for i, c in enumerate(data):
        retv += chr(ord(k[i&0x1f]) ^ ord(c))
    return retv

def decrypt(payload):
    rand_byte = payload[0]
    opcode = payload[1]
    length = ord(payload[2]) + ord(payload[3])*256
    k = key[ord(rand_byte)*32:]
    
    data = payload[4:][:length]
    retv = ""
    for i, c in enumerate(data):
        retv += chr(ord(k[i&0x1f]) ^ ord(c))
    return opcode, retv

p = remote("10.13.37.2", 7777)
def send(opcode, payload):
    p.send("\x00")
    p.send(opcode)
    p.send(p16(len(payload)))
    p.send(crypt("\x00", payload))

def recv():
    rand_byte = p.recv(1)
    opcode = p.recv(1)
    print "[opecode]0x%x" % ord(opcode)
    length = u16(p.recv(2))
    data = p.recv(length)
    return opcode, crypt(rand_byte, data)
    
send("\x02", "")
print recv()
cy = 0
stage = 0
while True:
    print "AAA", cy
    cy += 1
    a, b=  recv()
    if a == "\x0b":
        print b.encode("hex")
        b = b[5:]
        print b.encode("hex")
        c = b.split("\x00")
        flag = False
        res = filter(lambda x:x, c)
        plain_text_list = res[:-5]
        plain_text_list = filter(lambda x:x.startswith("0x"), plain_text_list)


        rres = res[-5:]

        print plain_text_list
        for i in plain_text_list:
            if "????" in i:
                start=i.find(": ")+2
                end=i.find("  ")
                code=i[start:end]
                break
        print rres
        print code

        r = choose(code, rres)
        print "!!!", r

        send("\x0c", chr(r)) 
    if a == "\x08":
        send("\x09", "")

p.interactive()


