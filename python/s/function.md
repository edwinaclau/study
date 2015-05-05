1.函数的性质

>>> def outer(o1, o2):
…     def inner(i1 = 10, i2 = []):
…             return i1+o1+o2
…     return inner
…
>>> a1 = outer(50, 30)
>>> a2 = outer(50, 30)
>>> a1.func_closure
(<cell at 0xb75454f4: int object at 0x8455ddc>, <cell at 0xb7545524: int object at 0x8455cec>)
>>> a2.func_closure
(<cell at 0xb754541c: int object at 0x8455ddc>, <cell at 0xb75453a4: int object at 0x8455cec>)

两次生成的函数对象拥有不同的闭包空间。

>>> a1.func_defaults
(10, [])
>>> a2.func_defaults
(10, [])
>>> a1.func_defaults[1].append(10)
>>> a1.func_defaults
(10, [10])
>>> a2.func_defaults
(10, [])

也拥有不同的默认值空间。

>>> def default_test(d = []):
…     print d
…
>>> default_test.func_defaults
([],)
>>> default_test.func_defaults[0].append(10)
>>> default_test()
[10]

然而同一次生成的默认值空间是共享的，哪怕多次运行。

2.参数传递

>>> def f(a,b,c,d): return a,b,c,d
…
>>> f(1,2,3,4)
(1, 2, 3, 4)
>>> f(1,2,a=3,b=4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: f() got multiple values for keyword argument 'a'
>>> f(1,2,c=3,d=4)
(1, 2, 3, 4)

参数分两种，位置参数和键值参数。具体如何传递是由调用时决定而非编译时。调用时参数必须先以位置参方式传递，再以键值参方式传递。一旦出现键值传递，再出现位置传递即出现编译时非法。调用时会先入栈所有参数，一个位置参占一个对象，一个键值参占两个对象（这是当然）。

解析的时候按照先位置后键值的方式赋值，先将所有位置参依次赋值给所有参数名。如果位置参有多，而没有扩展位置参来接收，则报错TypeError: %s expected at %s %d arguments, got %d。而后将所有键值参赋值给未赋值的参数，如果这个参数名已经赋值，则如上文，报错。如果键值参数有多，又没有扩展键值参来接受，也报错。

最后，如果有参数名尚未赋值，查看这些参数名是否有默认值。如果没有，报错。

另外，在字节码中访问本地（locals）命名空间的时候，是不通过命名空间查询的方式进行的。因为编译时可以明确一个名称是否在locals空间中，而不用理会代码段在名称空间中的位置结构。而一旦明确其在locals命名空间中，则可以直接堆栈访问位置，这样使得locals名称查询速度远高于普通名称空间。对于一个函数内频繁使用的符号，建议做一次赋值，将其引入locals命名空间。

3.调用堆栈

python的调用堆栈是通过PyFrameObject来实现的，每一次调用，python会产生一个新的PyFrameObject加入到栈中。而每个PyFrameObject自带一个小数据区域，用于接收参数，处理局部变量。python字节码指令中的LOAD_FAST，STORE_FAST就是操作的这个区域。

4.层级闭包的实现

>>> def f1():
…     def f2(): return i
…     i = 10
…     return f2
…
>>> a = f1()
>>> a()
10

实现的还是不错的。通过计算当时名称-值的方法就无法获得i。

>>> def f1():
…     def f2():
…             return inet_aton
…     from socket import *
…     return f2
…
<stdin>:1: SyntaxWarning: import * only allowed at module level
  File "<stdin>", line 4
SyntaxError: import * is not allowed in function 'f1' because it is contains a nested function with free variables

这主要是因为闭包的实现是通过函数编译时名称层状传递。例子1在编译时，f2知道上层作用域中有一个名叫i的变量，于是f2的freevars属性就为i。而当f1操作i时，f2保持了一个对结果的引用。当f1返回f2函数对象时，自身的PyFrameObject消失了没错，但是f2中对结果的引用还保存在了func_closure中。当from socket import *的时候，当前locals空间名称会发生变化，从而导致动态引入的名称无法在f2中生效。