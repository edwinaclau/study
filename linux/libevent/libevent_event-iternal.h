
事件处理框架-event_base 
回想Reactor模式的几个基本组件，本节讲解的部分对应于Reactor框架组件。在libevent
中，这就表现为event_base结构体，结构体声明如下，它位于event-internal.h文件中


//add init del 注册 删除 初始化 事件

struct eventop {
      const char *name;
	  void   *(*init)(struct event_base *);
	  int    (*add)(void *, struct event *);
	  int    (*del)(void *, struct event *);
	  int    (*dispatch)(struct event_base * , void *)
	  void   (*dealloc)(struct  event_base * , void *);
	  int need_reinit;
};

在后面会再次提到。
2）activequeues是一个二级指针，前面讲过libevent支持事件优先级，因此你可以把它
看作是数组，其中的元素activequeues[priority]是一个链表，链表的每个节点指向一个优先
级为priority的就绪事件event。
3）eventqueue，链表，保存了所有的注册事件event的指针。
4）sig是由来管理信号的结构体，将在后面信号处理时专门讲解；
5）timeheap是管理定时事件的小根堆，将在后面定时事件处理时专门讲解；
6）event_tv和tv_cache是libevent用于时间管理的变量，将在后面讲到；

struct event_base {
	const struct eventop *evsel;
	void *evbase;
	int event_count;
	int event_count_active;

	int event_gotterm;
	int event_break;

	struct event_list *activeQueues;
	int nactivequeues;

	struct evsignal_info sig;


	struct event_list eventqueue;

	struct timeval event_tv;

	struct 



   
}
