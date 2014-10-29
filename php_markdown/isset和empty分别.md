# PHP内核函数里面有提供了两个函数用来检测 变量
####isset和empty,这两个有什么区别?

```php
<?php
//第一种
var_dump(empty($a));   //true  为空
var_dump(isset($a));   //false  未设置
//第二种
$b=0;
var_dump(empty($b));  //true  为空
var_dump(isset($b));  //true 已设置
//第三种
$c=0;
unset($c);
var_dump(empty($c));  //true 为空
var_dump(isset($c));  //false 未设置
//第四种
$d=NULL;
var_dump(empty($c));  //true 为空
var_dump(isset($c));  //false 未设置
?>
```

### 1. 经过试验发现,empty不仅检测是否设置 而且还检测 是否为0,如果为0 也返回空
### 2而 isset只要 变量设置,并不等於NULL或者没有unset 就返回true



####下面看看PHP的内核源码详细分析下

####我们先来看看 分别执行 isset和empty ,PHP生成的op
isset:




     0  >   ZEND_ISSET_ISEMPTY_VAR                        5   RES[  IS_TMP_VAR ~0 ]       OP1[  IS_CV !0 ] OP2[  IS_UNUSED  ]
     1      FREE                                                      OP1[  IS_TMP_VAR ~0 ]
     2    > RETURN                                                    OP1[  IS_CONST (0) 1 ]
empty :




  >   ZEND_ISSET_ISEMPTY_VAR                        6   RES[  IS_TMP_VAR ~0 ]       OP1[  IS_CV !0 ] OP2[  IS_UNUSED  ]
      FREE                                                      OP1[  IS_TMP_VAR ~0 ]
   > RETURN                                                    OP1[  IS_CONST (0) 1 ]
