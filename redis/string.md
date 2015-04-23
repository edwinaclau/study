动态字符串


 struct sdshdr {


            int len;

            int free;
       
            char buf[];
};

SDS和C的字符串一样，最后保留\0


有字段记录 len

缓冲溢出  


减少字符串 内存分配次数

