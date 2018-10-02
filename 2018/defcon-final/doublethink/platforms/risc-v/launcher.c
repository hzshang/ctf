#include <machine/syscall.h>
#include <riscv-pk/mmap.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define str(x) #x
 
int main()
{
  	int max_size = 0x2000;
  	uintptr_t address = 0x1337000;

  	//printf("Opening shellcode file...\n");
  	FILE *shellcode_file = fopen("shellcode", "r");
  	//printf("... %p\n", shellcode_file);

	//puts("Mapping file...\n");
	//#warning Memory-mapping shellcode.
  	//void *mem = __internal_syscall(SYS_mmap, (void *)address, 0x4000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE, fileno(shellcode_file), 0);
  	//printf("Mapped shellcode at %p (tried for %p)...\n", mem, (void *)address);

	//puts("Mapping memory...\n");
  	void *mem = __internal_syscall(SYS_mmap, (void *)address, 0x4000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_FIXED|MAP_PRIVATE|MAP_ANONYMOUS, 0, 0);
	//printf("Reading file into %p...\n", mem);
  	int read_bytes = fread(mem, 1, max_size, shellcode_file);
  	printf("Executing %d bytes of shellcode at %p!\n", read_bytes, mem);

  	((void(*)())mem)();
}
