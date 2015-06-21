struct evsignal_info {
	struct event ev_signal;   ///<所属的event
	int ev_signal_pair[2];    ///<创建的流管道
	int ev_signal_added;     ///<信号是否已被加入到event中的标记。
	volatile sig_atomic_t evsignal_caught; ///<事件触发标记,1表示有信号被触发
	struct event_list evsigevents[NSIG];   ///<多个事件有可能注册到同一个信号，因此这里每个信号的事件都是一个event_list.
	sig_atomic_t evsigcaught[NSIG];   ///<由于一个信号可能被注册多次，这里保存信号被捕捉的次数
#ifdef HAVE_SIGACTION
	struct sigaction **sh_old;
#else
	ev_sighandler_t **sh_old;
#endif
	int sh_old_max;
};


void
evsignal_init(struct event_base *base)
{
	int i;

	///创建一对流管道
	if (evutil_socketpair(
		    AF_UNIX, SOCK_STREAM, 0, base->sig.ev_signal_pair) == -1)
		event_err(1, "%s: socketpair", __func__);
        
        ///设置fd
	FD_CLOSEONEXEC(base->sig.ev_signal_pair[0]);
	FD_CLOSEONEXEC(base->sig.ev_signal_pair[1]);
        ///初始化sig数据结构
	base->sig.sh_old = NULL;
	base->sig.sh_old_max = 0;
	base->sig.evsignal_caught = 0;
	memset(&base->sig.evsigcaught, 0, sizeof(sig_atomic_t)*NSIG);
	/* initialize the queues for all events */
        ///在libevent里面，所有的事件队列都用tail queue实现，linux下它使用的是linux自带的taile queue，具体用法可以去看man手册。
	for (i = 0; i < NSIG; ++i)
		TAILQ_INIT(&base->sig.evsigevents[i]);

       ///设置非阻塞
        evutil_make_socket_nonblocking(base->sig.ev_signal_pair[0]);
        
        ///初始化event结构
	event_set(&base->sig.ev_signal, base->sig.ev_signal_pair[1],
		EV_READ | EV_PERSIST, evsignal_cb, &base->sig.ev_signal);
	base->sig.ev_signal.ev_base = base;
	base->sig.ev_signal.ev_flags |= EVLIST_INTERNAL;
}
