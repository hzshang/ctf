#include <sys/mman.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define str(x) #x
 
int main()
{
  	int max_size = 0x2000;
  	uintptr_t address = 0x10000;

  	printf("Opening shellcode file...\n");
  	FILE *shellcode_file = fopen("shellcode", "r");
  	printf("... %p\n", shellcode_file);

	#warning Not mapping memory.
	void *mem = (void *)address;
	printf("Reading file into %p...\n", mem);
  	int read_bytes = fread(mem, 1, max_size, shellcode_file);
  	printf("Loaded %d bytes of shellcode at %p (tried for %p)...\n", read_bytes, mem, (void *)address);

	printf("Executing!\n");

  	((void(*)())mem)();
}
