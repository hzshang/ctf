/*
 * test.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
int main(){
    for(int i=0;i<10000;i++){
        void *ptr=malloc(0xFFFFFFFF);
        printf("malloc address :%p\n",ptr);
    }	
	return 0;
}
