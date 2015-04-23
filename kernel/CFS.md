调度


抢占式和非抢占式



 进程是(CPU-bound) 和 I/O(I/O-bound)


进程分3种

交互式


批处理进程


实时处理进程


SCHED_NORMAL  默认


SCHED_FIFO    先到先出


SCHED_RR     时间片轮训


SCHED_BATCH  批处理



SCHED_IDLE   最低的优先级



nice   ps将可以列出来


nice 值 -20~19,较高数字会运行优先较低，反之亦然



优先级 static priority


动态优先级



实时级



时间片 



  完全公平调度CFS

（1）运行队列



(2)时间片的影响


(3)优先级计算的时机


(4)支持抢占

(5)负责均衡


进程调度的目标



高效

加强交互性


保持公平

SMP调度

软实时调度


进程的nice值




O(1)调度器

每一个CPU维护一个运行队列



struct runqueue,含有两个优先级数组

一个是active数组，另外一个过期优先级(expired)



active 时间片没用完

expired 时间片


Priority 0        进程   进程 


Priority 1        进程   进程

 .
 .
 .
 .
 .
Priority 99        进程 进程


每个优先级数组MAX_PRIO



(2) 时间片的影响



(3) 优先级计算的时机



(4)支持内核抢占


(5) 负载均衡


SD调度器






CFS 公平调度器



CPU 计算时间



当一个进程占用CPU，其他进程必须等待，

CFS引入了虚拟运行事件(virtual)


进程由权重优先级决定，实际运行事件相同，虚拟运行时间越来越小


CFS算法每次调度，选择运行队列 虚拟运行时间最小的进程

