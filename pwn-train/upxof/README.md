### upxof
tctf 2017

题目使用了upx加壳，并且需要输入密码脱壳，动态调试可知密码就是12345678，使用upx脱壳后的代码页非常简单，使用gets进行栈溢出，但是需要绕过canary检查。

	int main()
	{
	  char v4; // [rsp+0h] [rbp-410h]
	  unsigned __int64 v5; // [rsp+408h] [rbp-8h]
	  v5 = __readfsqword(0x28u);
	  setvbuf(stdin, 0LL, 2, 0LL);
	  setvbuf(stdout, 0LL, 2, 0LL);
	  setvbuf(stderr, 0LL, 2, 0LL);
	  printf("let's go:", 0LL);
	  gets(&v4);
	  return 0;
	}
	
#### 绕过canary检查  
upx在读取密码是存在栈溢出，可以直接覆盖程序加载前的main 参数、环境变量、以及axuv  
栈结构
    
    --------------
	|     argc    |
	|   argv[0]   |
	|   argv[1]   |
	|   argv[2]   |
	|   argv[n]   |
	|      0      |    eg.
	|   env1 ptr  |-> "SHELL=/bin/bash"
	|   env2 ptr  |-> "COLUMNS=89"
	|   env3 ptr  |...
	|      0      |
	| axuv1 type  |
	| axuv1 value |
	| axuv2 type  |
	| axuv2 value |
	| axuv3 type  |
	| axuv3 value |
	|    ......   |
	|       0     |
    --------------


axuv有一个type为25(AT_RANDOM)的项，指向一个16个byte的随机数，这串随机数用来辅助生成canary，并将其写入tls。  

	static inline uintptr_t __attribute__ ((always_inline))
	_dl_setup_stack_chk_guard (void *dl_random)
	{
	  union
	  {
	    uintptr_t num;
	    unsigned char bytes[sizeof (uintptr_t)];
	  } ret = { 0 };
	
	  if (dl_random == NULL)
	    {
	      ret.bytes[sizeof (ret) - 1] = 255;
	      ret.bytes[sizeof (ret) - 2] = '\n';
	    }
	  else
	    {
	      memcpy (ret.bytes, dl_random, sizeof (ret));
	#if BYTE_ORDER == LITTLE_ENDIAN
	
	      ret.num &= ~(uintptr_t) 0xff;
	#elif BYTE_ORDER == BIG_ENDIAN
	
	      ret.num &= ~((uintptr_t) 0xff << (8 * (sizeof (ret) - 1)));
	#else
	
	#error "BYTE_ORDER unknown"
	
	#endif
	
	    }
	  return ret.num;
	}
	
在输入密码时伪造axuv，就可以把随机数指向一处16个byte的0，canary就会变为0，绕过栈检查








