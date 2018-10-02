### preview

程序被加了壳，但是壳load程序时用axuv的随机数当作地址进行mmap，这样就可以通过leak出ld和elf文件的基地址来推出canary，接下来就是一个栈溢出。