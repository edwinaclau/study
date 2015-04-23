
内存中的物理内存页的管理

分配大块内存的伙伴系统

分配较小块内存的slab、slub、和slob分配器
分配非连续内存块的vmalloc机制
进程的地址空间


Linux处理器的虚拟地址空间划分为两个部分。

(1)UMA计算机(一致内存访问)


(2)NUMA计算机(非一致内存访问)



两种类型计算机混合



ZONE_DMA标记DMA的内存域


ZONE_DMA32


ZONE_NORMAL

ZONE_HIGHMEM


typedef sturct pglist_data {
        struct zone node_zones[MAX_NR_ZONES];
        struct zonelist node_zonelists[
        int nr_zones;




} pg_data_t;

node_zones 是一个数组，包含所有节点

node_zonelists


node_mem_map


enum node_states {

  N_POSSIBLE,
  N_ONLINE,
};



32位系统，0x~0xFFFFFFFF

高地址的1GB就是内核


Kmem

Stack

Heap

BSS

DATA

TEXT

分页 Frame 或 page

2的为主


struct page {


flag 是个页面状态

_count 内存页引用次数

内核page结构，是否空闲，给谁使用


内核结构NUMA


Node --->Zone---->Page


Linux x86 Zone

ZONE_DMA(0~16MB)


ZONE_NORMAL (16MB~896MB)


ZONE_HIGHMEM(896MB~)




page_data_t

pages_min

pages_low

pages_high


                Node

zone:DMA         ZONE:Normal  zone


Buddy            Buddy           Buddy



SLAB


cache                slab           object

/proc/meminfo
/proc/zoneinfo



BUDDY

减少内存碎片



例如一个楼房

有20 40 60 80 100 120 140 160平方的住宅


/proc/buddyinfo 页面分配情况


GFP标志


__GFP_HIGH

__GFP_WAIT


__GFP_IO



Cache chain

  Kmem_cache


Kmem_cache

Kmem_cache






SLAB 缺点，缓存队列复杂，

所以有了SLUB 简化kmem_cache


SLUB分配器，一个SLAB是一组连续的物理内存页框
固定方数房子，没有额外空闲对象，就算重用也是自身

SLUB分配器描述了struct page 加入 freelist 和 SLAB union字段


SLUB具有kmem_cache 合并功能

内核




kmalloc()函数得到内存是SLAB内存对象

