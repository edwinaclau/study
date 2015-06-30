一）模型分析

####memcached到底是如何处理我们的网络连接的？

####memcached通过epoll（使用libevent，下面具体再讲）实现异步的服务器，但仍然使用多线程，主要有两种线程，分别是“主线程”和“worker线程”，一个主线程，多个worker线程。

####主线程负责监听网络连接，并且accept连接。当监听到连接时，accept后，连接成功，把相应的client fd丢给其中一个worker线程。
worker线程接收主线程丢过来的client fd，加入到自己的epoll监听队列，负责处理该连接的读写事件。

####所以说，主线程和worker线程都各自有自己的监听队列，主线程监听的仅是listen fd，而worker线程监听的则是主线程accept成功后丢过来的client fd。

####memcached使用libevent实现事件监听。在这简单介绍一下libevent的使用，一般有以下几步：

* 1）event_base = event_init(); 初始化事件基地。

* 2）event_set(event, fd, event_flags, event_handler, args); 创建事件event，fd为要监听的fd，event_flags为监听的事件类型，event_handler为事件发生后的处理函数，args为调用处理函数时传递的参数。

* 3）event_base_set(event_base, event); 为创建的事件event指定事件基地。

* 4）event_add(event, timeval); 把事件加入到事件基地进行监听

* 5）event_base_loop(event_base, flag); 进入事件循环，即epoll_wait

##memcached主线程和worker线程各有自己的监听队列，故有主线程和每个worker线程都有一个独立的event_base，事件基地。

##了解libevent的简单使用后，我们回到memcache线程模型上，先看看下面的图片了解它线程模型的构建逻辑：

 

##memcached线程模型


* 1）主线程首先为自己分配一个event_base，用于监听连接，即listen fd。

* 2）主线程创建n个worker线程，同时每个worker线程也分配了独立的event_base。

* 3）每个worker线程通过管道方式与其它线程（主要是主线程）进行通信，调用pipe函数，产生两个fd，一个是管道写入fd，一个是管道读取fd。worker线程把管道读取fd加到自己的event_base，监听管道读取fd的可读事件，即当主线程往某个线程的管道写入fd写数据时，触发事件。

* 4）主线程监听到有一个连接到达时，accept连接，产生一个client fd，然后选择一个worker线程，把这个client fd包装成一个CQ_ITEM对象（该结构体下面再详细讲，这个对象实质是起主线程与worker线程之间通信媒介的作用，主线程把client fd丢给worker线程往往不止“client fd”这一个参数，还有别的参数，所以这个CQ_ITEM相当于一个“参数对象”，把参数都包装在里面），然后压到worker线程的CQ_ITEM队列里面去（每个worker线程有一个CQ_ITEM队列），
 同时主线程往选中的worker线程的管道写入fd中写入一个字符“c”（触发worker线程）。

* 5）主线程往选中的worker线程的管道写入fd中写入一个字符“c”，则worker线程监听到自己的管道读取fd可读，触发事件处理，而此是的事件处理是：从自己的CQ_ITEM队列中取出CQ_ITEM对象（相当于收信，看看主线程给了自己什么东西），从4）可知，CQ_ITEM对象中包含client fd，worker线程把此client fd加入到自己的event_base，从此负责该连接的读写工作。

##二）代码实现

##下面我们看一下memcached线程模型的具体代码实现：

首先看下main函数中关键的几行：
    1. //main_$1
    2.main_base = event_init(); //全局的main_base变量
    3. 
    4.//main_$2
    5.//初始化主线程，参数是worker线程个数，和当前主线程的event_base
    6.thread_init(settings.num_threads, main_base);
    7. 
    8.//main_$3 
    9.//建立sockets
    10.if (settings.port && server_sockets(settings.port, tcp_transport,
    11. 
    12.portnumber_file)) {
    13.vperror("failed to listen on TCP port %d", settings.port);
    14.exit(EX_OSERR);
    15.}
    16. 
    17.//main_$4
    18. 
    19.//进入事件循环
    20. 
    21.if (event_base_loop(main_base, 0) != 0) {
    22.retval = EXIT_FAILURE;
    23.}
    

上述代码中：

main_$1就是给主线程自己分配了一个event_base，而最后在main_$4那里进入事件循环。

而main_$2，初始化线程工作，其中包括：1）对主线程的初始化 2）创建worker线程

main_$1创建event_base，main_$4进入事件循环，那么漏了的为创建事件，为事件绑定事件处理函数在哪些设置了？

