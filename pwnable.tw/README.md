pwnable.tw writeup
==================

## start  
控制跳转，第一次泄露栈地址，第二次跳转到shellcode

## orw
使用汇编输出flag**或者**  
使用retf指令，将cs寄存器设为3，可将指令集转为64位模式，32位的系统调用无效
>retf 指令从栈顶取出两个值，第一个传给pc寄存器，第二个传给cs寄存器  
>cs寄存器为2表示32位模式 为3表示64位模式

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
输入内容必须时可写字符，一般用到的`call` `ret` `jmp` 都无法读入，但此时堆结尾处有4字节的数值表示堆的剩余空间，控制堆大小，使数值里出现 `c3` 字符，对应汇编位ret指令。然后通过 `jle` 相对偏移跳转，执行该指令，跳到栈上执行代码。  
栈上的内容自己可控，直接构造shellcode即可。  

## starbound
程序在输入选项时没有对序号范围做检查，当输入值为负数时，程序并不做检测。并且每个序号对应的执行函数表在bss段，函数表上面就是name的内存位置。  
利用上面的漏洞，修改name，控制好序号大小，就可以跳到想要的位置，对libc地址进行泄露。但是题目并没有给出libc版本，使用LibcSearcher找出libc版本。将`one_gadget`的地址写入序号函数表，执行`one_gadget`拿到shell。  

## Spirited Away
- 泄露栈地址，libc地址。
- 循环100次，利用sprintf将`comment_size`覆盖为一个更大的值。
- 这时读入comment时覆盖name的指针为栈指针。
- 下次malloc时得到的内存就是栈空间。
- 读入name时覆盖survey返回值为`one_gadget`。

## secret garden
申请堆块的大小是自己定义的，利用这一点申请`unsortbin`，可以泄露出`main_arena`地址，根据偏移计算libc地址。  
在除花是不做检查，通过double free可以对任意地址进行写操作，这里修改`malloc_hook`值为`one_gadget`值。  
此时如果直接进行申请堆块，所有的`one_gadget`都无法满足条件，反复尝试以后，如果让double free 触发系统错误，会调用malloc函数，此时即可执行shell。  
`one_gadget`值挑选比较坑，本地能过但远程一直上不去，一度怀疑自己思路有问题。好不容易找到了一份别人的writeup，发现只有`one_gadget`的值和别人不一样。

## alive note
做法和death note类似，这里修改的是atoi的got表，不过申请堆块要1200次左右，连接时间为60秒，意味着和主机的延迟不高于0.5ms！！！🌚反正我过了=，=  


## critical_heap
一个比较明显的洞是在 `play_with_normal`函数里，有这样一句。content是可控的，但是`__printf_chunk`相比于printf多了更多的检查，禁止使用`%N$`的字符串，这样就没有办法做到任意地址写了，但是因为`__printf_chunk`的参数栈和我们输入的buf离得比较近，所以可以实现任意地址读。同时libc和堆地址也很容易通过申请一个堆块来leak出来。  

    if ( opt == 1 )
    {
      printf("Content :");
      _printf_chk(1LL, a1->content);
    }

接下来要做的就是把flag的内容读出来了，在调用localtime的函数里，(这个利用确实够骚，以前都没见过)，会调用`tzset_internal`，部分源代码如下

	/* Examine the TZ environment variable.  */
	tz = getenv ("TZ");
	if (tz && *tz == '\0')
	  /* User specified the empty string; use UTC explicitly.  */
	  tz = "Universal";
	/* A leading colon means "implementation defined syntax".
	   We ignore the colon and always use the same algorithm:
	   try a data file, and if none exists parse the 1003.1 syntax.  */
	if (tz && *tz == ':')
	  ++tz;
	/* Check whether the value changed since the last run.  */
	if (old_tz != NULL && tz != NULL && strcmp (tz, old_tz) == 0)
	  /* No change, simply return.  */
	  return;
	if (tz == NULL)
	  /* No user specification; use the site-wide default.  */
	  tz = TZDEFAULT;
	tz_rules[0].name = NULL;
	tz_rules[1].name = NULL;
	/* Save the value of `tz'.  */
	free (old_tz);
	old_tz = tz ? __strdup (tz) : NULL;
	/* Try to read a data file.  */
	__tzfile_read (tz, 0, NULL);
	if (__use_tzfile)
	  return

利用system_heap把TZ环境变量设为flag的路径，就可以直接把flag读到堆上面。  


## bookwriter
- leak libc
- leak heap address
- change top chunk size to trigger free
- expand unsortbin size to control its content
- fake unsortbin bk to change dl open hook to heap address
- trigger error


## 以下题目不公开writeup

- kidding
- secret-of-my-heart
- de-aslr
- unexpolitable
- critical-heap++  
