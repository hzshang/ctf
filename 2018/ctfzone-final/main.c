/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
int main(){
    char *buf=malloc(0x10000);
    char *dst=malloc(0x10000);
    memcpy(buf,dst,0x10000);
    printf("hello,world\n");
    return 0;
}
