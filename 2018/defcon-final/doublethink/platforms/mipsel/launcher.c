#include <sys/mman.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define str(x) #x
 
int main()
{
  	int max_size = 0x2000;
  	uintptr_t address = 0x1337000;

  	printf("Opening shellcode file...\n");
  	FILE *shellcode_file = fopen("shellcode", "r");
  	printf("... %p\n", shellcode_file);

	puts("Mapping memory...\n");
  	void *mem = mmap((void *)address, 0x4000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, 0, 0);
	printf("Reading file into %p...\n", mem);
  	int read_bytes = fread(mem, 1, max_size, shellcode_file);
  	printf("Loaded %d bytes of shellcode at %p (tried for %p)...\n", read_bytes, mem, (void *)address);

	printf("Executing!\n");

  	((void(*)())mem)();
}
