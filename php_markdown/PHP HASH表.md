在PHP中,所有的数据 无论变量,常量,类,属性 都用Hash表来实现.

    typedef struct bucket {
    ulong h;/* Used for numeric indexing */
    uint nKeyLength; //key长度
    void *pData; //指向 Bucke保存的数据 指针
    void *pDataPtr; //指针数据
    struct bucket *pListNext; //下一个元素指针
    struct bucket *pListLast;//上一个元素指针
    struct bucket *pNext;
    struct bucket *pLast;
    char arKey[1]; /* Must be last element */
    } Bucket;
    typedef struct _hashtable {
    uint nTableSize;//HashTable的大小
    uint nTableMask;//等于nTableSize-1
    uint nNumOfElements;//对象个数
    ulong nNextFreeElement;//指向下一个空元素位置 nTableSize+1
    Bucket *pInternalPointer;   /* Used for element traversal *///保存当前遍历的指针
    Bucket *pListHead;//头元素指针
    Bucket *pListTail;//尾元素指针
    Bucket **arBuckets;//存储hash数组数据
    dtor_func_t pDestructor;//类似于析构函数
    zend_bool persistent;//用哪种方法分配内存空间 PHP统一管理内存还是用普通的malloc
    unsigned char nApplyCount;//当前hash bucket被访问的次数,是否遍历过数据,防止无限递归循环
    zend_bool bApplyProtection;
    #if ZEND_DEBUG
    int inconsistent;
    #endif
    } HashTable;


    ZEND_API int _zend_hash_init(HashTable *ht, uint nSize, hash_func_t pHashFunction, dtor_func_t pDestructor, zend_bool persistent ZEND_FILE_LINE_DC)
    {
     uint i = 3;
     Bucket **tmp;
     
    SET_INCONSISTENT(HT_OK);
     
     if (nSize &gt;= 0x80000000) { //HASH表大小大于0x8则初始化为0x8
       /* prevent overflow */
       ht-&gt;nTableSize = 0x80000000;
     } else {
       while ((1U &lt;&lt; i) &lt; nSize) { //调整为 2的n次方  i++;}ht-&gt;nTableSize = 1 &lt;&lt; i;//HASH bucket大小   为 2的i次方  i=3 ,nTableSize最小值为8
     }



//为了提高计算效率，系统自动会将nTableSize调整到最小一个不小于nTableSize的2的整数次方。也就是说，如果在初始化HashTable时指定一个nTableSize不是2的整数次方，系统将会自动调整nTableSize的值 &lt;!--EndFragment--&gt;
     
     nTableMask = ht-&gt;nTableSize - 1;
     ht-&gt;pDestructor = pDestructor;//一个函数指针,当HashTable发生增,删,改时调用
     ht-&gt;arBuckets = NULL;
     ht-&gt;pListHead = NULL;
     ht-&gt;pListTail = NULL;
     ht-&gt;nNumOfElements = 0;
     ht-&gt;nNextFreeElement = 0;
     ht-&gt;pInternalPointer = NULL;
     ht-&gt;persistent = persistent;//如果persisient为TRUE，则使用操作系统本身的内存分配函数为Bucket分配内存，否则使用PHP的内存分配函数
     ht-&gt;nApplyCount = 0;
     ht-&gt;bApplyProtection = 1;
     
     /* Uses ecalloc() so that Bucket* == NULL */
     if (persistent) {  //操作系统本身内存分配方式分配内存,calloc分配内存后自动初始化为0
     tmp = (Bucket **) calloc(ht-&gt;nTableSize, sizeof(Bucket *));
     if (!tmp) {
     return FAILURE;
     }
     ht-&gt;arBuckets = tmp;
     } else {//用PHP的内存管理机制分配内存
     tmp = (Bucket **) ecalloc_rel(ht-&gt;nTableSize, sizeof(Bucket *));
     if (tmp) {
     ht-&gt;arBuckets = tmp;
     }
     }
    //自动申请一块内存给arBuckets,该内存大小等于 nTableSize
    return SUCCESS;
    }


在读源码的时候 ,经常会看到 EG,PG,CG这样的宏

CG是 compile_global的简写

EG是excutor_global的简写

G就是全局变量的意思

我们就以EG宏为例:

    #ifdef ZTS
    # define EG(v) TSRMG(executor_globals_id, zend_executor_globals *, v)
    #else
    # define EG(v) (executor_globals.v)
    extern ZEND_API zend_executor_globals executor_globals;
    #endif

很简单 只是一个获取全局变量的宏

那么我们看看 zend_executor_globals这个结构体

在/Zend/zend.h里面定义

typedef struct _zend_executor_globals zend_executor_globals;

是一个 _zend_executor_globals的别名

同一个文件里找到它

PHP的所有 局部变量,全局变量,函数,类的 Hash表 都在这里定义了


    struct _zend_executor_globals {
    zval **return_value_ptr_ptr;
     
    zval uninitialized_zval;
    zval *uninitialized_zval_ptr;
     
    zval error_zval;
    zval *error_zval_ptr;
     
    zend_ptr_stack arg_types_stack;
     
    /* symbol table cache */
    HashTable *symtable_cache[SYMTABLE_CACHE_SIZE];
    HashTable **symtable_cache_limit;
    HashTable **symtable_cache_ptr;
     
    zend_op **opline_ptr;
     
    HashTable *active_symbol_table;  //局部变量
    HashTable symbol_table; /* main symbol table */ //全局变量
 
    HashTable included_files; /* files already included */ //include的文件
     
    JMP_BUF *bailout;
     
    int error_reporting;
    int orig_error_reporting;
    int exit_status;
     
    zend_op_array *active_op_array;
     
    HashTable *function_table; /* function symbol table */ //函数表
    HashTable *class_table; /* class table */ //类表
    HashTable *zend_constants; /* constants table */ //常量表
     
    zend_class_entry *scope;
    zend_class_entry *called_scope; /* Scope of the calling class */
     
    zval *This;
     
    long precision;
     
    int ticks_count;
     
    zend_bool in_execution;
    HashTable *in_autoload;
    zend_function *autoload_func;
    zend_bool full_tables_cleanup;
     
    /* for extended information support */
    zend_bool no_extensions;
     
    #ifdef ZEND_WIN32
    zend_bool timed_out;
    OSVERSIONINFOEX windows_version_info;
    #endif
     
    HashTable regular_list;
    HashTable persistent_list;
     
    zend_vm_stack argument_stack;
     
    int user_error_handler_error_reporting;
    zval *user_error_handler;
    zval *user_exception_handler;
    zend_stack user_error_handlers_error_reporting;
    zend_ptr_stack user_error_handlers;
    zend_ptr_stack user_exception_handlers;
     
    zend_error_handling_t error_handling;
    zend_class_entry *exception_class;
     
    /* timeout support */
    int timeout_seconds;
     
    int lambda_count;
     
    HashTable *ini_directives;
    HashTable *modified_ini_directives;
     
    zend_objects_store objects_store;
    zval *exception, *prev_exception;
    zend_op *opline_before_exception;
    zend_op exception_op[3];
     
    struct _zend_execute_data *current_execute_data;
     
    struct _zend_module_entry *current_module;
     
    zend_property_info std_property_info;
     
    zend_bool active;
     
    void *saved_fpu_cw;
     
    void *reserved[ZEND_MAX_RESERVED_RESOURCES];
    };



这里先简单看看,以后用到的时候再细说,

PHP里最基本的单元 变量:
在PHP里 定义一个变量 再简单不过了
如

&lt;?php
$a=1;
?&gt;
但是在内核中 它是用一个 zval结构体实现的
如上面定义变量 在内核中则执行了下面这些代码


zval *val;
MAKE_STD_ZVAL(val);  //申请一块内存
ZVAL_STRING(val,&quot;hello&quot;,1);//用ZVAL_STRING设置它的值为 &quot;hello&quot;
ZEND_SET_SYMBOL(EG(active_symbol_table),&quot;a&quot;,val));//将  val指针加入到符号表里面去
宏 MAKE_STD_ZVAL 定义如下

