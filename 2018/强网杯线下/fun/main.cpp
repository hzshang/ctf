/*
 * main.cpp
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <cstdio>
#include <iostream>
int main(){
	int* a=new int[0x10];
    int* b=new int[0x10];
    int* c=new int[0x10];
    delete a;
    delete b;
    delete a;
	return 0;
}
