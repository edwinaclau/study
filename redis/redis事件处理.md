````c

#ifdef HAVE_EPOLL
#include "ae_epoll.c"
#else
    #ifdef HAVE_KQUEUE
    #include "ae_kqueue.c"
    #else
    #include "ae_select.c"
    #endif
#endif

```

redis是单线程多路,event driver

redis 支持select,kqueue,epoll


````c
#ifdef HAVE_EPOLL
#include "ae_epoll.c"
#else
    #ifdef HAVE_KQUEUE
    #include "ae_kqueue.c"
    #else
    #include "ae_select.c"
    #endif
#endif
````

````c
ae_select.c 、ae_epoll.c ae_kqueue.c

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

````
````c

maxfd当前最大文件描述符id,timeEventNextId是下一个timer
的id,


event和fired分别保存已经注册和已释放的文件event


timeEventHead

apidata保存了


typedef struct aeFileEvent {
    int mask; 
    aeFileProc  *rfileProc;
    aeFileProc  *wfileProc;
    void        *clientData;
} aeFileEvent;

````


系统中的timer事件使用一个链表，每个timer有一个唯一的id,

该timer在when_sec,when_ms后调用



typedef struct aeTimeEvent {
   long long id;
   logn when_sec;
   long when_ms;
   aeTimeProc *timeProc;
   aeEventFinalizerProc  *finalizerProc;
   void *clientData;
   struct aeTimeEvent   *next;
} aeTimerEvent;
