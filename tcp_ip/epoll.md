epoll是事件非阻塞，而不是IO非阻塞,这是大家的一个误区，有问题看源码


epoll是新建一个文件
1. int epoll_create(int size);

2. int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);

第一个参数是epoll_create()的返回值。
第二个参数表示动作，用三个宏来表示：
EPOLL_CTL_ADD：注册新的fd到epfd中；
EPOLL_CTL_MOD：修改已注册的fd的监听事件；
EPOLL_CTL_DEL：从epfd中删除一个fd；
第三个参数是需要监听的fd。




EPOLLIN ：表示对应的文件描述符可以读（包括对端SOCKET正常关闭）；
EPOLLOUT：表示对应的文件描述符可以写；
EPOLLPRI：表示对应的文件描述符有紧急的数据可读（这里应该表示有带外数据到来）；
EPOLLERR：表示对应的文件描述符发生错误；
EPOLLHUP：表示对应的文件描述符被挂断；
EPOLLET： 将EPOLL设为边缘触发(Edge Triggered)模式，这是相对于水平触发(Level Triggered)来说的。
EPOLLONESHOT：只监听一次事件，当监听完这次事件之后，如果还需要继续监听这个socket的话，需要再次把这个socket加入到EPOLL队列里


typedef union epoll_data {  
    void *ptr;  
    int fd;  
    __uint32_t u32;  
    __uint64_t u64;  
} epoll_data_t;  


 //感兴趣的事件和被触发的事件  
struct epoll_event {  
    __uint32_t events; /* Epoll events */  
    epoll_data_t data; /* User data variable */  
};  


内存映射（mmap）技术


每一个事件都会建立一个epitem结构体


epoll还维护了一个双链表，用户发生的事件。当epoll_wait调用时，仅仅观察这个list链表里有没有数据eptime项即可。有数据就返回，没有数据就sleep，等到timeout时间到后即使链表没数据也返回。

epoll所有的handler保存在一个eventpoll(红黑树)

epoll_create时，创建了红黑树和就绪链表，执行epoll_ctl时，如果增加socket句柄，则检查在红黑树中是否存在，存在立即返回，不存在则添加到树干上，然后向内核注册回调函数，用于当中断事件来临时向准备就绪链表中插入数据。执行epoll_wait时立刻返回准备就绪链表里的数据即可。

anon_inode_getfd("[eventpoll]", &eventpoll_fops, ep,
             O_RDWR | (flags & O_CLOEXEC));

2 epoll所管理的所有的句柄都是放在一个大的结构eventpoll(红黑

  file = fget(epfd);
    /* Get the "struct file *" for the target file */
    tfile = fget(fd);

3.每次通过epoll fd 可以得到eventpoll

kmem_cache_alloc(epi_cache, GFP_KERNEL)

4.eventpoll 有两个queue

  epoll_wait(wq)

  poll_wait

wait queue(pwqlist)

queue是 fd私有wait

struct epitem {


    struct rb_node rbn;

    struct list_head pwqlist;

    struct eventpool *ep;
};


struct eventpoll {
      spinlock_t lock;
          

      struct mutex mtx;

       wait_queue_head_t wq;
       
      wait_queue_head_t poll_wait;

      struct list_head rdlist;
 
      struct rb_root rbr;

      struct epitem  *ovlist;
};







加入的epoll 都是 red black tree 的节点
默认是POLLERR POLLHUP

初始化eventpoll


 switch (op) {
      case EPOLL_CTL_ADD:
         if (!epi) {
              epds.events |= POLLERR | POLLHUP;
              error = ep_insert(ep, &epds, tfile, fd);
         } else 
               error = -EEXIST;
         break;


ep_poll_callback 绑定epitem 的wait queue 回调
ep_poll_callback

epoll有一个read_list ,有了所有事件句柄，其实就是
网络模型Reactor,


static int ep_poll_callback(wait_queue_t *wait,
                            unsigned mode,
                            int sync,
                            void *key)
{
     struct epitem *epi = ep_item_from_wait(wait);
     struct eventpoll *ep = epi->ep;
  

      if (!ep_is_linked(&epi->rdlink)
          list_add_tail(&epi->rdlink, &ep->rdlist);

系统调用epoll_wait,如果read list ，休眠等待会唤醒


rdlist 复制到新的list(LT模型),然后ep_send_events_proc

对这个心的list进行遍历


if (list_empty(&ep->rdlist)) {


       init_waitqueue_entry(&wait, current);
     __add_wait_queue_exclusive(&ep->wq, &wait);

     for (;;) {


        set_current_state(TASK_INTERRUPTIBLE);
        if(!list_empty(&ep->rdllist) || timed_out)
            break;
        if (signal_pending(current)) {
            res = -EINTR;
            break;
        }
 
    spint_unlock_irqrestore(&ep->lock, flags);
    if (!schedule_hritemout_range(to, slack, HRIMER_MODE_ABS))
       timed_out = 1;
      
    spint_lock_inrqsave(&ep->lock, flags);



 LT和ET的区别是在ep_send_events_proc中处理的，如果是LT，不但会将对应的数据返回给用户，并且会将当前的epitem再次加入到rdllist中。这样子，如果下次再次被唤醒就会给用户空间再次返回事件.



10 eventpol还有一个list，叫做ovflist，主要是解决当内核在传输数据给用户空间(ep_send_events_proc)时的锁(eventpoll->mtx)，此时epoll就是将这个时候传递上来的事件保存到ovflist中。