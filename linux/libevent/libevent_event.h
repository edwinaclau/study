其实就是定义事件 16进制


#define EVLIST_TIMEOUT	0x01
#define EVLIST_INSERTED	0x02
#define EVLIST_SIGNAL	0x04
#define EVLIST_ACTIVE	0x08
#define EVLIST_INTERNAL	0x10
#define EVLIST_INIT	0x80

/* EVLIST_X_ Private space: 0x1000-0xf000 */
#define EVLIST_ALL	(0xf000 | 0x9f)

#define EV_TIMEOUT	0x01
#define EV_READ		0x02
#define EV_WRITE	0x04
#define EV_SIGNAL	0x08
#define EV_PERSIST	0x10	/* Persistant event */

struct event_base *event_base_new(void);


struct event_base *event_init(void);


int event_reinit(struct event_base *base);


int event_dispatch(void);



int event_base_dispatch(struct event_base *);



const char *event_base_get_method(struct event_base *);




void event_base_free(struct event_base *);



#define _EVENT_LOG_DEBUG 0
#define _EVENT_LOG_MSG   1
#define _EVENT_LOG_WARN  2
#define _EVENT_LOG_ERR   3


typedef void (*event_log_cb)(int severity, const char *msg);

void event_set_log_callback(event_log_cb cb);


int event_base_set(struct event_base *, struct event *);


int event_loop(int);


int event_base_loop(struct event_base *, int);


int event_loopexit(const struct timeval *);


int event_base_loopexit(struct event_base *, const struct timeval *);



int event_loopbreak(void);



int event_base_loopbreak(struct event_base *);

int	event_base_priority_init(struct event_base *, int);

int	event_priority_set(struct event *, int);

#define evtimer_add(ev, tv)		event_add(ev, tv)


struct evbuffer {
	u_char *buffer;
	u_char *orig_buffer;

	size_t misalign;
	size_t totallen;
	size_t off;

	void (*cb)(struct evbuffer *, size_t, size_t, void *);
	void *cbarg;
};

/* Just for error reporting - use other constants otherwise */
#define EVBUFFER_READ		0x01
#define EVBUFFER_WRITE		0x02
#define EVBUFFER_EOF		0x10
#define EVBUFFER_ERROR		0x20
#define EVBUFFER_TIMEOUT	0x40
struct bufferevent;
typedef void (*evbuffercb)(struct bufferevent *, void *);
typedef void (*everrorcb)(struct bufferevent *, short what, void *);

struct event_watermark {
	size_t low;
	size_t high;
};

#ifndef EVENT_NO_STRUCT
struct bufferevent {
	struct event_base *ev_base;

	struct event ev_read;
	struct event ev_write;

	struct evbuffer *input;
	struct evbuffer *output;

	struct event_watermark wm_read;
	struct event_watermark wm_write;

	evbuffercb readcb;
	evbuffercb writecb;
	everrorcb errorcb;
	void *cbarg;

	int timeout_read;	/* in seconds */
	int timeout_write;	/* in seconds */

	short enabled;	/* events that are currently enabled */
};
#endif



struct bufferevent *bufferevent_new(int fd,
    evbuffercb readcb, evbuffercb writecb, everrorcb errorcb, void *cbarg);




int bufferevent_base_set(struct event_base *base, struct bufferevent *bufev);




int bufferevent_priority_set(struct bufferevent *bufev, int pri);


void bufferevent_free(struct bufferevent *bufev);



void bufferevent_setcb(struct bufferevent *bufev,
    evbuffercb readcb, evbuffercb writecb, everrorcb errorcb, void *cbarg);




void bufferevent_setfd(struct bufferevent *bufev, int fd);



int bufferevent_write(struct bufferevent *bufev,
    const void *data, size_t size);


int bufferevent_write_buffer(struct bufferevent *bufev, struct evbuffer *buf);




size_t bufferevent_read(struct bufferevent *bufev, void *data, size_t size);



int bufferevent_enable(struct bufferevent *bufev, short event);


int bufferevent_disable(struct bufferevent *bufev, short event);


void bufferevent_settimeout(struct bufferevent *bufev,
    int timeout_read, int timeout_write);


void bufferevent_setwatermark(struct bufferevent *bufev, short events,
    size_t lowmark, size_t highmark);

#define EVBUFFER_LENGTH(x)	(x)->off
#define EVBUFFER_DATA(x)	(x)->buffer
#define EVBUFFER_INPUT(x)	(x)->input
#define EVBUFFER_OUTPUT(x)	(x)->output



struct evbuffer *evbuffer_new(void);


del 那些我就不写，都差不多
