#php function

```
function hello($str){
echo $str;
}
```

在/zend/zend_language_parse.y中找到 T_FUNCTION

```
function:
        T_FUNCTION { $$.u.opline_num = CG(zend_lineno); };
```

```
unticked_function_declaration_statement: //译为 "函数声明语句"
                function is_reference T_STRING { zend_do_begin_function_declaration(&$1, &$3, 0, $2.op_type, NULL TSRMLS_CC); }
                        '(' parameter_list ')' '{' inner_statement_list '}' { zend_do_end_function_declaration(&$1 TSRMLS_CC); }
```


```c
void zend_do_begin_function_declaration(znode *function_token, znode *function_name, int is_method, int return_reference, znode *fn_flags_znode TSRMLS_DC) /* {{{ */
{
        zend_op_array op_array;
        char *name = function_name->u.constant.value.str.val; //函数名
        int name_len = function_name->u.constant.value.str.len;//函数名长度
        int function_begin_line = function_token->u.opline_num;//函数定义的位置
        zend_uint fn_flags;
        char *lcname;
        zend_bool orig_interactive;
        if (is_method) { //是类的方法? 这里不涉及到类的方法的内容 所以暂时跳过
                if (CG(active_class_entry)->ce_flags & ZEND_ACC_INTERFACE) {
                        if ((Z_LVAL(fn_flags_znode->u.constant) & ~(ZEND_ACC_STATIC|ZEND_ACC_PUBLIC))) {
                        }
                        Z_LVAL(fn_flags_znode->u.constant) |= ZEND_ACC_ABSTRACT; /* propagates to the rest of the parser */
                }
                fn_flags = Z_LVAL(fn_flags_znode->u.constant); /* must be done *after* the above check */
        } else {
                fn_flags = 0;
        }
        //类相关 跳过
        if ((fn_flags & ZEND_ACC_STATIC) && (fn_flags & ZEND_ACC_ABSTRACT) && !(CG(active_class_entry)->ce_flags & ZEND_ACC_INTERFACE)) {
           zend_error(E_STRICT, "Static function %s%s%s() should not be abstract", is_method ? CG(active_class_entry)->name : "", is_method ? "::" : "", Z_STRVAL(function_name->u.constant));
        }
        //转换为小写
        lcname = zend_str_tolower_dup(name, name_len);
 
        orig_interactive = CG(interactive);
        CG(interactive) = 0;
        //初始化zend_op_array
        /*要特别说明一下 在PHP里面 函数有两种一种是自定义函数:ZEND_USER_FUNCTION,
         *一种是内置函数ZEND_INTERNAL_FUNCTION,这里我们是自定义函数所以 类型为ZEND_USER_FUNCTION
          */
        init_op_array(&op_array, ZEND_USER_FUNCTION, INITIAL_OP_ARRAY_SIZE TSRMLS_CC);
        CG(interactive) = orig_interactive;
 
        op_array.function_name = name; //函数名称
        op_array.return_reference = return_reference; //是否是引用函数
        op_array.fn_flags |= fn_flags; //可能是标示声明为类的方法
        op_array.pass_rest_by_reference = 0; //所有参数都强制为引用?
        op_array.prototype = NULL;//
 
        op_array.line_start = zend_get_compiled_lineno(TSRMLS_C);//开始行
        if (is_method) {//类的方法 以下....省略
 
        } else {//到这里 ,用户函数
                //生成一个 zend_op
                zend_op *opline = get_next_op(CG(active_op_array) TSRMLS_CC);
 
                if (CG(current_namespace)) { //5.3新特性 支持命名空间
                        /* Prefix function name with current namespcae name */
                        znode tmp;
 
                        tmp.u.constant = *CG(current_namespace);
                        zval_copy_ctor(&tmp.u.constant);
                        zend_do_build_namespace_name(&tmp, &tmp, function_name TSRMLS_CC);
                        op_array.function_name = Z_STRVAL(tmp.u.constant);
                        efree(lcname);
                        name_len = Z_STRLEN(tmp.u.constant);
                        lcname = zend_str_tolower_dup(Z_STRVAL(tmp.u.constant), name_len);
                }
                //生成的中间代码
                opline->opcode = ZEND_DECLARE_FUNCTION;
                //类型
                opline->op1.op_type = IS_CONST;
                build_runtime_defined_function_key(&opline->op1.u.constant, lcname, name_len TSRMLS_CC);
                opline->op2.op_type = IS_CONST;
                opline->op2.u.constant.type = IS_STRING;
                opline->op2.u.constant.value.str.val = lcname;
                opline->op2.u.constant.value.str.len = name_len;
                Z_SET_REFCOUNT(opline->op2.u.constant, 1);
                opline->extended_value = ZEND_DECLARE_FUNCTION;
               //更新函数表的HashTable
               zend_hash_update(CG(function_table), opline->op1.u.constant.value.str.val, opline->op1.u.constant.value.str.len, &op_array, sizeof(zend_op_array), (void **) &CG(active_op_array));
        }
 
        if (CG(compiler_options) & ZEND_COMPILE_EXTENDED_INFO) {
                zend_op *opline = get_next_op(CG(active_op_array) TSRMLS_CC);
 
                opline->opcode = ZEND_EXT_NOP;
                opline->lineno = function_begin_line;
                SET_UNUSED(opline->op1);
                SET_UNUSED(opline->op2);
        }
 
        {
                /* Push a seperator to the switch and foreach stacks */
                zend_switch_entry switch_entry;
 
                switch_entry.cond.op_type = IS_UNUSED;
                switch_entry.default_case = 0;
                switch_entry.control_var = 0;
 
                zend_stack_push(&CG(switch_cond_stack), (void *) &switch_entry, sizeof(switch_entry));
 
                {
                        /* Foreach stack separator */
                        zend_op dummy_opline;
 
                        dummy_opline.result.op_type = IS_UNUSED;
                        dummy_opline.op1.op_type = IS_UNUSED;
 
                        zend_stack_push(&CG(foreach_copy_stack), (void *) &dummy_opline, sizeof(zend_op));
                }
        }
 
        if (CG(doc_comment)) {
                CG(active_op_array)->doc_comment = CG(doc_comment);
                CG(active_op_array)->doc_comment_len = CG(doc_comment_len);
                CG(doc_comment) = NULL;
                CG(doc_comment_len) = 0;
        }
 
        zend_stack_push(&CG(labels_stack), (void *) &CG(labels), sizeof(HashTable*));
        CG(labels) = NULL;
}
```
自定义函数结构

```c
typedef union _zend_function {
    zend_uchar type;    /* MUST be the first element of this struct! */
 
    struct {
        zend_uchar type;  /* never used */
        char *function_name; //函数名称
        zend_class_entry *scope;
        zend_uint fn_flags;
        union _zend_function *prototype;
        zend_uint num_args; //参数个数
        zend_uint required_num_args;
        zend_arg_info *arg_info;
        zend_bool pass_rest_by_reference;
        unsigned char return_reference;
    } common;
 
    zend_op_array op_array;
    zend_internal_function internal_function;
} zend_function;
```
初始化op_array
生成 zend_op
生成的中间码 ZEND_DECLARE_FUNCTION
更新function_table

