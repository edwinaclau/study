工具链

gcc实际上不是一个编译器，是个驱动程序(driver program)
gcc 编译过程中的每一个环节由具体的组件负责

编译过程由cc1负责,汇编过程由as负责,链接过程ld负责

gcc就是用collect2安排初始化过程中

预编译、编译、汇编、链接


  
预编译

       #include #define
       #if #else #endif

gcc -E hello.c hello.i

gcc -E 仅做预处理


(1) 文件包含


(2) 宏定义


(3) 条件编译


编译就是对 词法分析 语法分析 语义分析 生成中间代码
并对 中间代码进行优化 

例如gcc -S target.c

生成汇编文件，自己随便做个例子


汇编

 1目标文件，Linux二进制可执行文件，静态库，动态库

 32 位ELF文件,有兴趣搜索一下ELF的格式

命令readelf 读取


readelf -h target.o


链接

 链接是编译过程最后一个阶段，将一个或者多个目标文件和库
链接成一个单独文件





构建工具链

 
Binutils

GCC

Glibc


linux 还可以嵌入式，嵌入式有多种CPU体系结构


使用交叉编译可以编译代码到嵌入式


简单来说就是 我们本来X86 代码编译后到别的APM平台 


构建完整的交叉编译器 