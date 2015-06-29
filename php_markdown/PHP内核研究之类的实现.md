原创:PHP内核研究之类的实现



    class student {}
    
    
    unticked_class_declaration_statement:
    class_entry_type T_STRING extends_from
    { zend_do_begin_class_declaration(&$1, &$2, &$3 TSRMLS_CC); }
    implements_list
    '{'
    class_statement_list
    '}' { zend_do_end_class_declaration(&$1, &$2 TSRMLS_CC); }
    |   interface_entry T_STRING
    { zend_do_begin_class_declaration(&$1, &$2, NULL TSRMLS_CC); }
    interface_extends_list
    '{'
    class_statement_list
    '}' { zend_do_end_class_declaration(&$1, &$2 TSRMLS_CC); }
    ;
    class_entry_type:
    T_CLASS { $$.u.opline_num = CG(zend_lineno); $$.u.EA.type = 0; }
    |   T_ABSTRACT T_CLASS { $$.u.opline_num = CG(zend_lineno); $$.u.EA.type = ZEND_ACC_EXPLICIT_ABSTRACT_CLASS; }
    |   T_FINAL T_CLASS { $$.u.opline_num = CG(zend_lineno); $$.u.EA.type = ZEND_ACC_FINAL_CLASS; }
    ;





#####T_CLASS,T_ABSTRACT T_CLASS和T_FINAL 是PHP的三种类的模式
#####T_CLASS:是一个标准类.
#####T_ABSTRACT:是声明一个抽象类
#####T_FINAL:声明一个不容许继承和扩展的类.
#####当然还有interface
#####他们定义在Zend/zend_complie.h的文件中

    #define ZEND_ACC_IMPLICIT_ABSTRACT_CLASS0x10//没有声明为抽象,但是内部有抽象方法
    #define ZEND_ACC_EXPLICIT_ABSTRACT_CLASS0x20   //抽象
    #define ZEND_ACC_FINAL_CLASS0x40  //Final
    #define ZEND_ACC_INTERFACE  0x80 //接口



####这三个规则 记录当前行,并设置类的类型.
####在定义类的时候调用了 ####zend_do_begin_class_declaration和zend_do_end_class_declaration两个方法,
####类的关键字 ,类的名称和所继承的父类作为参数传递给这两个函数.
####zend_do_begin_class_declaration是用来声明类,设置类型,创建一个
####zend_do_end_class_declaration用来处理类中的属性及方法.
####在讲到两个函数之前一定先要说说 保存类的结构####zend_class_entry
####它定义在Zend/zend.h中



    struct _zend_class_entry {
       char type;
       char *name;//类名称
       zend_uint name_length;
       struct _zend_class_entry *parent; //所继承的父类
    int refcount;  //引用数
    zend_bool constants_updated; //类的类型
    zend_uint ce_flags;//类的类型 抽象?接口?Final?
    HashTable function_table;  //函数表
    HashTable default_properties; //属性
    HashTable properties_info;  //函数的访问级别
    HashTable default_static_members; //静态成员
    HashTable *static_members; //静态成员,当是用户声明的类等于default_static_members,内置的类为NULL
    HashTable constants_table;
    const struct _zend_function_entry *builtin_functions;
       //魔术函数在这里哦..
    union _zend_function *constructor;
    union _zend_function *destructor;
    union _zend_function *clone;
    union _zend_function *__get;
    union _zend_function *__set;
    union _zend_function *__unset;
    union _zend_function *__isset;
    union _zend_function *__call;
    union _zend_function *__callstatic;
    union _zend_function *__tostring;
    union _zend_function *serialize_func;
    union _zend_function *unserialize_func;
     
    zend_class_iterator_funcs iterator_funcs;
     
    /* handlers */
    zend_object_value (*create_object)(zend_class_entry *class_type TSRMLS_DC);
    zend_object_iterator *(*get_iterator)(zend_class_entry *ce, zval *object, int by_ref TSRMLS_DC);
    int (*interface_gets_implemented)(zend_class_entry *iface, zend_class_entry *class_type TSRMLS_DC); /* a class implements this interface */
    union _zend_function *(*get_static_method)(zend_class_entry *ce, char* method, int method_len TSRMLS_DC);
     
    /* serializer callbacks */
    int (*serialize)(zval *object, unsigned char **buffer, zend_uint *buf_len, zend_serialize_data *data TSRMLS_DC);
    int (*unserialize)(zval **object, zend_class_entry *ce, const unsigned char *buf, zend_uint buf_len, zend_unserialize_data *data TSRMLS_DC);
     
    zend_class_entry **interfaces;
    zend_uint num_interfaces;
     
    char *filename;//声明类的文件地址
    zend_uint line_start;//类开始行
    zend_uint line_end;//类结束行
    char *doc_comment;
    zend_uint doc_comment_len;
     
    struct _zend_module_entry *module;
    };

