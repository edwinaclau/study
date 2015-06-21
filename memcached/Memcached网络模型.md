Memcached ---->  libevent

依赖于，其实没啥的，很多都是开始时候依赖 libevent ,网络模型是Reactor


 主线程   绑定 event_base 在监听接口监听网络连接


 再分发给其它的    worker线程， 每个 worker线程都自身的 evet-base


 主线程的任务就是监听网络，如果监听到了连接就顺序分发到worker线程，通过管道通知worker线程建立连接（调用accept函数，这样调用accept肯定能得到连接的fd）


每一个worker线程都维护一个CQ队列，主线程把fd和一些信息写入一个CQ_ITEM里面，然后主线程往worker线程的CQ队列里面push这个CQ_ITEM


typedef struct conn_queue_item CQ_ITEM;

struct conn_queue_item {
        int                   sfd;
		enum conn_states      init_sate;
		int                   event_flags;
		int                   read_buffer_size;
		enum network_transport  transport;
		CQ_ITEM               *next;
};


typedef struct conn_queue CQ;
struct conn_queue {
        CQ_ITEM *head;
		CQ_ITEM *tail;
		phtread_mutex_t  lock;
};


                   struct conn_queue
				   CQ_ITEM*        head
				   phtread_mutex_t lock
				   CQ_ITEM*        tail
就是一个链表

work线程CQ队列

typedef struct {
         phtread_t   thread_id;
		 struct event_base *base;
		 struct event    notify_event;
		 int notify_receive_fd;
		 int notffy_send_id;
		 struct conn_queue *new_conn_queue;
} LIBEVENT_THREAD;



LIBEVENT_THREAD 





CQ_ITEM内存池
     memcached 申请 一个CQ_ITEM结构体，并不是直接使用malloc 申请



主线程的工作



  接到了请求了之后，会顺序分配给每个worker线程，把这个连接的sfd所关心的初始状态和事件和readbuf，作为一个entry放到worker进程的连接队列中，同时向那个worker的线程的管道的notify_ receive_fd写入‘c’,提示worker进程有连接，每个worker线程有个连接队列，做缓冲，为了防止worker新连接产生的过快，worker线程处理速度过慢。
