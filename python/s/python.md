1.类型的类型

obj int(10).ob_type -> PyInt_Type
PyInt_Type.ob_type -> PyType_Type
PyInt_Type.tp_base -> PyBaseObject_Type
PyBaseObject_Type.ob_type -> PyType_Type
PyType_Type.ob_type -> PyType_Type

更精确的参考源码解析262页图。

2.小整数对象

if (-NSMALLNEGINTS <= ival && ival < NSMALLPOSINTS) {
    v = small_ints[ival + NSMALLNEGINTS];
    Py_INCREF(v);
}

3.大整数对象，空对象池，对象缓存

>>> a = 1000000
>>> b = 2000000
>>> id(a) == id(1000000)
False
>>> id(100000) == id(100000)
True

最后一个是因为python解析器在解析对象的时候，对前后生成的对象进行了缓存。经过测试，对文件也有效。

4.字符串对象复用和缓存

>>> c = 'qazwsxedcrfvt'
>>> c += 'gbyhnujmikolp'
>>> a = 'qazwsxedcrfvtgbyhnujmikolp'
>>> id(a) == id(c)
False
>>> a = 'abc'
>>> b = 'def'
>>> c = 'abc'
>>> id(a) == id(c)
True
>>> b = 'abcde'
>>> id(b[1]) == id(c[1])
True

缓存原理同上，对于长度为0, 1的小字符串，永久缓存。

5.free_list对象缓存的机制

每个类别有自己的free_list对象，用于缓存已经被销毁的对象。目前尚不清楚GC是否会定时释放这部分内存，但是python在对象引用到0时是不释放对象的，而且多数情况下表现为内存泄漏。而且多种对象的free_list不能互相通用，继承子类也不适用。

6.list对象的行为

list对象用一种vector等同的方法处理对象池。因此随机插入（尤其是头部插入）一个对象超长队列会引发大量的内存复制行为。

7.dict对象的索引方案

dict对象的索引方案使用的是哈希表，而且是开放地址法的哈希表。当装载率达到一定规模后，会新申请一块内存，将有效数据复制过去。最小的表空间为8个对象，当装载率超过2/3时，会扩大规模到当前active的4倍（超过50000个对象为2倍）。目前为止，在对象被删除后，其表空间并不释放。因此曾经增长的非常大的dict对象，可以定期复制以回收空间。

8.dict的用法注释

从序列中移除重复对象

dict.fromkeys(seqn).keys()

计算序列中元素出现次数

for e in seqn: d[e] = d.get(e,0) + 1

词典中移除大量元素

d = dict([(k, v) for k, v in d.items() if k != xxx])

词典中访问可能不存在的元素（当不存在的风险高于5%时）

o = d.get(k, default)

词典中访问可能不存在的元素（当不存在的风险低于5%时）

try: o = d[k]
except KeyError: o = default