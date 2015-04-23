Redis 是一个事件驱动
   Reactor模式

启动服务器-->否->等待文件事件产生-->处理已产生事件-->处理已到达事件


typedef struct aeFiredEvent {  
    int fd;  
    int mask;  
} aeFiredEvent;  
  
/* State of an event based program */  
typedef struct aeEventLoop {  
    int maxfd;  
    long long timeEventNextId;  
    aeFileEvent events[AE_SETSIZE]; /* Registered events */  
    aeFiredEvent fired[AE_SETSIZE]; /* Fired events */  
    aeTimeEvent *timeEventHead;  
    int stop;  
    void *apidata; /* This is used for polling API specific data */  
    aeBeforeSleepProc *beforesleep;  
} aeEventLoop;  



/* File event structure */  
typedef struct aeFileEvent {  
    int mask; /* one of AE_(READABLE|WRITABLE) */用来区分读写事件  
    aeFileProc *rfileProc;   读文件事件的处理函数  
    aeFileProc *wfileProc;  写文件事件的处理函数  
    void *clientData;  
} aeFileEvent;  
aeTimeEvent则是定时响应的事件的抽象  
/* Time event structure */  
typedef struct aeTimeEvent {  
    long long id; /* time event identifier. */  
    long when_sec; /* seconds */  事件响应点的秒时刻  
    long when_ms; /* milliseconds */事件响应的毫秒时刻  
    aeTimeProc *timeProc;  事件响应函数  
    aeEventFinalizerProc *finalizerProc;  
    void *clientData;  
    struct aeTimeEvent *next;  下一个要响应的时间事件  
} aeTimeEvent  



aeEventLoop aeFileEvent awTimeEvent

aeEventLoop

     timeEventNextid
   
     events

     fired

      aeTimeEvent


其中 events ----> events 结构---> aeFileEvent


fired ---> fired队列

aeTimeEvent
   mask
   when_sec
   when_ms
   timeProc




aeCreateEventLoop()




  aeMain() ------>beforeSleep()

                       |
                       |
                       |

                    aeProcessEvents()---> aeApiPoll



aeApiCreate：调用epoll_create创建epoll的句柄，并分配epoll事件。

aeApiFree：调用close关闭epoll_create创建的epoll句柄，并释放epoll事件。

aeApiAddEvent：调用epoll_ctl向aeEventLoop中添加一个事件。

aeApiDelEvent：调用epoll_ctl从aeEventLoop中删除一个事件。