zend_do_begin_class_declaration函数


    void zend_do_begin_class_declaration(const znode *class_token, znode *class_name, const znode *parent_class_name TSRMLS_DC) /* {{{ */
    {
    zend_op *opline;
    int doing_inheritance = 0;
    zend_class_entry *new_class_entry;
    char *lcname;
    int error = 0;
    zval **ns_name;
     
        if (CG(active_class_entry)) {
                zend_error(E_COMPILE_ERROR, "Class declarations may not be nested");
                return;
        }
 
        lcname = zend_str_tolower_dup(class_name->u.constant.value.str.val, class_name->u.constant.value.str.len);
 
        if (!(strcmp(lcname, "self") && strcmp(lcname, "parent"))) {
                efree(lcname);
                zend_error(E_COMPILE_ERROR, "Cannot use '%s' as class name as it is reserved", class_name->u.constant.value.str.val);
        }
 
        /* Class name must not conflict with import names */
        if (CG(current_import) &&
                        zend_hash_find(CG(current_import), lcname, Z_STRLEN(class_name->u.constant)+1, (void**)&ns_name) == SUCCESS) {
                error = 1;
        }
       if (CG(current_namespace)) {
                /* Prefix class name with name of current namespace */
                znode tmp;
 
                tmp.u.constant = *CG(current_namespace);
                zval_copy_ctor(&tmp.u.constant);
                zend_do_build_namespace_name(&tmp, &tmp, class_name TSRMLS_CC);
                class_name = &tmp;
                efree(lcname);
                lcname = zend_str_tolower_dup(Z_STRVAL(class_name->u.constant), Z_STRLEN(class_name->u.constant));
        }
 
        if (error) {
                char *tmp = zend_str_tolower_dup(Z_STRVAL_PP(ns_name), Z_STRLEN_PP(ns_name));
 
                if (Z_STRLEN_PP(ns_name) != Z_STRLEN(class_name->u.constant) ||
                        memcmp(tmp, lcname, Z_STRLEN(class_name->u.constant))) {
                        zend_error(E_COMPILE_ERROR, "Cannot declare class %s because the name is already in use", Z_STRVAL(class_name->u.constant));
                }
                efree(tmp);
        }
 
        new_class_entry = emalloc(sizeof(zend_class_entry));
        new_class_entry->type = ZEND_USER_CLASS;
        new_class_entry->name = class_name->u.constant.value.str.val;
        new_class_entry->name_length = class_name->u.constant.value.str.len;
 
        zend_initialize_class_data(new_class_entry, 1 TSRMLS_CC);
        new_class_entry->filename = zend_get_compiled_filename(TSRMLS_C);
        new_class_entry->line_start = class_token->u.opline_num;
        new_class_entry->ce_flags |= class_token->u.EA.type;
if (parent_class_name && parent_class_name->op_type != IS_UNUSED) {
                switch (parent_class_name->u.EA.type) {
                        case ZEND_FETCH_CLASS_SELF:
                                zend_error(E_COMPILE_ERROR, "Cannot use 'self' as class name as it is reserved");
                                break;
                        case ZEND_FETCH_CLASS_PARENT:
                                zend_error(E_COMPILE_ERROR, "Cannot use 'parent' as class name as it is reserved");
                                break;
                        case ZEND_FETCH_CLASS_STATIC:
                                zend_error(E_COMPILE_ERROR, "Cannot use 'static' as class name as it is reserved");
                                break;
                        default:
                                break;
                }
                doing_inheritance = 1;
        }
 
        opline = get_next_op(CG(active_op_array) TSRMLS_CC);
        opline->op1.op_type = IS_CONST;
        build_runtime_defined_function_key(&opline->op1.u.constant, lcname, new_class_entry->name_length TSRMLS_CC);
 
        opline->op2.op_type = IS_CONST;
        opline->op2.u.constant.type = IS_STRING;
        Z_SET_REFCOUNT(opline->op2.u.constant, 1);
 
        if (doing_inheritance) {
                opline->extended_value = parent_class_name->u.var;
                opline->opcode = ZEND_DECLARE_INHERITED_CLASS;
        } else {
                opline->opcode = ZEND_DECLARE_CLASS;
        }
opline->op2.u.constant.value.str.val = lcname;
        opline->op2.u.constant.value.str.len = new_class_entry->name_length;
 
        zend_hash_update(CG(class_table), opline->op1.u.constant.value.str.val, opline->op1.u.constant.value.str.len, &new_class_entry, sizeof(zend_class_entry *), NULL);
        CG(active_class_entry) = new_class_entry;
 
        opline->result.u.var = get_temporary_variable(CG(active_op_array));
        opline->result.op_type = IS_VAR;
        CG(implementing_class) = opline->result;
 
        if (CG(doc_comment)) {
                CG(active_class_entry)->doc_comment = CG(doc_comment);
                CG(active_class_entry)->doc_comment_len = CG(doc_comment_len);
                CG(doc_comment) = NULL;
                CG(doc_comment_len) = 0;
        }
}

