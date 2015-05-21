 ```c

typedef struct zskiplistNode {  
    robj *obj; //节点数据  
    double score;  
    struct zskiplistNode*backward; //前驱  
    struct zskiplistLevel {  
        struct zskiplistNode*forward;//后继  
        unsigned int span;//该层跨越的节点数量  
    } level[];  
} zskiplistNode;  
   
typedef struct zskiplist {  
    struct zskiplistNode*header, *tail;  
    unsigned long length;//节点的数目  
    int level;//目前表的最大层数  
} zskiplist;

```

跳跃表最主要实现比较简单直观

这就是为何不实现其它 复杂的数据结构例如AVL RBT 

查找，删除，插入 都可以再


新建返回一个跳表节点  O(1)


新建并初始化一个跳跃表 O(L)

释放给定的节点      slFreeNode


zslRandomLevel    得到新节点层数



zslInsert  O(logN)


zslDeleteNode    删除给定的跳表节点




其实中心思想就是随机分层索引，

假如元素有8个


第一层索引 节点有 两个

第二层索引  节点有四个

第三层索引  遍历所有节点

