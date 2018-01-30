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
- scanf 遇到"+"字符时，不会修改指针的值，利用这一点绕过栈检查

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


