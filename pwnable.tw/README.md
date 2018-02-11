pwnable.tw writeup
==================

## start  
控制跳转，第一次泄露栈地址，第二次跳转到shellcode

## orw
使用汇编输出flag**或者**  
使用retf指令，将cs寄存器设为3，可将指令集转为64位模式，32位的系统调用无效
>retf 指令从栈顶取出两个值，第一个传给pc寄存器，第二个传给cs寄存器  
>cs寄存器为2表示32位模式 为1表示64位模式

## double sort  
- 泄露堆地址
- scanf 遇到"+"字符时，不会修改指针指向的内存值，利用这一点绕过栈检查

## calc
- 搞清楚计算表达式的逻辑
- 构造rop链
- 想办法绕过栈检查

## hacknote
申请unsort bin 泄漏出main_arana地址，根据便宜计算出libc地址，将输出函数的指针改为system函数地址，调用shell。

## silver bullet
- power_up函数有bug，当填充48个字节后，会将power的值覆盖为0，此漏洞可以造成overflow
- 控制返回值，先泄露libc地址
- 再跳转到main函数，跳转到libc的one_gadget

## apple store
checkout时会有一个彩蛋，当总额达到7174时会将iphone8的订单加入购物车，订单是一个结构体， 

	struct unit{
		char* name;
		int price;
		unit* next;
		unit* back;
	};

但是最后彩蛋订单的内存实在栈上的！！利用这个bug，通过myread函数可以修改最后一个订单的信息，进而可以泄露出栈地址和libc地址。  
本来是想将atoi的got表修改为system地址，但system的地址处不可写。  
最后参考网上的方法，修改main函数的ebp值，通过换栈的方式将main函数的返回地址改为system地址。

## seethefile
[writeup](seethefile/README.md)  

## babystack
通过爆破的方法解出16位随机数，通过`magic_copy`,可以将libc的地址复制到栈上，继续爆破出libc的地址。最后将main函数返回地址改为`one_gadget`地址，拿到shell。（远程连接比较耗时，最好用台日本主机。。。

## death note
程序的漏洞很明显，题目也给出了提示，要求写入shellcode  
在add_note时,由于index的最小值没有限制，因此将index写为负值，就可以修改atoi的got表，进一步跳到堆上执行我们输入的内容。  
输入内容必须时可写字符，一般用到的`call` `ret` `jmp` 都无法读入，但此时堆结尾处有4字节的数值表示堆的剩余空间，控制堆大小，是数值里出现 `c3` 字符，对应汇编位ret指令。然后通过 `jle` 相对偏移跳转，执行该指令，跳到栈上执行代码。  
栈上的内容自己可控，直接构造shellcode即可。  

## starbound
程序在输入选项时没有对序号范围做检查，当输入值为负数时，程序并不做检测。并且每个序号对应的执行函数表在bss段，函数表上面就是name的内存位置。  
利用上面的漏洞，修改name，控制好序号大小，就可以跳到想要的位置，对libc地址进行泄露。但是题目并没有给出libc版本，使用LibcSearcher找出libc版本。将one_gadget的地址写入序号函数表，执行one_gadget拿到shell。  



