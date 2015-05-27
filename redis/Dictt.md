    
    typedef struct dictht {
      
       dictEntry **table;
    
       unsigned long size;
    
       unsigned long sizemark;
    
       unsigned long used;
    
    } dictht;






字典



redis自带一个哈希算法
MurmurHash2

冲突使用链表解决

rehash
防止一次性rehash造成服务器停止工作


dictDelete

    typedef struct dictEntry {
       void *key;
       void *val;
       struct dictEntry *next;
    } dictEntry;
    





    typedef struct dictType {
     unsigned int (*hashFunction)(const void *key);
     void *(*keyDup)(void *privdata, const void *key);
     void *(*valDup)(void *privdata, const void *obj);
     int  (*KeyCompare)(void *privdata, void *key)
     void (*keyDestructor)(void *privdata, void *key);
     void (*valDestructor)(void *privdata, void *obj);
    } dictType;




哈希表结构dictht:


    typedef struct dictht {
        dictEntry **table;
        unsigned long size;
        unsigned long sizemask;
        unsigned long used;
    } dictht;





    typedef struct dict {
       dictType  *type;
       void *privdata;
       dictht   ht[2];
       int rehashidex;
       int iterators;
    } dict;


字典迭代器


    typedef struct dictIterator {
    dict *d;
    int table, index, safe;
    dictEntry  *entry, *nextEntry;
    } dictIterator;
    


int dictExpand(dict *d, unsigned long size)  


于传入的参数：新哈希表的大小size，首先调用内部函数_dictNextPower(size)取得大于size的最小2次幂整数，作为哈希表大小。掩码sizemask为size二进制表示长度减一的全1表示。调用内存管理函数zcalloc分配新哈希表的内存。

接下来，函数判断这是否是哈希表的首次初始化，这通过判断字典的哈希表数组ht的首个元素的dictEntry是否为空实现，如果为空，说明是首次初始化，则将该哈希表的size设为n，直接返回DICT_OK；否则，说明这是一次rehash，那么函数将准备第二个哈希表d->ht[1]，并将d的rehashidx设为0，准备进行后续的增量哈希，然后返回DICT_OK。

    dict->ht ----> ht[0]
     dictht
     table
     size
     sizemark
     used
    
    
    
    
    
    
    
     ----> ht[1] 
       dictht
       table
       size
       sizemark
       used
    


rehash

   哈希表键值或多或少，为了让哈希表(load factor)
维持一个合理范围

哈希表保存键值太多或者太少，需要对哈希表扩展或收缩

rehash

ht[0].used 大于 htp[0].used *2

如果



2)将ht[0]所有的键值rehash到ht[1]上



扩展哈希表

* redis 为每个数据集配备两个哈希表，能在不中断服务的情况下扩展哈希表。平时哈希表扩展的做法是，为新的哈希表另外开辟一个空间，将原哈希表的数据重新计算哈希值，以移动到新哈希表。如果原哈希表数据过多，中间大量的计算过程会耗费大量时间。

* redis 扩展哈希表的做法有点小聪明：为第二个哈希表分配新空间，其空间大小为原哈希表键值对数量的两倍（是的，没错），接着逐步将第一个哈希表中的数据移动到第二个哈希表；待移动完毕后，将第二个哈希值赋值给第一个哈希表，第二个哈希表置空。在这个过程中，数据会分布在两个哈希表，这时候就要求在 CURD 时，都要考虑两个哈希表。

* 而这里，将第一个哈希表中的数据移动到第二个哈希表被称为重置哈希（rehash）。

* 重置哈希表

* 在 CURD 的时候会执行一步的重置哈希表操作，在服务器定时程序 serverCorn() 中会执行一定时间的重置哈希表操作。为什么在定时程序中重置哈希表了，还 CURD 的时候还要呢？或者反过来问。一个可能的原因是 redis 做了两手准备：在服务器空闲的时候，定时程序会完成重置哈希表；在服务器过载的时候，更多重置哈希表操作会落在 CURD 的服务上。

* 下面是重置哈希表的函数，其主要任务就是选择哈希表中的一个位置上的单链表，重新计算哈希值，放到第二个哈希表。
