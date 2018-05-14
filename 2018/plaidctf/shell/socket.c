/*
 * socket.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
#include <sys/types.h>          /* See NOTES */
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
int main(){
    int fd=socket(AF_INET,SOCK_STREAM,0);
	return 0;
}
