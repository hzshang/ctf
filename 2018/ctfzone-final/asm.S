.section .shellcode,"awx"
.global _start
.global __start
_start:
__start:
.syntax unified
.arch armv7-a
.arm
start:
    mov r3,0x8000
    add r3,0xf00
    adr r1,write_m
    adr r0,func_end
loop:
    ldm r1!,{r4-r13}
    stm r3!,{r4-r13}
    cmp r1,r0
    blo loop

    mov r1,0x1f000
    add r1,0x000
    mov r2,0x10000
    add r2,0xf700
    add r2,0xff
    adr r0,crc
    ldm r0!,{r4-r14}
    mov r0,r4
    mov r3,0x8000
    add r3,0xf00
    mov pc,r3

write_m:
    mov r3,r4
loop_m:
    stm r1!,{r3-r14,r0}
    and r1,r2
    b loop_m
func_end:
crc:
//    .ascii "\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6\xcc\x0b\x89\xf6"
    .ascii "\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0"
end:
    nop
