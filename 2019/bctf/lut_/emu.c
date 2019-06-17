//gcc emu.c -g -fPIE -no-pie
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <stdint.h>
#define uint_8 unsigned 
#define ELF_ADD 0x100000
void loadfile(char* name){
    FILE* fd = fopen(name,"r");
    fseek(fd,0,SEEK_END);
    uint64_t size = ftell(fd);
    fseek(fd,0,SEEK_SET);
    mmap((void*)ELF_ADD,(size+0xfff)&0xfffff000,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS,-1,0);
    uint64_t pc=0;
    while(1){
        uint64_t t = fread((void*)(ELF_ADD+pc),0x1,0x100,fd);
        if (t<=0)
            break;
        pc+=t;
    }
}
void *memset_ptr;
uint64_t (*enc)(uint64_t);
void func_init(){
    memset_ptr = (void*)memset;
    *(uint64_t*)(ELF_ADD + 0x640 + 2) = ((uint64_t)(&memset_ptr) - (ELF_ADD + 0x640 +6))&0xffffffff;

    enc = (void*)(ELF_ADD + 0x786);
}


uint64_t linear(uint64_t x){
    return enc(x)^enc(0);
}

int main(){
    loadfile("./lut");
    func_init();
    printf("%016lx\n",enc(0x3030303030303031));
}
