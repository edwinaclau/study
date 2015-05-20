hash不介绍，会编程的都懂


  小明 年龄 => 18
  小方 年龄 => 17



...c
typedef struct node_s{
     char    *key;
     char    *val;
     node_t  *next;
}node_t;

#define HASHSIZE 101
node_t* hashtable[HASHSIZE];
...



如果冲突就是链表方式解决


这个可以自行到baidu查找


typedef struct {
    void             *value;
    u_short           len;
    u_char            name[1];
} ngx_hash_elt_t;



typedef struct {
    ngx_hash_elt_t  **buckets; //有N个buckets
    ngx_uint_t        size;
} ngx_hash_t;


buckets
// ngx_pool_t申请空间，存放管理结构体ngx_hash_t ,4个

ngx_hash_t  *hash;
 ngx_hash_elt_t指针
hash = ngx_pcalloc(pool, sizeof(ngx_hash_t) + 4*sizeof(ngx_hash_elt_t *));

u_char *elts;
// 向ngx_pool_t申请hash表本身使用的连续内存块
elts = ngx_palloc(pool, 4 * 2 * sizeof(ngx_hash_elt_t));

ngx_hash_elt_t **buckets;
// 将管理结构体成员变量赋于正确的值。
for (i = 0; i < 4; i++) {
    buckets[i] = (ngx_hash_elt_t *) elts;  // 4个ngx_hash_elt_t指针指向正确地址；
    elts += 2 * sizeof(ngx_hash_elt_t);
}
hash->buckets = buckets;
hash->size = 4;