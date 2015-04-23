容错


扩容



负载均衡



退休


lighthttp
libevent
JavaNIO

one loop per thread

每个IO线程都由一个event loop

这种方式的好处是:

  线程数目基本固定，

  方便线程调配方案

  IO事件发生的线程是固定的

EventLoop代表了线程的主循环，需要让哪个线程干活

    把timer 或 IO channed 
注册到哪个线程 的loop即可.

实时性有要求单独用一个线程

数量大connection 毒战一个线程

数据处理任务 分摊 计算线程用(线程池)

non

多线程 的话是有 线程安全要求的 允许线程每个

基于事件驱动的编程模型也有本质的缺点


  事件回调必须是非阻塞


多线程服务器常用模型


 

推荐模式



    event loop 用作 IO multiplexing,配合 Non blocking


    thread pool 用来计算，任务队列  生产者 消费者

  

进程间通信只用TCP


 Sockets(TCP,UDP)



Linux 进程间通信只用

   Linux进程间通信(IPC)   pipe


   FIFO

    POSIX 消息队列

   信号(signals)

   同步原语(synchronization primitives)

   互斥器(mutex)
   
   条件变量(condition variable)

   读写锁(reader-writer lock)

   文件(record locking)

   信号量(semaphore)

进程间sockets


  TCP sockets pipe 操作文件描述符


TCP port 由一个进程独占,操作系统自动回收

两个进程通过TCP通信





  还有port 独占,

使用TCP字节流(byte stream) marshal/unmarshal 开销




多线程服务器的适合


  服务器开发 一个基本任务处理并发连接



当 线程 廉价 ，一台机器上 创建远高于CPU线程

Python gevent Go gorutine Erlang actor


线程 宝贵 ，创建于CPU数目相当的线程




必须用单线程的场合

1. 程序可能会fork(2)

2.  限制程序的CPU占用率

只有单线程程序 fork(2)


1.立即执行exec()


2.不调用exec


单线程的优缺点

 Eventloop有一个明显缺点，非抢占(non-preemptive)

 多线程程序有性能优势

使用多线程场景


    多个CPU可用

线程间有共享数据


共享的数据可以修改

提供非均的服务

latency throughtput


利用异步操作


能scale up



多线程问题的困难思想


当前线程随时切换或被


线程程序事件的发生顺序不再有全局统一的先后关系




   单CPU系统中，理论上可以通过CPU执行指令的先后顺序来推演多线程

   多核系统中，多个线程是并行


多线程正确性不能依赖一个线程的执行速度

2个 线程的创建和等待结束(join)

不推荐使用读写所是原因往往
写操作会发生阻塞