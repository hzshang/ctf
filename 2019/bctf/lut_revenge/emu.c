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

uint64_t (*enc)(uint8_t*);
void func_init(){
    enc = (void*)(ELF_ADD + 0x820);
}

void show_buf(uint8_t *buf){
    for(int i=0;i<10;i++){
        printf("%02x",buf[i]);
    }
    puts("");
}

void xor_buf(uint8_t *dst,uint8_t* p,uint8_t* q){
    for(int i=0;i<10;i++){
        dst[i] = p[i]^q[i];
    }
}

int main(){
    loadfile("./lut_revenge");
    func_init();
    uint8_t a1[10]={0};
    uint8_t a2[10]={0};
    uint8_t a3[10]={0};
    uint8_t b1[10]={0};
    uint8_t b2[10]={0};
    uint8_t b3[10]={0};
    for(int i = 0;i < 10*8;i++){
        memset(a1,0,10);
        a1[i/8] = 1<<(i%8);
        enc(a1);
        show_buf(a1);
    }

}
