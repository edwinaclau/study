##slabs 子系统分配

每个 slab 是MB单位

* slab 划分多个page, 一个 page 大小固定为 1MB



* page 划分多个 chunk,一个page中chunk大小相同


##回收已分配的chunk(LRU)


	* Memcached内存管理采取预分配、分组管理的方式，分组管理就是* * 划分slab class，按照chunk的大小slab被分为很多种类。

#slab
####Slab是一个内存块，它是memcached一次申请内存的最小单位。
在启动memcached的时候一般会使用参数-m指定其可用内存，但是并不是在启动的那一刻所有的内存就全部分配出去了，只有在需要的时候才会去申请，而且每次申请一定是一个slab。

####Slab的大小固定为1M(1048576 Byte),一个slab由若干个大小相等的chunk组成。每个chunk中都保存了一个item结构体、一对key和value。

###chunk
#同一个slab中chunk的大小相等的，但是在不同的slab中chunk的大小并不一定相等.

在memcached中按照chunk的大小不同，可以把slab分为很多种类(class)

###新增item
#向memcached添加一个item时候，memcached首先会根据item的大小，来选择最合适的slab class。

###例如item的大小为190字节，默认情况下class 4的chunk大小为160字节显然不合适，class 5的chunk大小为200字节，大于190字节，因此该item将放在class 5中（显然这里会有10字节的浪费是不可避免的）。

###计算好所要放入的chunk之后，memcached会去检查该类大小的chunk还有没有空闲的，如果没有，将会申请1M（1个slab）的空间并划分为该种类chunk。

###在class1中，剩余的16字节因为不够一个chunk的大小（80byte），因此会被浪费掉。每类chunk的大小有一定的计算公式的，假定i代表分类，###class i的计算公式如下：
###chunk size(class i) :  (default_size+item_size)*f^(i-1)###+ CHUNK_ALIGN_BYTES
###default_size: 默认大小为48字节,也就是memcached默认的key+value的大小为48字节，可以通过-n参数来调节其大小；
###item_size: item结构体的长度，固定为32字节。default_size大小为48字节,item_size为32，因此class1的chunk大小为48+32=80字节；
###f为factor，是chunk变化大小的因素，默认值为1.25，调节f可以影响###chunk的步进大小，在启动时可以使用-f来指定;
###CHUNK_ALIGN_BYTES是一个修正值，用来保证chunk的大小是某个值的整数倍（在32位机器上要求chunk的大小是4的整数倍）。
###从上面的分析可以看到，我们实际可以调节的参数有-f、-n，在memcached的实际运行中，我们还需要观察我们的数据特征，合理的调节f，n的值，使我们的内存得到充分的利用减少浪费。


##分布式/hash
memcached本身是集中式的缓存系统，要搞多节点分布，只能通过客户端实现：
* 1.hash结果
* 2.一致性hash
* Memcached的item保存基于一个大的hash表，它的实际地址就是slab中的chunk偏移，但是它的定位是依靠对key做hash的结果，在primary_hashtable中找到的。在assoc.c和items.c中定义了所有的hash和item操作

##链接数
####Memcached使用libevent库实现网络连接服务，理论上可以处理无限多的连接，但是它和Apache不同，它更多的时候是面向稳定的持续连接的，所以它实际的并发能力是有限制的。在保守情况下memcached的最大同时连接数为200，这和Linux线程能力有关系，这个数值是可以调整的。

##启动过程
* 1 、调用 settings_init() 设定初始化参数
* 2 、从启动命令中读取参数来设置 setting 值
* 3 、设定 LIMIT 参数
* 4 、开始网络 socket 监听（如果非 socketpath 存在）（ 1.2 之后支持 UDP 方式）
* 5 、检查用户身份（ Memcached 不允许 root 身份启动）
* 6 、如果有 socketpath 存在，开启 UNIX 本地连接（Sock 管道）
* 7 、如果以 -d 方式启动，创建守护进程（如上调用 daemon 函数）
* 8 、初始化 item 、 event 、状态信息、 hash 、连接、 slab
* 9 、如设置中 managed 生效，创建 bucket 数组
* 10 、检查是否需要锁定内存页
* 11 、初始化信号、连接、删除队列
* 12 、如果 daemon 方式，处理进程 ID
* 13 、event 开始，启动过程结束， main 函数进入循