1
2
3
#define MAKE_STD_ZVAL(zv)                                \
ALLOC_ZVAL(zv); \  //它归根到底等于 (p) = (type *) emalloc(sizeof(type))
INIT_PZVAL(zv);
INIT_PZVAL定义在


    #define INIT_PZVAL(z)   \ 看得出它是初始化参数
    ;refcount__gc = 1;  \
    is_ref__gc = 0;
    那么 zval到底是什么呢
    在zend/zend.h里面
    typedef struct _zval_struct zval; //原来它是 _zval_struct 的别名
    _zval_struct 定义如下

    
    typedef union _zvalue_value {
    long lval;  //保存long类型的数据
    double dval; //保存 double类型的数据
    struct {
    char *val; //真正的值在这里
    int len;   //这里返回长度
    } str;
    HashTable *ht;
    zend_object_value obj; //这是一个对象
    } zvalue_value;
 
    struct _zval_struct {
    zvalue_value value; //保存的值
    zend_uint refcount__gc;//被引用的次数 如果为1 则只被自己使用如果大于1 则被其他变量以&amp;的形式引用.
    zend_uchar type;   //数据类型 这也是 为什么 PHP是弱类型的原因
    zend_uchar is_ref__gc;  //表示是否为引用
    };
    如果还是不够清楚..那么我们实战一下..用C来创建一个PHP变量
    这里需要一个扩展,PHP如果用C扩展模块 这里就不说了
    关键代码
    
    
    PHP_FUNCTION(test_siren){
    zval *value;
    char *s=&quot;create a php variable&quot;;
    value=(zval*)malloc(sizeof(zval));
    memset(value,0,sizeof(value));
    value-&gt;is_ref__gc=0; //非引用变量
    value-&gt;refcount__gc=1;//引用次数 只有自己
    value-&gt;type=IS_STRING;//类型为字符串
    value-&gt;value.str.val=s;//值
    value-&gt;value.str.len=strlen(s);//长度
    ZEND_SET_SYMBOL(EG(active_symbol_table),&quot;a&quot;,value);
    }


第三行和第四行的作用 与MAKE_STD_ZVAL的作用相同,给value分配内存空间
第5-9行 的作用与ZVAL_STRING的作用相同,
最后一行 是将value创建一个 在PHP里叫$a的变量..并添加到局部Hash表里..
这样 在PHP里


<? php
test_siren(1);
echo $a;
?>;