lcname = zend_str_tolower_dup(class_name->u.constant.value.str.val, class_name->u.constant.value.str.len);
```
把所有类全部转换为小写处理.这就是为什么PHP大小写不敏感的原因.


```c
if (!(strcmp(lcname, “self”) && strcmp(lcname, “parent”))) {
efree(lcname);
zend_error(E_COMPILE_ERROR, “Cannot use ‘%s’ as class name as it is reserved”, class_name->u.constant.value.str.val);
}
```
类的名字不能是self和parent.
第23-26行 用来检测类名是否重复定义.
第27-37行 用来设置命名空间,这是PHP5.3的新特性
第39-47行 用来抛出重复定义的错误
第49-57行 初始化保存类的结构
```c
zend_initialize_class_data(new_class_entry, 1 TSRMLS_CC);函数是用来初始化结构里面的HashTable,魔术方法.
```
这个函数里面也有上面提到( HashTable *static_members; //静态成员,当是用户声明的类等于default_static_members,内置的类为NULL)的原因
第58-73行 同样用来检测父类的类名是否包含 保留关键字 self,parent,static
剩下的就是用来生成一个OP,
是内部类:那么生成的OP中间代码就是 ZEND_DECLARE_INHERITED_CLASS
是用户类:OP中间代码就是ZEND_DECLARE_CLASS
在这之后..Zend引擎会调用zend_execute函数执行OP的中间代码ZEND_DECLARE_CLASS_SPEC_HANDLER
它定义在Zend/zend_vm_execute.h中.
这个函数将执行关键代码
EX_T(opline->result.u.var).class_entry = do_bind_class(opline, EG(class_table), 0 TSRMLS_CC) ;
do_bind_class会将此类放到class_table中.当然 ,在这个函数里还会判断该类是否存在.不存在会抛出错误
Internal Zend error – Missing class information for %s
