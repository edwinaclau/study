模块配置指令
一个模块的配置指令是定义在一个静态数组中的。同样地，我们来看一下从hello module中截取的模块配置指令的定义。

static ngx_command_t ngx_http_hello_commands[] = {
   {
        ngx_string("hello_string"),
        NGX_HTTP_LOC_CONF|NGX_CONF_NOARGS|NGX_CONF_TAKE1,
        ngx_http_hello_string,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_hello_loc_conf_t, hello_string),
        NULL },

    {
        ngx_string("hello_counter"),
        NGX_HTTP_LOC_CONF|NGX_CONF_FLAG,
        ngx_http_hello_counter,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_hello_loc_conf_t, hello_counter),
        NULL },

    ngx_null_command
};
其实看这个定义，就基本能看出来一些信息。例如，我们是定义了两个配置指令，一个是叫hello_string，可以接受一个参数，或者是没有参数。另外一个命令是hello_counter，接受一个NGX_CONF_FLAG类型的参数。除此之外，似乎看起来有点迷惑。没有关系，我们来详细看一下ngx_command_t，一旦我们了解这个结构的详细信息，那么我相信上述这个定义所表达的所有信息就不言自明了。

ngx_command_t的定义，位于src/core/ngx_conf_file.h中。

struct ngx_command_s {
    ngx_str_t             name;
    ngx_uint_t            type;
    char               *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
    ngx_uint_t            conf;
    ngx_uint_t            offset;
    void                 *post;
};
name:	配置指令的名称。
type:	该配置的类型，其实更准确一点说，是该配置指令属性的集合。nginx提供了很多预定义的属性值（一些宏定义），通过逻辑或运算符可组合在一起，形成对这个配置指令的详细的说明。下面列出可在这里使用的预定义属性值及说明。
NGX_CONF_NOARGS：配置指令不接受任何参数。

NGX_CONF_TAKE1：配置指令接受1个参数。

NGX_CONF_TAKE2：配置指令接受2个参数。

NGX_CONF_TAKE3：配置指令接受3个参数。

NGX_CONF_TAKE4：配置指令接受4个参数。

NGX_CONF_TAKE5：配置指令接受5个参数。

NGX_CONF_TAKE6：配置指令接受6个参数。

NGX_CONF_TAKE7：配置指令接受7个参数。

可以组合多个属性，比如一个指令即可以不填参数，也可以接受1个或者2个参数。那么就是NGX_CONF_NOARGS|NGX_CONF_TAKE1|NGX_CONF_TAKE2。如果写上面三个属性在一起，你觉得麻烦，那么没有关系，nginx提供了一些定义，使用起来更简洁。

NGX_CONF_TAKE12：配置指令接受1个或者2个参数。

NGX_CONF_TAKE13：配置指令接受1个或者3个参数。

NGX_CONF_TAKE23：配置指令接受2个或者3个参数。

NGX_CONF_TAKE123：配置指令接受1个或者2个或者3参数。

NGX_CONF_TAKE1234：配置指令接受1个或者2个或者3个或者4个参数。

NGX_CONF_1MORE：配置指令接受至少一个参数。

NGX_CONF_2MORE：配置指令接受至少两个参数。

NGX_CONF_MULTI: 配置指令可以接受多个参数，即个数不定。

NGX_CONF_BLOCK：配置指令可以接受的值是一个配置信息块。也就是一对大括号括起来的内容。里面可以再包括很多的配置指令。比如常见的server指令就是这个属性的。

NGX_CONF_FLAG：配置指令可以接受的值是”on”或者”off”，最终会被转成bool值。

NGX_CONF_ANY：配置指令可以接受的任意的参数值。一个或者多个，或者”on”或者”off”，或者是配置块。

最后要说明的是，无论如何，nginx的配置指令的参数个数不可以超过NGX_CONF_MAX_ARGS个。目前这个值被定义为8，也就是不能超过8个参数值。

下面介绍一组说明配置指令可以出现的位置的属性。

NGX_DIRECT_CONF：可以出现在配置文件中最外层。例如已经提供的配置指令daemon，master_process等。

NGX_MAIN_CONF: http、mail、events、error_log等。

NGX_ANY_CONF: 该配置指令可以出现在任意配置级别上。

对于我们编写的大多数模块而言，都是在处理http相关的事情，也就是所谓的都是NGX_HTTP_MODULE，对于这样类型的模块，其配置可能出现的位置也是分为直接出现在http里面，以及其他位置。

NGX_HTTP_MAIN_CONF: 可以直接出现在http配置指令里。

NGX_HTTP_SRV_CONF: 可以出现在http里面的server配置指令里。

NGX_HTTP_LOC_CONF: 可以出现在http server块里面的location配置指令里。

