Redis5中类型


STRING ---> RAW

       ---> INT


LIST ---> LINKEDlIST
     ---> ZIPLIST


HASH ---> HT

SET       INTSET

          SKIPLIST


sds 两种编码 

adlist 是双向链表



robj *createObject(int type, void *ptr) {
    robj *o = zmalloc(sizeof(*o));
    o->type = type;
    o->encoding = REDIS_ENCODING_RAW;
    o->ptr = ptr;
    o->refcount = 1;

    /* Set the LRU to the current lruclock (minutes resolution). */
    o->lru = server.lruclock;
    return o;
}


robj *createStringObject(char *ptr, size_t len) {
    return createObject(REDIS_STRING,sdsnewlen(ptr,len));
}


robj *createStringObjectFromLongLong(long long value) {
    robj *o;
    if (value >= 0 && value < REDIS_SHARED_INTEGERS) {
        incrRefCount(shared.integers[value]);
        o = shared.integers[value];
    } else {
        if (value >= LONG_MIN && value <= LONG_MAX) {
            o = createObject(REDIS_STRING, NULL);
            o->encoding = REDIS_ENCODING_INT;
            o->ptr = (void*)((long)value);
        } else {
            o = createObject(REDIS_STRING,sdsfromlonglong(value));
        }
    }
    return o;
}

字符串	REDIS_ENCODING_INT	REDIS_ENCODING_EMBSTR	REDIS_ENCODING_RAW
列表	REDIS_ENCODING_ZIPLIST	REDIS_ENCODING_LINKEDLIST	
哈希	REDIS_ENCODING_ZIPLIST	REDIS_ENCODING_HT	
集合	REDIS_ENCODING_INTSET	REDIS_ENCODING_HT	
有序集合	REDIS_ENCODING_ZIPLIST	REDIS_ENCODING_SKIPLIST	

typedef struct redisObject {  
    // 类型  
    unsigned type:4;  
    // 编码  
    unsigned encoding:4;  
    // 对象最后一次被访问的时间  
    unsigned lru:REDIS_LRU_BITS; /* lru time (relative to server.lruclock) */  
    // 引用计数  
    int refcount;  
    // 指向实际值的指针  
    void *ptr;  
} robj;  