经过观察发现,他们是一样的..op指向的handler都是ZEND_ISSET_ISEMPTY_VAR,说明他们执行了同样的检测函数
两个YACC所对应的代码是
T_EMPTY ‘(‘ variable ‘)’ { zend_do_isset_or_isempty(ZEND_ISEMPTY, &$$, &$3 TSR MLS_CC);
还有
variable { zend_do_isset_or_isempty(ZEND_ISSET, &$$, &$1 TSRMLS_CC);

验证了我们上面的推断,都执行了共同的函数 zend_do_isset_or_isempty,只是第一个传参不同
看看zend_do_isset_or_isempty的定义

```c
void zend_do_isset_or_isempty(int type, znode *result, znode *variable TSRMLS_DC) /* {{{ */
{
        zend_op *last_op;
 
        zend_do_end_variable_parse(variable, BP_VAR_IS, 0 TSRMLS_CC);
//此函数下面有特别说明
        zend_check_writable_variable(variable);
 
        if (variable->op_type == IS_CV) { //如果已经编译过 也就是参数是一个变量
                last_op = get_next_op(CG(active_op_array) TSRMLS_CC);          //创建一个 zend_op
                last_op->opcode = ZEND_ISSET_ISEMPTY_VAR;
                last_op->op1 = *variable;
                SET_UNUSED(last_op->op2);
                last_op->op2.u.EA.type = ZEND_FETCH_LOCAL; //当前作用域
                last_op->result.u.var = get_temporary_variable(CG(active_op_array));
                last_op->extended_value = ZEND_QUICK_SET;
        } else {
                last_op = &CG(active_op_array)->opcodes[get_next_op_number(CG(active_op_array))-1];
 
                switch (last_op->opcode) {
                        case ZEND_FETCH_IS:
                                last_op->opcode = ZEND_ISSET_ISEMPTY_VAR;
                                break;
                        case ZEND_FETCH_DIM_IS:
                                last_op->opcode = ZEND_ISSET_ISEMPTY_DIM_OBJ;
                                break;
                        case ZEND_FETCH_OBJ_IS:
                                last_op->opcode = ZEND_ISSET_ISEMPTY_PROP_OBJ;
                                break;
                }
                last_op->extended_value = 0;
        }
        //result为临时变量
        last_op->result.op_type = IS_TMP_VAR;
        last_op->extended_value |= type;
        *result = last_op->result;
}
```
zend_check_writable_variable这里要特别说明一下
isset和empty只检测变量,如果传递一个方法或函数进来,会报错,这个函数就是来检测传递进来的参数是否是一个函数或方法
如果是会抛出错误.
下面是定义

```c
void zend_check_writable_variable(const znode *variable) /* {{{ */
{
        zend_uint type = variable->u.EA.type;
 
        if (type & ZEND_PARSED_METHOD_CALL) {//类型是方法?
                zend_error(E_COMPILE_ERROR, "Can't use method return value in write context");
        }
        if (type == ZEND_PARSED_FUNCTION_CALL) {//类型是函数?
                zend_error(E_COMPILE_ERROR, "Can't use function return value in write context");
        }
}
```

zend_do_isset_or_isempty的作用就是 创建一个ZEND_OP..那么好像并没有 empty或者isset的作用啊..
这个时候就不得不提一下 op的执行过程了
创建定义好 _zend_op 之后..
解释器引擎会最终将op在zend_execute函数里执行,
zend_execute只是一个指针函数 它指向 zend_vm_executes.h里面的execute函数
详情请查看 >>>
execute 首先会构造zend_execute_data 指针,设置参数把op中间代码全都放在execute_data里.
execute_data下面会讲到
last_op->opcode = ZEND_ISSET_ISEMPTY_VAR;
它会被execute解析 成
ZEND_ISSET_ISEMPTY_VAR_SPEC_CV_HANDLER 函数


```c
static int ZEND_FASTCALL  ZEND_ISSET_ISEMPTY_VAR_SPEC_CV_HANDLER(ZEND_OPCODE_HANDLER_ARGS){
        zend_op *opline = EX(opline); //当前执行的OP
        zval **value;
        zend_bool isset = 1;
        if (IS_CV == IS_CV && (opline->extended_value & ZEND_QUICK_SET)) { //参数是解析的变量
                if (EX(CVs)[opline->op1.u.var]) { //在上面zend_do_isset_or_isempty已经处理过,索引号保存在opline->op1.u.var里面
                        value = EX(CVs)[opline->op1.u.var];//获取到这个值
                } else if (EG(active_symbol_table)) {  //如果zend_do_isset_or_isempty没有处理就要从局部变量表里面去找
                        zend_compiled_variable *cv = &CV_DEF_OF(opline->op1.u.var);
                       if (zend_hash_quick_find(EG(active_symbol_table), cv->name, cv->name_len+1, cv->hash_value, (void **) &value) == FAILURE) {
                                isset = 0; //没有找到 也就是没有设置 ,那么isset=0
                        }
                } else {
                        isset = 0;
                }
        } else {
                HashTable *target_symbol_table;
 
                zval tmp, *varname = _get_zval_ptr_cv(&opline->op1, EX(Ts), BP_VAR_IS TSRMLS_CC);
 
                if (Z_TYPE_P(varname) != IS_STRING) {
                        tmp = *varname;
                        zval_copy_ctor(&tmp);
                        convert_to_string(&tmp);
                        varname = &tmp;
                }
 
                if (opline->op2.u.EA.type == ZEND_FETCH_STATIC_MEMBER) {
                        if (!value) {
                                isset = 0;
                        }
                } else {
                                isset = 0;
                        }
                }
 
                if (varname == &tmp) {
                        zval_dtor(&tmp);
                }
 
        }
 
        Z_TYPE(EX_T(opline->result.u.var).tmp_var) = IS_BOOL;
        //这里就是 isset和 empty的区别了
        switch (opline->extended_value & ZEND_ISSET_ISEMPTY_MASK) {
                case ZEND_ISSET:
                        if (isset && Z_TYPE_PP(value) == IS_NULL) {
                                Z_LVAL(EX_T(opline->result.u.var).tmp_var) = 0;
                        } else {
                                Z_LVAL(EX_T(opline->result.u.var).tmp_var) = isset;
                        }
                        break;
                case ZEND_ISEMPTY:
                        if (!isset || !i_zend_is_true(*value)) {
                                Z_LVAL(EX_T(opline->result.u.var).tmp_var) = 1;
                        } else {
                                Z_LVAL(EX_T(opline->result.u.var).tmp_var) = 0;
                        }
                        break;
        }
 
        ZEND_VM_NEXT_OPCODE();
}
```
ZEND_OPCODE_HANDLER_ARGS 展开为
``` c
#define ZEND_OPCODE_HANDLER_ARGS zend_execute_data *execute_data TSRMLS_DC
```
zend_execute_data 用来保存在PHP执行是的数据 ,比如 当前执行的代码 ,局部变量以及在上一条中间代码执行的数据等,


struct _zend_execute_data {
        struct _zend_op *opline;  //当前执行的op
        zend_function_state function_state; //当前执行的函数表 包括用户定义的所有信息,参数,名称,类作用域等
        zend_function *fbc; /* Function Being Called */ //以及执行过的函数
        zend_class_entry *called_scope; //函数的作用域
        zend_op_array *op_array;
        zval *object;
        union _temp_variable *Ts;
        zval ***CVs;
        HashTable *symbol_table; //局部变量符号表
        struct _zend_execute_data *prev_execute_data;  //上一个op的数据
        zval *old_error_reporting;
        zend_bool nested;
        zval **original_return_value;
        zend_class_entry *current_scope;
        zend_class_entry *current_called_scope;
        zval *current_this;
        zval *current_object;
        struct _zend_op *call_opline;
};
里面的属性用 EX宏来获取

源码注释已经基本清楚了 重点来看一下


//这里就是 isset和 empty的区别了
``` c
 switch (opline->extended_value & ZEND_ISSET_ISEMPTY_MASK) {
         case ZEND_ISSET:
                 if (isset && Z_TYPE_PP(value) == IS_NULL) {
                         Z_LVAL(EX_T(opline->result.u.var).tmp_var) = 0;
                 } else {
                         Z_LVAL(EX_T(opline->result.u.var).tmp_var) = isset;
                 }
                 break;
         case ZEND_ISEMPTY:
                 if (!isset || !i_zend_is_true(*value)) {
                         Z_LVAL(EX_T(opline->result.u.var).tmp_var) = 1;
                 } else {
                         Z_LVAL(EX_T(opline->result.u.var).tmp_var) = 0;
                 }
                 break;
 }
 ``` 
 
##### 45-60行就是isset 和empty的区别.
##### 这段代码之前的判断都是一样的区别如下:
##### isset:如果 变量设置了,但是类型确是NULL,那么就直接返回false

##### empty: 返回的状态与 i_zend_is_true返回的状态相同
##### 看看i_zend_is_true

``` c
static inline int i_zend_is_true(zval *op)
{
        int result;
 
        switch (Z_TYPE_P(op)) {
                case IS_NULL:
                        result = 0; //如果为NULL 返回0
                        break;
                case IS_LONG:
                case IS_BOOL:
                case IS_RESOURCE:
                        result = (Z_LVAL_P(op)?1:0); //LONG,BOOL,RESOURCE的值不为空,返回真
                        break;
                case IS_DOUBLE:
                        result = (Z_DVAL_P(op) ? 1 : 0); //浮点数的值为真 返回真
                        break;
                case IS_STRING://字符型:长度为0或者长度等于一且首地址等于0 返回假
                        if (Z_STRLEN_P(op) == 0
                                || (Z_STRLEN_P(op)==1 && Z_STRVAL_P(op)[0]=='0')) {
                                result = 0;
                        } else {
                                result = 1;
                        }
                        break;
                case IS_ARRAY://数组:如果数组的个数大于0则为真
                        result = (zend_hash_num_elements(Z_ARRVAL_P(op))?1:0);
                        break;
                case IS_OBJECT://对象
                        if(IS_ZEND_STD_OBJECT(*op)) { //是OBJECT
                                TSRMLS_FETCH();
 
                                if (Z_OBJ_HT_P(op)->cast_object) {
                                        zval tmp;
                                        if (Z_OBJ_HT_P(op)->cast_object(op, &tmp, IS_BOOL TSRMLS_CC) == SUCCESS) {
                                                result = Z_LVAL(tmp);
                                                break;
                                        }
                                } else if (Z_OBJ_HT_P(op)->get) {
                                        zval *tmp = Z_OBJ_HT_P(op)->get(op TSRMLS_CC);
                                        if(Z_TYPE_P(tmp) != IS_OBJECT) {
                                                /* for safety - avoid loop */
                                                convert_to_boolean(tmp);
                                                result = Z_LVAL_P(tmp);
                                                zval_ptr_dtor(&tmp);
                                                break;
                                        }
                                }
                        }
                        result = 1;
                        break;
                default:
                        result = 0;
                        break;
        }
        return result;
}
``` 
经过分析
isset 只判断 变量是否设置 并且值是否为NULL
empty 则会根据不同的数据类型做了不同的处理
详见i_zend_is_true函数的注释.