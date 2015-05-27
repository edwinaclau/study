    
    $arr = array(1, 2, 3, 4, 5);
    
    foreach ($arr as $key => $row) {
     echo $key , $row;
    }
    



    foreach ($arr as $key => &$row) {
    echo $key , $row;
    }

问题出来了
    
    typedef struct _hashtable {
    uint nTableSize;/* 散列表大小, Hash值的区间 */
    uint nTableMask;/* 等于nTableSize -1, 用于快速定位 */
    uint nNumOfElements;/* HashTable中实际元素的个数 */
    ulong nNextFreeElement; /* 下个空闲可用位置的数字索引 */
    Bucket *pInternalPointer;   /* 内部位置指针, 会被reset, current这些遍历函数使用 */
    Bucket *pListHead;  /* 头元素, 用于线性遍历 */
    Bucket *pListTail;  /* 尾元素, 用于线性遍历 */
    Bucket **arBuckets; /* 实际的存储容器 */
    dtor_func_t pDestructor;/* 元素的析构函数(指针) */
    zend_bool persistent;
    unsigned char nApplyCount; /* 循环遍历保护 */
    zend_bool bApplyProtection;
    #if ZEND_DEBUG
    int inconsistent;
    #endif
    } HashTable;
    

这个字段就是为了防治循环引用导致的无限循环而设立的.

    <?php
    
    $arr = array("foo",
     "bar",
     "baz");
    
    foreach ($arr as &$item) { /* do nothing by reference */ }
    print_r($arr);
    
    foreach ($arr as $item) { /* do nothing by value */ }
    print_r($arr); // $arr has changed....why?
    
    ?>
This outputs:

    Array
    (
    [0] => foo
    [1] => bar
    [2] => baz
    )
    Array
    (
    [0] => foo
    [1] => bar
    [2] => bar
    )
    


第一次循环时候 , $arr[2] 变成 $arr[0]


    $arr[2] = $arr[1]
    
    
    foreach ($arr as &$item) { /* do nothing by reference */ }
    print_r($arr);
    
    unset($item); // This will fix the issue.
    
    foreach ($arr as $item) { /* do nothing by value */ }
    print_r($arr); // $arr has changed....why?


在PHP手册中有这样一个NOTE:

Note: 当 foreach 开始执行时，数组内部的指针会自动指向第一个单元。这意味着不需要在 foreach 循环之前调用 reset()。 由于 foreach 依赖内部数组指针，在循环中修改其值将可能导致意外的行为。