其实就是在main_$3处，server_sockets函数的作用就是创建socket，bind，listen，并把listen fd加到主线程的event_base中，同时绑定事件处理函数。

2）我们来具体看server_sockets函数：主线程监听listen fd
1. static int server_sockets(int port, enum network_transport transport,
2.                          FILE *portnumber_file) {
3.    if (settings.inter == NULL) {
4.        return server_socket(settings.inter, port, transport, portnumber_file);
5.    }
6. //。。。
7. 
8.}
9.static int server_socket(const char *interface,
10.                         int port,
11.                         enum network_transport transport,
12.                         FILE *portnumber_file) {
13.    int sfd;
14.    for (next= ai; next; next= next->ai_next) {
15.        conn *listen_conn_add;
16.        if ((sfd = new_socket(next)) == -1) { //创建socket
17.            //。。。
18.        }
19.        setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, (void *)&flags, sizeof(flags));
20.        if (bind(sfd, next->ai_addr, next->ai_addrlen) == -1) {   //bind
21.            //。。。
22.        }else{
23.            success++;
24.            if (!IS_UDP(transport) && listen(sfd, settings.backlog) == -1) { //listen
25.                perror("listen()");
26.                close(sfd);
27.                freeaddrinfo(ai);
28.                return 1;
29.            }
30. 
31.        }
32.        if (IS_UDP(transport)) {
33.            //。。。
34.        } else {
35.            //创建主线程 监听 连接，conn_state 为conn_listening
36.            if (!(listen_conn_add = conn_new(sfd, conn_listening,
37.                                             EV_READ | EV_PERSIST, 1,
38.                                             transport, main_base))) {
39.                //。。。
40.            }
41.            listen_conn_add->next = listen_conn;
42.            listen_conn = listen_conn_add;
43.        }
44.    }
45. 
46.//。。。
47.}


上面的代码是经典的监听连接过程，而在最后调用了一个函数conn_new：
1. conn *conn_new(const int sfd, const int init_state, const int event_flags,  
2.                    const int read_buffer_size, const bool is_udp, struct event_base *base) {  
3.          
4.            conn *c;
5. 
6.            c->state = init_state;
7.     //   。。。  
8. 
9.            event_set(&c->event, sfd, event_flags, event_handler, (void *)c);   //在这里创建事件，并指定事件处理函
10.                                                                   //数为event_handler
11.            event_base_set(base, &c->event);  
12.            c->ev_flags = event_flags;  
13.            if (event_add(&c->event, 0) == -1) {  
14.            if (conn_add_to_freelist(c)) {  
15.                conn_free(c);  
16.            }  
17.            return NULL;  
18.            }  
19.       // 。。。  
20. }


上面的conn_new函数主要是为主线程的event_base创建事件，并设置了事件处理函数为event_handler。最后event_base_loop()进入事件循环，开始监听listen fd的可读事件。

3）主线程监听listen fd这边，我们先暂时一下，回到main函数中的main_$2部分，即
1. thread_init(settings.num_threads, main_base);


这一行代码中，这里对主线程的初化始化到底都做了些什么？我们看看thread_init的实现：
1.//初始化主线程
2.void thread_init(int nthreads, struct event_base *main_base) {
3. 
4. 
5.//。。。省略一些锁的初始化。。
6. 
7. 
8. 
9.    threads = calloc(nthreads, sizeof(LIBEVENT_THREAD)); //创建nthreads个worker线程对象
10. 
11.    if (! threads) {
12.        perror("Can't allocate thread descriptors");
13.        exit(1);
14.    }
15. 
16.    dispatcher_thread.base = main_base; //设置主线程对象的event_base
17.    dispatcher_thread.thread_id = pthread_self(); //设置主线程对象pid
18. 
19.    for (i = 0; i < nthreads; i++) { //为每个worker线程创建与主线程通信的管道
20.        int fds[2];
21.        if (pipe(fds)) {
22.            perror("Can't create notify pipe");
23.            exit(1);
24.        }
25. 
26.        threads[i].notify_receive_fd = fds[0]; //worker线程管道接收fd
27.        threads[i].notify_send_fd = fds[1]; //worker线程管道写入fd
28. 
29.        setup_thread(&threads[i]); //装载 worker线程
30.        stats.reserved_fds += 5;
31.    }
32. 
33.    for (i = 0; i < nthreads; i++) {
34.        create_worker(worker_libevent, &threads[i]); //启动worker线程，见worker_libevent
35.    }
36. 
37.    pthread_mutex_lock(&init_lock);
38.    wait_for_thread_registration(nthreads); //等待所有worker线程启动完毕
39.    pthread_mutex_unlock(&init_lock);
40.}


