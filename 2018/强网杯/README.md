## Pig
一个很明显的double free 大小为0x70的fastbin，修改malloc hook的地址为gadget地址，通过double free触发malloc

## Silent
通过double free ，利用bss上的stderr的0x7f字节伪造一个chunk，申请出chunk后覆盖指针数组，将free的got表改为system的地址，通过free调用system。  

## Silent2
由于这次对size的大小有所限制，利用unsortbin，伪造chunk，通过unlink修改指针数组，将free的got表内容改为system地址。
