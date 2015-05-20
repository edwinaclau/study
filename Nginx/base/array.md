ngx_array_create



ngx_array_init



ngx_array_destroy




ngx_array_push



ngx_array_push_n




typedef  unsigned __int64 ngx_uint_t;
typedef struct ngx_array_s  ngx_array_t;
 
...c 
struct ngx_array_s 
{
    void*       elts;//数据
    ngx_uint_t  nelts;//已经使用个数
    size_t      size;//每个数据的大小
    ngx_uint_t  nalloc;//已经分配的区域
    ngx_pool_t* pool; //内存池
 
};
...

ngx_array_t

ngx_array_t

ngx_array_t *ngx_array_create(ngx_pool_t *p,
ngx_uint_t n, size_t size);

static ngx_inline ngx_int_t
ngx_array_init(ngx_array_t *array, ngx_pool_t *pool, ngx_uint_t n, size_t size)
{
    /*
     * set "array->nelts" before "array->elts", otherwise MSVC thinks
     * that "array->nelts" may be used without having been initialized
     */

    array->nelts = 0;
    array->size = size;
    array->nalloc = n;
    array->pool = pool;

    array->elts = ngx_palloc(pool, n * size);
    if (array->elts == NULL) {
        return NGX_ERROR;
    }

    return NGX_OK;
}