主线程和每个worker线程我们都用一个结构体来表示，上面的代码中:
threads = calloc(nthreads, sizeof(LIBEVENT_THREAD)); 这一行是对worker线程结构体实例对象的创建。

dispatcher_thread.base = main_base;
 dispatcher_thread.thread_id = pthread_self(); 而这两行则是对主线程对象的初始化，dispatcher_thread是个全局变量。

我们看看worker线程的结构体和主线程的结构体定义：
1. typedef struct {
2.    pthread_t thread_id;         //线程id
3.    struct event_base *base;     //每个线程自己独立的event_base，监听的就是下面的notify_event事件对象
4.    struct event notify_event;  //事件对象，fd即为下面的notify_receive_fd
5.    int notify_receive_fd;      //管道接收fd
6.    int notify_send_fd;         //管道写入fd
7.    struct thread_stats stats;  //线程的一些统计
8.    struct conn_queue *new_conn_queue; //连接参数对象CQ_ITEM队列
9.    cache_t *suffix_cache;      
10.    uint8_t item_lock_type;     //控制线程锁的粒度
11.} LIBEVENT_THREAD;
12. 
13.typedef struct {
14.    pthread_t thread_id;        //线程id
15.    struct event_base *base;    //event_base
16.} LIBEVENT_DISPATCHER_THREAD;


看完结构体定义后，我们回到thread_init中，里面有一个for循环，循环里面就是对每个worker线程进行初始化，具体包括：

a）调用pipe函数为每个线程产生两个fd，即管道接收fd和管道写入fd。用于与主线程之间的通信。（先跳过，后面详讲）

b）调用setup_thread函数装载线程，这个函数里面也是对worker线程初始化，包括监听管道接收fd。（先跳过，后面详讲）

另外，在后面调用了 create_worker(worker_libevent, &threads[i]); 启动线程，线程就开始运行了，而worker_libevent函数是线程启动的执行入口。

我们先看看调用create_worker函数后，做了啥:
1.static void create_worker(void *(*func)(void *), void *arg) {
2.    pthread_t thread;
3.    pthread_attr_t attr;
4.    int ret;
5. 
6.    pthread_attr_init(&attr);
7. 
8.    if ((ret = pthread_create(&thread, &attr, func, arg)) != 0) {
9.        fprintf(stderr, "Can't create thread: %s\n",
10.        strerror(ret));
11.        exit(1);
12.    }
13.}
14. 
15./*
16.* 这里主要是让worker线程进入event_base_loop
17.*/
18.static void *worker_libevent(void *arg) {
19.    LIBEVENT_THREAD *me = arg;
20.    me->item_lock_type = ITEM_LOCK_GRANULAR;
21.    pthread_setspecific(item_lock_type_key, &me->item_lock_type);
22. 
23.    //每一个worker线程进入loop，全局init_count++操作，
24.    //见thread_init函数后面几行代码和wait_for_thread_registration函数，
25.    //主线程通过init_count来确认所有线程都启动完毕。
26.    register_thread_initialized();
27. 
28.    //进入事件循环
29. 
30.    event_base_loop(me->base, 0);
31.    return NULL;
32.}


create_worker通过调用系统函数pthread_create启动线程，然后每个线程进入worker_libevent执行，从代码中可到，worker线程启动后，主要做的一事也仅仅是event_base_loop()，进行事件循环而已，你会奇怪，worker线程什么时候分配了自己的event_base？（me->base），其实就在上面thread_init中“先跳过”的那部分，setup_thread函数。