NGX_HTTP_UPS_CONF: 可以出现在http里面的upstream配置指令里。

NGX_HTTP_SIF_CONF: 可以出现在http里面的server配置指令里的if语句所在的block中。

NGX_HTTP_LMT_CONF: 可以出现在http里面的limit_except指令的block中。

NGX_HTTP_LIF_CONF: 可以出现在http server块里面的location配置指令里的if语句所在的block中。

set:	这是一个函数指针，当nginx在解析配置的时候，如果遇到这个配置指令，将会把读取到的值传递给这个函数进行分解处理。因为具体每个配置指令的值如何处理，只有定义这个配置指令的人是最清楚的。来看一下这个函数指针要求的函数原型。
char *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
先看该函数的返回值，处理成功时，返回NGX_OK，否则返回NGX_CONF_ERROR或者是一个自定义的错误信息的字符串。

再看一下这个函数被调用的时候，传入的三个参数。

cf: 该参数里面保存从配置文件读取到的原始字符串以及相关的一些信息。特别注意的是这个参数的args字段是一个ngx_str_t类型的数组，该数组的首个元素是这个配置指令本身，第二个元素是指令的第一个参数，第三个元素是第二个参数，依次类推。
cmd: 这个配置指令对应的ngx_command_t结构。
conf: 就是定义的存储这个配置值的结构体，比如在上面展示的那个ngx_http_hello_loc_conf_t。当解析这个hello_string变量的时候，传入的conf就指向一个ngx_http_hello_loc_conf_t类型的变量。用户在处理的时候可以使用类型转换，转换成自己知道的类型，再进行字段的赋值。
为了更加方便的实现对配置指令参数的读取，nginx已经默认提供了对一些标准类型的参数进行读取的函数，可以直接赋值给set字段使用。下面来看一下这些已经实现的set类型函数。

ngx_conf_set_flag_slot： 读取NGX_CONF_FLAG类型的参数。
ngx_conf_set_str_slot:读取字符串类型的参数。
ngx_conf_set_str_array_slot: 读取字符串数组类型的参数。
ngx_conf_set_keyval_slot： 读取键值对类型的参数。
ngx_conf_set_num_slot: 读取整数类型(有符号整数ngx_int_t)的参数。
ngx_conf_set_size_slot:读取size_t类型的参数，也就是无符号数。
ngx_conf_set_off_slot: 读取off_t类型的参数。
ngx_conf_set_msec_slot: 读取毫秒值类型的参数。
ngx_conf_set_sec_slot: 读取秒值类型的参数。
ngx_conf_set_bufs_slot： 读取的参数值是2个，一个是buf的个数，一个是buf的大小。例如： output_buffers 1 128k;
ngx_conf_set_enum_slot: 读取枚举类型的参数，将其转换成整数ngx_uint_t类型。
ngx_conf_set_bitmask_slot: 读取参数的值，并将这些参数的值以bit位的形式存储。例如：HttpDavModule模块的dav_methods指令。
conf:	该字段被NGX_HTTP_MODULE类型模块所用 (我们编写的基本上都是NGX_HTTP_MOUDLE，只有一些nginx核心模块是非NGX_HTTP_MODULE)，该字段指定当前配置项存储的内存位置。实际上是使用哪个内存池的问题。因为http模块对所有http模块所要保存的配置信息，划分了main, server和location三个地方进行存储，每个地方都有一个内存池用来分配存储这些信息的内存。这里可能的值为 NGX_HTTP_MAIN_CONF_OFFSET、NGX_HTTP_SRV_CONF_OFFSET或NGX_HTTP_LOC_CONF_OFFSET。当然也可以直接置为0，就是NGX_HTTP_MAIN_CONF_OFFSET。
offset:	指定该配置项值的精确存放位置，一般指定为某一个结构体变量的字段偏移。因为对于配置信息的存储，一般我们都是定义个结构体来存储的。那么比如我们定义了一个结构体A，该项配置的值需要存储到该结构体的b字段。那么在这里就可以填写为offsetof(A, b)。对于有些配置项，它的值不需要保存或者是需要保存到更为复杂的结构中时，这里可以设置为0。
post:	该字段存储一个指针。可以指向任何一个在读取配置过程中需要的数据，以便于进行配置读取的处理。大多数时候，都不需要，所以简单地设为0即可。
看到这里，应该就比较清楚了。ngx_http_hello_commands这个数组每5个元素为一组，用来描述一个配置项的所有情况。那么如果有多个配置项，只要按照需要再增加5个对应的元素对新的配置项进行说明。

需要注意的是，就是在ngx_http_hello_commands这个数组定义的最后，都要加一个ngx_null_command作为结尾。