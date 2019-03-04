全程划水。。。。  =，=、
## babystack  
因为alarm的低字节和execve相近，本来是想用自己的方法改alarm got表的低字节，写完本地可以，但远程限制了只能读取一次。。。  
最后学到了一招 ret to dl resolve。  
目测对64位的机器不好实现，因为bss段和data段的距离相隔有点远，在下面的检查里很容易使vernum[ELFW(R_SYM) (reloc->r_info)] 变为一个非法地址。

	／*used don't look in the global scope.  */
	if (__builtin_expect (ELFW(ST_VISIBILITY) (sym->st_other), 0) == 0)
	{
	  const struct r_found_version *version = NULL;
	  if (l->l_info[VERSYMIDX (DT_VERSYM)] != NULL)
	    {
	      const ElfW(Half) *vernum =
	        (const void *) D_PTR (l, l_info[VERSYMIDX (DT_VERSYM)]);
	      ElfW(Half) ndx = vernum[ELFW(R_SYM) (reloc->r_info)] & 0x7fff;
	      version = &l->l_versions[ndx];
	      if (version->hash == 0)
	        version = NULL;
	    }

## blackhole  
允许使用的system call 只有 read open 以及mprotect，也是一次传过去所有的payload。  
比赛前得到了某股神秘力量的暗示，一个很明显的流程就是先mprotect将栈变为可执行，然后利用shellcode侧信道爆出flag内容。（嗯，对这个题的唯一贡献就是提供了这个思路  
／／TODO
## MagaGame
>nxn的方格里，有2xm个宫殿，还有若干个障碍物，其余方格为道路。  
>要求使用道路将这2xm个宫殿两两匹配，道路之间不能重叠。  
>问有多少种不同的方法（10s内给出结果）

递归时间太长，只能dp，搞了一天，不能解决道路之间的环问题。  

## house of card  
利用了一个CVE，使用bpf的bug拿root shell

## heapstorm
使用large bin插链过程来在0x13370000段上写入两个地址，然后用unsort bin分配出来，实现任意地址写。