4）我们回到thread_init的地方中我们刚才“跳过”的地方，那里有个setup_thread函数，是对每个worker线程进行装载，这个装载非常重要：
1. /*
2. * 装载worker线程，worker线程的event_base在此设置
3. */
4.static void setup_thread(LIBEVENT_THREAD *me) {
5.    me->base = event_init(); //为每个worker线程分配自己的event_base
6.    if (! me->base) {
7.        fprintf(stderr, "Can't allocate event base\n");
8.        exit(1);
9.    }
10.    event_set(&me->notify_event, me->notify_receive_fd,
11.              EV_READ | EV_PERSIST, thread_libevent_process, me);     //监听管道接收fd，这里即监听
12.    //来自主线程的消息，事件处理函数为thread_libevent_process
13.    event_base_set(me->base, &me->notify_event);
14. 
15.    if (event_add(&me->notify_event, 0) == -1) {
16.        fprintf(stderr, "Can't monitor libevent notify pipe\n");
17.        exit(1);
18.    }
19. 
20.    me->new_conn_queue = malloc(sizeof(struct conn_queue));        //CQ_ITEM队列
21.    if (me->new_conn_queue == NULL) {
22.        perror("Failed to allocate memory for connection queue");
23.        exit(EXIT_FAILURE);
24.    }
25. 
26. 
27.    cq_init(me->new_conn_queue);  //初始化CQ_ITEM对象队列
28. 
29.    if (pthread_mutex_init(&me->stats.mutex, NULL) != 0) {
30.        perror("Failed to initialize mutex");
31.        exit(EXIT_FAILURE);
32.    }
33. 
34.    me->suffix_cache = cache_create("suffix", SUFFIX_SIZE, sizeof(char*),
35.                                    NULL, NULL);
36.    if (me->suffix_cache == NULL) {
37.        fprintf(stderr, "Failed to create suffix cache\n");
38.        exit(EXIT_FAILURE);
39.    }
40.}


代码中可以看到，worker线程的event_base就在这里分配的了，分配完后，马上创建事件event，同时监听自己管道接收fd的可读事件，事件处理函数为thread_libevent_process。

setup_thread完之后，就是回到thread_init函数，然后线程启动，进入event_base_loop了。

5）直至到此，我们已经了解到了：

a）主线程是如何监听listen fd的。

b）worker线程是如何被创建并分配自己的event_base同时监听自己的管道接收fd的。

但我们还没了解到：

a）当主线程监听到listen fd有连接上来后，具体做了什么？即主线程的监听listen fd的事件处理event_handler做了什么？

b）worker线程监听的管道接收fd是怎么发生可读事件的？发生之后具体做了什么？即worker线程的监听管道接收fd的事件处理thread_libevent_process做了什么？

6）下面我们要把主线程事件处理和worker线程事件处理结合一起来看：

回顾一下主线程绑定event_handler函数作为事件处理的过程：

server_socket->conn_new(sfd, conn_listening,EV_READ | EV_PERSIST, 1,transport, main_base); （请注意这里第二个参数值是conn_listening！）->event_set(&c->event, sfd, event_flags, event_handler, (void *)c);

