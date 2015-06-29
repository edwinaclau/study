```c

PHP_FUNCTION(count)
{
        zval *array;
        long mode = COUNT_NORMAL; //这是count第二个参数的默认值
       //获取两个参数
        if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "z|l", &array, &mode) == FAILURE) {
                return;
        }    
 
        switch (Z_TYPE_P(array)) {
                case IS_NULL:
                        RETURN_LONG(0);//空直接返回0
                        break;
                case IS_ARRAY: //计算数组元素个数
                        RETURN_LONG (php_count_recursive (array, mode TSRMLS_CC));
                        break;
                case IS_OBJECT: {
#ifdef HAVE_SPL
                        zval *retval;
#endif
                        /* first, we check if the handler is defined */
                        if (Z_OBJ_HT_P(array)->count_elements) {
                                RETVAL_LONG(1);
                                if (SUCCESS == Z_OBJ_HT(*array)->count_elements(array, &Z_LVAL_P(return_value) TSRMLS_CC)) {
                                        return;
                                }
                        }
#ifdef HAVE_SPL //如果安装了 SPL
                        /* if not and the object implements Countable we call its count() method */
                        if (Z_OBJ_HT_P(array)->get_class_entry && instanceof_function(Z_OBJCE_P(array), spl_ce_Countable TSRMLS_CC)) {
                                zend_call_method_with_0_params(&array, NULL, NULL, "count", &retval);
                                if (retval) {
                                        convert_to_long_ex(&retval);
                                        RETVAL_LONG(Z_LVAL_P(retval));
                                        zval_ptr_dtor(&retval);
                                }
                                return;
                        }
#endif
                }
                default://其他类型返回1
                        RETURN_LONG(1);
                        break;
        }
}


```




count只计算数组和对象的元素个数,对于其他类型的值,全部返回1
我们重点说一下对于数组类型的数据是如何处理的
函数 php_count_recursive 也接受两个参数,array和mode,与count的参数相同


static int php_count_recursive(zval *array, long mode TSRMLS_DC) /* {{{ */
{
        long cnt = 0;
        zval **element;
 
        if (Z_TYPE_P(array) == IS_ARRAY) { //如果是数组 再处理
                if (Z_ARRVAL_P(array)->nApplyCount > 1) {//检测数据是否被循环遍历过
                        php_error_docref(NULL TSRMLS_CC, E_WARNING, "recursion detected");
                        return 0;
                }
                // return ht->nNumOfElements;返回数组个数
                cnt = zend_hash_num_elements(Z_ARRVAL_P(array));
                if (mode == COUNT_RECURSIVE) {
                        HashPosition pos;
                        for (zend_hash_internal_pointer_reset_ex(Z_ARRVAL_P(array), &pos);
                                zend_hash_get_current_data_ex(Z_ARRVAL_P(array), (void **) &element, &pos) == SUCCESS;
                                zend_hash_move_forward_ex(Z_ARRVAL_P(array), &pos)                        ) {
                                Z_ARRVAL_P(array)->nApplyCount++;
                                cnt += php_count_recursive(*element, COUNT_RECURSIVE TSRMLS_CC);//递归
                                Z_ARRVAL_P(array)->nApplyCount--;
                        }
                }
        }               
 
        return cnt;
}
只有mode==COUNT_RECURSIVE的时候才会递归重新计算数组数量
不指定mode时,只返回元素个数 nNumOfElements
这样就很明显了
那么echo count(“abc”)的结果就是1.