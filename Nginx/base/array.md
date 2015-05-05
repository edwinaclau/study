ngx_array_create



ngx_array_init



ngx_array_destroy




ngx_array_push



ngx_array_push_n




typedef  unsigned __int64 ngx_uint_t;
typedef struct ngx_array_s  ngx_array_t;
 
 
struct ngx_array_s 
{
    void*       elts;//数据
    ngx_uint_t  nelts;//已经使用个数
    size_t      size;//每个数据的大小
    ngx_uint_t  nalloc;//已经分配的区域
    ngx_pool_t* pool; //内存池
 
};