我们再来看下event_handler函数的代码：
1. void event_handler(const int fd, const short which, void *arg) {
2.    conn *c;
3.    c = (conn *)arg;
4.    c->which = which;
5.    //。。。
6.    drive_machine(c); //调用drive_machine处理事件发生后的业务逻辑。
7.    return;
8.}
9. 
10.static void drive_machine(conn *c) {
11.    bool stop = false;
12.    int sfd;
13.    socklen_t addrlen;
14.    struct sockaddr_storage addr;
15.    int nreqs = settings.reqs_per_event; //每个连接可处理的最大请求数
16.    int res;
17.    const char *str;
18.    while (!stop) {
19.        switch(c->state) {
20.        case conn_listening: //此case只有当listen fd有事件到达后触发主线程执行
21.            addrlen = sizeof(addr);
22.            sfd = accept(c->sfd, (struct sockaddr *)&addr, &addrlen); //accept，得到client fd
23. 
24.            if (settings.maxconns_fast &&
25.                stats.curr_conns + stats.reserved_fds >= settings.maxconns - 1) {
26.                //。。。
27.            } else {
28.                /**
29.                accept成功后，调用dispatch_conn_new，把client fd交给 worker线程处理
30.                必须注意dispatch_conn_new 函数第二个参数：init_state，也就是
31.                创建连接对象的初始化状态，通过主线程分发给worker线程的client fd，最终
32.                建立的连接对象初始化状态为conn_new_cmd （当然这里只说的是TCP socket的情况，UDP socket暂不作分析）
33.                */
34.                dispatch_conn_new(sfd, conn_new_cmd, EV_READ | EV_PERSIST,
35.                                     DATA_BUFFER_SIZE, tcp_transport);
36.            }
37.            stop = true;
38.            break;
39.            //。。。省略其它连接状态case
40.    }
41.}


上面代码看到，当主线程有连接到达，触发调用event_handler函数，而event_handler函数又调用drive_machine，先不去理解这个drive_machine的命名，我们以程序的角度去往下走，主线程会进入switch里面，由于在上面conn_new传进来的conn_state值为conn_listening，所以进入conn_listening这个case分支，在这个分支，主线程accept刚请求过来的连接，产生一个client fd，然后调用 dispatch_conn_new函数，而这个函数正是把client fd分发给某个worker线程。

以下是把连接分发给worker线程的代码，即dispatch_conn_new：
1. void dispatch_conn_new(int sfd, enum conn_states init_state, int event_flags,
2.                       int read_buffer_size, enum network_transport transport) {
3.    /**
4.    这下面有一个CQ_ITEM结构体，可以这么理解，主线程accept连接后，把client fd
5.    分发到worker线程的同时会顺带一些与此client连接相关的信息，例如dispatch_conn_new的形参上面列的，
6.    而CQ_ITEM是包装了这些信息的一个对象。
7.    CQ_ITEM中的CQ是connection queue的缩写，但它与conn结构体是完全不一样的概念，CQ_ITEM仅仅是把client连接相关的信息
8.    打包成一个对象而已。
9.    */
10.    CQ_ITEM *item = cqi_new();
11.    char buf[1];
12.    if (item == NULL) {
13.       //。。。
14.    }
15.    int tid = (last_thread + 1) % settings.num_threads;
16.    LIBEVENT_THREAD *thread = threads + tid; //通过简单的轮叫方式选择处理当前client fd的worker线程
17.    last_thread = tid;
18.    //初始化CQ_ITEM对象，即把信息包装
19.    item->sfd = sfd;
20.    item->init_state = init_state;
21.    item->event_flags = event_flags;
22.    item->read_buffer_size = read_buffer_size;
23.    item->transport = transport;
24.    cq_push(thread->new_conn_queue, item); //每个worker线程保存着所有被分发给自己的CQ_ITEM，即new_conn_queue
25.    MEMCACHED_CONN_DISPATCH(sfd, thread->thread_id);
26.    /*
27.    主线程向处理当前client fd的worker线程管道中简单写进一个'c'字符，
28.    由于每个worker线程都监听了管道的receive_fd，于是相应的worker进程收到事件通知，
29.    触发注册的handler，即thread_libevent_process
30.    */
31.    buf[0] = 'c';
32.    if (write(thread->notify_send_fd, buf, 1) != 1) {
33.        perror("Writing to thread notify pipe");
34.    }
35.}


注释说明了，dispatch_conn_new函数中主线程通过轮叫方式简单地把连接相关的参数压到worker线程的CQ_ITEM队列，分发给worker线程，然后通过管道通知worker线程，此时worker线程就监听到有事件来了，然后调用thread_libevent_process。

以下是worker线程调用thread_libevent_process进行事件处理：
1. //主线程分发client fd给worker线程后，同时往管道写入buf，唤醒worker线程调用此函数
2.static void thread_libevent_process(int fd, short which, void *arg) {
3.    LIBEVENT_THREAD *me = arg;
4.    CQ_ITEM *item;
5.    char buf[1];
6.    if (read(fd, buf, 1) != 1)
7.        if (settings.verbose > 0)
8.            fprintf(stderr, "Can't read from libevent pipe\n");
9.    switch (buf[0]) {
10.    case 'c':
11.    item = cq_pop(me->new_conn_queue); //取出主线程丢过来的CQ_ITEM
12.    if (NULL != item) {
13.        /*
14.        worker线程创建 conn连接对象，注意由主线程丢过来的CQ_ITEM的init_state为conn_new_cmd （TCP情况下）
15.        */
16.        conn *c = conn_new(item->sfd, item->init_state, item->event_flags,
17.                           item->read_buffer_size, item->transport, me->base);
18.        if (c == NULL) {
19.            //。。。
20.        } else {
21.            c->thread = me; //设置监听连接的线程为当前worker线程
22.        }
23.        cqi_free(item);
24.    }
25.        break;
26.    }
27.    //。。。
28.}


worker线程管道可读事件发生后，从自己的CQ_ITEM队列“收信”，拿到主线程分发过来的信息（其中包括client fd），然后你会发现，worker线程在这个地方也调用了conn_new函数！ 只是此是传给conn_new的参数中，fd不是listen fd而是client fd，init_state不是conn_listening，而是conn_new_cmd，event_base不是主线程的event_base，而是当前worker线程的event_base！

而回顾conn_new的作用可知，conn_new函数里面把传进来的fd（这里是client fd）加入传进来的event_base（这里是worker线程的event_base），于是worker线程也调用了conn_new方法，监听了client fd，并且事件处理方法也是event_handler，也就是drive_machine函数。

所以无论是主线程监听listen fd 还是各个worker线程监听client fd，当各自的fd有可读事件发生时，最终调用同一个函数drive_machine进行事件处理！！只是listen fd的conn_state初始时为conn_listening （其实永远都是），而client fd初始为conn_new_cmd
