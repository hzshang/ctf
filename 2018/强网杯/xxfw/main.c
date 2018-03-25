/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
void *fun_ptr;
void *rdi;
void *rsi;
void *rdx;

int main() {

    int length=0x10000;

    fun_ptr = malloc(length);
    int code_fd=open("mycode",O_RDONLY);
    while(read(code_fd,fun_ptr,length) > 0);

    int flag_fd=open("flag_re1.mod",O_RDONLY);
    rdi=malloc(length);
    while(read(flag_fd,rdi,length) > 0);
    
    int box_fd=open("rp_box.mod",O_RDONLY);
    rdx=malloc(length);
    while(read(box_fd,rdx,length) > 0);
    
    rsi=malloc(length);
    
    asm(
        "xor %%rax,%%rax\n\t"
        "xor %%rbx,%%rbx\n\t"
        "xor %%rcx,%%rcx\n\t"
        "xor %%rdx,%%rdx\n\t"
        "xor %%rsi,%%rsi\n\t"
        "xor %%rdi,%%rdi\n\t"
        "xor %%r8,%%r8\n\t"
        "xor %%r9,%%r9\n\t"
        "xor %%r10,%%r10\n\t"
        "xor %%r11,%%r11\n\t"
        "xor %%r12,%%r12\n\t"
        "xor %%r13,%%r13\n\t"
        "xor %%r14,%%r14\n\t"
        "xor %%r15,%%r15\n\t"
        "mov %1,%%rdi\n\t"
        "mov %2,%%rsi\n\t"
        "mov %3,%%rdx\n\t"
        "call *%0\n\t"
        "nop\n\t"
        "nop\n\t"
        "hlt\n\t"
        ::"m"(fun_ptr),"m"(rdi),"m"(rsi),"m"(rdx));
        
    return 0;
}
