工具链

gcc实际上不是一个编译器，是个驱动程序(driver program)
gcc 编译过程中的每一个环节由具体的组件负责

编译过程由cc1负责,汇编过程由as负责,链接过程ld负责

gcc就是用collect2安排初始化过程中

预编译、编译、汇编、链接


        Source code file
               |
               |
               |
         Preprocessor
               |
               |
               |