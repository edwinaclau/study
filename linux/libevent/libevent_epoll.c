

struct evepoll {
     struct event *evread;
	 struct event *evwrite;
};

struct epollop {
     struct evepoll *fds;
	 int nfds;
	 struct epoll_event *events;
	 int nevents;
	 int epfd;
};

static void *epoll_init	(struct event_base *);
static int epoll_add	(void *, struct event *);
static int epoll_del	(void *, struct event *);
static int epoll_dispatch	(struct event_base *, void *, struct timeval *);
static void epoll_dealloc	(struct event_base *, void *);


const struct eventop.epollops = {
      "epoll",
	  epoll_init,
	  epoll_add,
	  epoll_del,
	  epoll_dispatch,
	  epoll_dealloc,
	  1
};


static void *
epoll_init(struct event_base *base)



static int
epoll_recalc(struct event_base *base, void *arg, int max)


static int
epoll_dispatch(struct event_base *base, void *arg, struct timeval *tv)


static int
epoll_add(void *arg, struct event *ev)


static int
epoll_del(void *arg, struct event *ev)



static void
epoll_dealloc(struct event_base *base, void *arg)



