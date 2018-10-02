## CTF训练WriteUp

### ret 
修改返回地址

### ret2sec
修改返回地址为shellcode的地址

### orw
使用汇编输出flag**或者**  
使用retf指令，将cs寄存器设为3，可将指令集转为64位模式，32位的系统调用无效
>retf 指令从栈顶取出两个值，第一个传给pc寄存器，第二个传给cs寄存器  
>cs寄存器为2表示32位模式 为1表示64位模式

### two
通过输出的地址得到libc的基地址便宜
输入的16个字节控制两次跳转，第一次跳转将rax置为0，第二次跳转到one_gadget上去

### readme
需要注意flag 在0x400d21和0x600d20的地址上都存在  
爆栈，将argv[0]地址改写为flag地址，这时程序在检测到error时会将flag打印出。同时，栈溢出时将环境变量的指针改为0x600d20，在0x60020处写入`LIBC_FATAL_STDERR_=1`，可以将error信息重定向到标准输出

### readme_renvenge
覆盖bss的libc的函数指针，伪造`printf_arginfo_table`，将%s的函数指针指向`fortify_fail`,并修改bss段`printf_arginfo_table`的指针，将`printf_function_table`置1，再将libc_argv置为指向flag的指针。

### m0rph
程序每次都随机检查一位，判断和真正的flag是否一样  

### hacknote
申请unsort bin 泄漏出main_arana地址，根据便宜计算出libc地址，将输出函数的指针改为system函数地址，调用shell。

### eztosay
shellcode每个字节不能重复，总长度不超过24  
多用push操作  

### ezprintf
泄露libc地址，将malloc_hook值改为one_gadget值  

### bpc
修改返回地址，重新执行write函数，泄漏got表，得到libc基地址，第二次read时跳转到system，执行/bin/sh  

### babyheap  
通过修改堆结构的大小泄漏`main_arena`地址，得到libc地址，然后通过fastbin将`malloc_hook`地址修改为`one_gadget`地址

### skmgr
名字做检查时会泄露libc地址，通过double free将aoti的got表改为system地址。  

### eztosay2
调用read指令时会将rcx置为pc值，通过两次read执行shellcode














