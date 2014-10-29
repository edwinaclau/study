
PHP之所以发现这么迅速,有很大原因是因为数组数据非常好处理,而且它可以存储其他类型的数据
数组的值存储在zvalue_value.ht字段中,ht是一个HashTable的数据
有关于HashTable的知识请移步 >> HASH表和变量
我们来详细说一下数组
PHP里面所有的数据都离不开zval和HashTable,
一个PHP很简单的数组初始化,
在C语言里面实现的却没有那么简单.
经过简单分析,找到数组的初始化的opcode
在Zend/zend_vm_execute.h文件中

```c
static int ZEND_FASTCALL  ZEND_INIT_ARRAY_SPEC_CV_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS)
{
        zend_op *opline = EX(opline);
 
        array_init(&EX_T(opline->result.u.var).tmp_var); //分配数组内存空间,初始化
        if (IS_CV == IS_UNUSED) {
                ZEND_VM_NEXT_OPCODE();
    #if 0 || IS_CV != IS_UNUSED
        } else {
                return ZEND_ADD_ARRAY_ELEMENT_SPEC_CV_CONST_HANDLER(ZEND_OPCODE_HANDLER_ARGS_PASSTHRU);
#endif        }
}

```
初始化数组的函数是 array_init
看看它的定义

```c
ZEND_API int _array_init(zval *arg, uint size ZEND_FILE_LINE_DC) /* {{{ */
{
 ALLOC_HASHTABLE_REL(Z_ARRVAL_P(arg)); 
 zend_hash_init(Z_ARRVAL_P(arg), size, NULL, ZVAL_PTR_DTOR, 0 ZEND_FILE_LINE_RELAY_CC);
        Z_TYPE_P(arg) = IS_ARRAY; //类型为数组
        return SUCCESS;
}
```
Hash表初始化函数_zend_hash_init


用扩展创建一个空数组,然后用PHP var_dump;

关键代码

```c
PHP_FUNCTION(confirm_siren_compiled)
{
        zval *value;
        MAKE_STD_ZVAL(value);
        array_init(value);
        ZEND_SET_SYMBOL(EG(active_symbol_table),"siren",value);
}
```
PHP执行代码


<!--?php dl("siren.so"); 
confirm_siren_compiled(1); var_dump($siren); ?-->
用命令执行 输出
s# /usr/local/php53/bin/php test.php
array(0) {
}
我们成功创建了一个空数组,如果看过 变量那一章的内容,应该会明白confirm_siren_compiled都做了什么
不懂的话 猛击>>PHP内核研究第二步:HASH表和变量

但是创建一个空数组 ,是没有意义的,如何添加键,值?
添加一个元素的关键代码
```c
PHP_FUNCTION(confirm_siren_compiled)
{
        zval *value;
        zval *element;
        char *s="this is a value";
        char *key="a";
        MAKE_STD_ZVAL(element);
        MAKE_STD_ZVAL(value);
        array_init(value);
        ZVAL_STRING(element,s,strlen(s));
        zend_hash_update(value->value.ht,key,strlen(key)+1,(void*)&element,sizeof(zval*),NULL);
        ZEND_SET_SYMBOL(EG(active_symbol_table),"siren",value);
}
```
执行PHP 结果如下
s# /usr/local/php53/bin/php test.php
array(1) {
["a"]=>
string(15) “this is a value”
}
zend_hash_update只是给数组添加元素的一种方法 ..
还有很多API可以用,


函数                                                                 说明

add_assoc_long(zval *array, char *key, long n);    添加一个长整型元素。

add_assoc_unset(zval *array, char *key);             添加一个 unset 元素。

add_assoc_bool(zval *array, char *key, int b);       添加一个布尔值。
add_assoc_resource(zval *array, char *key, int r); 添加一个资源。

add_assoc_double(zval *array, char *key, double d); 添加一个浮点值。

add_assoc_string(zval *array, char *key, char *str, int duplicate); 添加一个字符串。duplicate 用于表明这个字符串是否要被复制到 

Zend 的内部内存。

add_assoc_stringl(zval *array, char *key, char *str, uint length, int duplicate); 添加一个指定长度的字符串。其余跟add_assoc_string () 相同。
add_assoc_zval(zval *array, char *key, zval *value); 添加一个 zval 结构。 这在添加另外一个数组、对象或流等数据时会很有用
add_index_long(zval *array, uint idx, long n); 添加一个长整型元素。
add_index_unset(zval *array, uint idx); 添加一个 unset 元素。
add_index_bool(zval *array, uint idx, int b); 添加一个布尔值。
add_index_resource(zval *array, uint idx, int r); 添加一个资源。
add_index_double(zval *array, uint idx, double d); 添加一个浮点值。
add_index_string(zval *array, uint idx, char *str, int duplicate); 添加一个字符串。duplicate 用于表明这个字符串是否要被复制到 Zend 的内部内存。
add_index_stringl(zval *array, uint idx, char *str, uint length, int duplicate); 添加一个指定长度的字符串。其余跟add_index_string () 相同。
add_index_zval(zval *array, uint idx, zval *value); 添加一个 zval 结构。 这在添加另外一个数组、对象或流等数据时会很有用。
add_next_index_long(zval *array, long n); 添加一个长整型元素。
add_next_index_unset(zval *array); 添加一个 unset 元素。
add_next_index_bool(zval *array, int b); 添加一个布尔值。
add_next_index_resource(zval *array, int r); 添加一个资源。
add_next_index_double(zval *array, double d); 添加一个浮点值。
add_next_index_string(zval *array, char *str, int duplicate); 添加一个字符串。duplicate 用于表明这个字符串是否要被复制到 Zend 的内部内存。
add_next_index_stringl(zval *array, char *str, uint length, int duplicate); 添加一个指定长度的字符串。其余跟add_next_index_string () 相同。
add_next_index_zval(zval *array, zval *value); 添加一个 zval 结构。 这在添加另外一个数组、对象或流等数据时会很有用。
具体使用方法很简单,看参数名称就知道方法了,自己试验吧…
