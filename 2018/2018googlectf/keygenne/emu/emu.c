/*
 * emu.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#define uint_8 unsigned char
#define ELF_ADD (0x100000)

void (*todo3)(char *dst,char *src,size_t len);
void (*md5)(char *dst,char *src,size_t len);
void (*todo2)(char *a1,char *src);


void (*crypto)(char *src,char *dst);
void (*hex2str)(uint_8 *src,uint_8 *dst);
uint_8 (*charchar2hex)(uint_8 *src);


void* (*memcpy_ptr)(void *dst, const void *src, size_t n);
void* (*memset_ptr)(void *s, int c, size_t n);

void loadfile(){
    int fd=open("./elf",O_RDWR);
    off_t size=lseek(fd,0,SEEK_END);
    mmap((void*)ELF_ADD,size,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE,fd,0);
    close(fd);
}

void init_fun(){
	todo3=(void (*)(char *dst,char *src,size_t len))(0x1747 + ELF_ADD);
	md5=(void (*)(char *dst,char *src,size_t len))(0xc46 + ELF_ADD);
	todo2=(void (*)(char *dst,char *src))(0x18A9 + ELF_ADD);
	crypto=(void (*)(char *src,char *dst))(0xa0e + ELF_ADD);
	hex2str=(void (*)(char *src,char *dst))(0x8e7 + ELF_ADD);
	charchar2hex=(uint_8(*)(uint_8 *src))(0x9CD + ELF_ADD);
	memcpy_ptr=memcpy;
	memset_ptr=memset;
	// change memcpy got in elf
	int *p=(int *)(0x7a2+ELF_ADD);
	*p=(int)((void*)&memcpy_ptr-(0x7a6+ELF_ADD));
	// change memset got in elf
	p=(int*)(0x722+ELF_ADD);
	*p=(int)((void*)&memset_ptr-(0x726+ELF_ADD));
}
void str2hex(uint_8 *dst,uint_8 *src){
	for(int i=0;i<0x10;i++){
		dst[i]=charchar2hex(&src[2*i]);
	}
}
void reverse(uint_8 *dst,uint_8 *src){
	uint_8 buf[0x10];
	uint_8 hex[0x10];
	str2hex(hex,src);
	memset(buf,0,0x10);
	for(int i=0;i<0x10;i++){
		uint_8 tmp=i^(i<<4)^hex[i];
		buf[i]|=tmp&0xf;
		buf[15-i]|=tmp&0xf0;
	}
	hex2str(buf,dst);
}

int main(){
    loadfile();
    init_fun();

    unsigned int buf[0x100];
    char *dst=malloc(0x1000);
    char hexcode[0x33];
    char result[0x33];
    char arg1[0x10];
    memset(result,0,0x33);
    memset(hexcode,0,0x33);
    memset(buf,0,0x100);

    buf[0]=0;
    buf[1]=0;
    buf[2]=0x67452301;
    buf[3]=0xEFCDAB89;
    buf[4]=0x98BADCFE;
    buf[5]=0x10325476;
    printf("input:");
    scanf("%s",arg1);
    int len=strlen(arg1);
    todo3((char*)buf,arg1,len);
    todo2(dst,(char*)buf);
    hex2str(dst,hexcode);
    reverse(result,hexcode);
    printf("%s\n",result);
	return 0;
}
