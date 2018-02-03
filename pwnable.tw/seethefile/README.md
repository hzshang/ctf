## seethefile

该程序可以读取任意文件并打印到屏幕上，通过读取文件/proc/self/maps可以得到程序的运行地址。  

检查程序发现没有开启栈保护，本来想着可以通过main函数里面的nptr覆盖返回值，发现main函数根本就不会返回，可能是故意忽悠人呢吧。。。    

最后在函数退出时，程序会让输入名字，很明显的套路，果然name的内存地址和文件指针紧挨着，利用scanf可以直接修改fp的指针。
FILE的结构体里，有一处是一个函数表的指针，对FILE的基本操作，都会从这个函数表里读取函数指针，然后调用。  
FILE结构体：

	241 struct _IO_FILE {
	242   int _flags;                /* High-order word is _IO_MAGIC; rest is flags. */
	243 #define _IO_file_flags _flags
	244 
	245   /* The following pointers correspond to the C++ streambuf protocol. */
	246   /* Note:  Tk uses the _IO_read_ptr and _IO_read_end fields directly. */
	247   char* _IO_read_ptr;        /* Current read pointer */
	248   char* _IO_read_end;        /* End of get area. */
	249   char* _IO_read_base;        /* Start of putback+get area. */
	250   char* _IO_write_base;        /* Start of put area. */
	251   char* _IO_write_ptr;        /* Current put pointer. */
	252   char* _IO_write_end;        /* End of put area. */
	253   char* _IO_buf_base;        /* Start of reserve area. */
	254   char* _IO_buf_end;        /* End of reserve area. */
	255   /* The following fields are used to support backing up and undo. */
	256   char *_IO_save_base; /* Pointer to start of non-current get area. */
	257   char *_IO_backup_base;  /* Pointer to first valid character of backup area */
	258   char *_IO_save_end; /* Pointer to end of non-current get area. */
	259 
	260   struct _IO_marker *_markers;
	261 
	262   struct _IO_FILE *_chain;
	263 
	264   int _fileno;
	265 #if 0
	266   int _blksize;
	267 #else
	268   int _flags2;
	269 #endif
	270   _IO_off_t _old_offset; /* This used to be _offset but it's too small.  */
	271 
	272 #define __HAVE_COLUMN /* temporary */
	273   /* 1+column number of pbase(); 0 is unknown. */
	274   unsigned short _cur_column;
	275   signed char _vtable_offset;
	276   char _shortbuf[1];
	277 
	278   /*  char* _save_gptr;  char* _save_egptr; */
	279 
	280   _IO_lock_t *_lock;
	281 #ifdef _IO_USE_OLD_IO_FILE
	282 };

通过动态调试，发现在fclose函数里，会调用`_IO_file_close_it`。  
如下所示，ebx即fp指针，在0x94偏移处是函数表的指针，这时函数表的0x44偏移处就是我们将要调用的函数入口，并且该函数的参数还是fp指针。  
  
#### 漏洞利用
对name的读取时，构造FILE结构体，将上面的函数指针修改为system地址，此时system的参数为fp。但是system的参数里如果有`;`，会对前面的内容进行截断，利用这一点可以执行shell。  

同时还需要注意，scanf函数遇到`0x09``0x0a``0x0b``0x0c``0x0d``0x20`字符时会结束读取，要保证payload里没有这些字符。

	[----------------------------------registers-----------------------------------]
	EAX: 0x804c410 --> 0xfbad2408
	EBX: 0x804c410 --> 0xfbad2408
	ECX: 0x0
	EDX: 0x0
	ESI: 0x0
	EDI: 0x0
	EBP: 0xffffd518 --> 0xffffd568 --> 0x0
	ESP: 0xffffd4d0 --> 0xf7fd0000 --> 0x1afdb0
	EIP: 0xf7e88d10 (<_IO_file_close_it+256>:	movsx  eax,BYTE PTR [ebx+0x46])
	EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
	[-------------------------------------code-------------------------------------]
	   0xf7e88d0c <_IO_file_close_it+252>:	pop    edi
	   0xf7e88d0d <_IO_file_close_it+253>:	ret
	   0xf7e88d0e <_IO_file_close_it+254>:	xchg   ax,ax
	=> 0xf7e88d10 <_IO_file_close_it+256>:	movsx  eax,BYTE PTR [ebx+0x46]
	   0xf7e88d14 <_IO_file_close_it+260>:	sub    esp,0xc
	   0xf7e88d17 <_IO_file_close_it+263>:	mov    eax,DWORD PTR [ebx+eax*1+0x94]
	   0xf7e88d1e <_IO_file_close_it+270>:	push   ebx
	   0xf7e88d1f <_IO_file_close_it+271>:	call   DWORD PTR [eax+0x44]
	[------------------------------------stack-------------------------------------]
	0000| 0xffffd4d0 --> 0xf7fd0000 --> 0x1afdb0
	0004| 0xffffd4d4 --> 0x804c410 --> 0xfbad2408
	0008| 0xffffd4d8 --> 0xf7e1f700 (0xf7e1f700)
	0012| 0xffffd4dc --> 0xf7e7cf49 (<fclose+137>:	mov    edx,DWORD PTR [esi])
	0016| 0xffffd4e0 --> 0x804c410 --> 0xfbad2408
	0020| 0xffffd4e4 --> 0xf7e28bd8 --> 0x4857 ('WH')
	0024| 0xffffd4e8 --> 0xf7e61bcb (<vfprintf+11>:	add    ebx,0x16e435)
	0028| 0xffffd4ec --> 0x0
	[------------------------------------------------------------------------------]
  
















