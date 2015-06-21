linux下，可执行文件格式是ELF格式，程序中数据在逻辑上大致可以分成下面几个大的区域：
Ÿ  Text: 执行的指令序列流，是只读内存区（编译期就决定了其内容）；.
Ÿ  Data: 程序所使用的静态变量和全局变量区（编译期就决定了其内容）；
Ÿ  Heap: 堆，进程动态申请的内存区，使用new，malloc操作申请的内存；
Ÿ  Stack:栈，动态增长和收缩的内存区，函数参数，返回值，调用栈，局部变量存放区域；

其中Data区域其实可以进一步细分为更多section，下面我们具体看看
static int val_a = 1; // 初始化的静态变量
int val_b = 2;        // 全局变量
const int val_c = 3;  // const 全局变量
static int val_d;     // 未初始化的静态变量
int val_e;            // 未初始化的全局变量
int main(int argc, char *argv[])
{
    static int val_f = 5;  // 初始化的局部静态变量
    static int val_g;      //未初始化局部静态变量
    int    val_h = 6;      //初始化局部变量
    int    val_i;          //未初始化局部变量
    const  int val_j = 7;  //const局部变量
    return 0;
}

g++ main.cpp -o test

通过objdump命令查看各种变量分布位置
objdump -t -T  test | grep 'val'
000000000060095c l     O .data  0000000000000004              _ZL5val_a
000000000060097c l     O .bss   0000000000000004              _ZL5val_d
0000000000400678 l     O .rodata        0000000000000004      _ZL5val_c
0000000000600980 l     O .bss   0000000000000004              _ZZ4mainE5val_g
0000000000600964 l     O .data  0000000000000004              _ZZ4mainE5val_f
0000000000600960 g     O .data  0000000000000004              val_b
0000000000600978 g     O .bss   0000000000000004              val_e

做一下总结
data 区存放初始化的全局变量和静态变量
bss  区存放未初始化的全局变量和静态变量
rodata 区存放只读的数据，const变量

其中 val_h, val_i,是局部变量，在进程启动main函数执行后，在栈里面分配；
val_j 虽然是const 变量，也是在栈里面分配
