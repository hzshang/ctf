#include <stdio.h>
#include <stdlib.h>

int main(){
	char *buf=malloc(0x100);
	read(0,buf,0x100);
	asm("call *%0"::"m"(buf));
}