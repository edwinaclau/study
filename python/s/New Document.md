1.mro

算法，自身先入栈，而后按声明顺序继承每个父类的mro，内部对象在最后。简单来说，深度优先，从左向右。

当类对象创建时，会将父类所有函数全部复制过来（很明显，应当是符号复制）。

2.super规则

>>> class A(object):
…     def f(self): print 'A'
…
>>> class B(object):
…     def f(self): print 'B'
…
>>> class C(A):
…     def f(self): print 'C'
…
>>> class D(C, B):

…     def f(self): super(D, self).f()
…
>>> d = D()
>>> d.f()
C
>>> D.__base__
<class '__main__.C'>
>>> D.__bases__

(<class '__main__.C'>, <class '__main__.B'>)
>>> class A(object):
…     def f(self): print 'A'
…
>>> class B(object):
…     def g(self): print 'B'
…
>>> class C(A, B):
…     def f(self): super(C, self).g()
…
>>> c = C()
>>> c.f()
B
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <type 'object'>)

super的算法是跟随mro次序，寻找非本类第一个符合名称的函数，调用之。

3.construct

instance = cls.__new__(cls, *args, **kargs)
cls.__init__(instance, *args, **kargs)

4.bound method

>>> class A(object):
…     def f(self): pass
…
>>> a = A()
>>> a.__class__.__dict__['f']
<function f at 0xb7595454>
>>> a.f
<bound method A.f of <__main__.A object at 0xb75a1e6c>>
>>> a.f.im_self
<__main__.A object at 0xb75a1e6c>

bound method是一个函数对象和一个实例对象的集合。

5.descriptor

>>> class A(object):
…     def __get__(self, obj, cls): return 'A.__get__ %s %s %s' % (self, obj, cls)

…
>>> class B(object):
…     v = A()
…
>>> b = B()
>>> b.v
"A.__get__ <__main__.A object at 0xb75a1cac> <__main__.B object at 0xb75a1cec> <class '__main__.B'>"

某个instance的属性查找顺序为，obj.__dict__，class属性（按照mro顺序）。如果有data descriptor则先于obj.__dict__。

于是，这解释了一个问题。我们定义函数的时候，定义的都是“类函数”，即函数是类的成员。为什么最终函数会变成实例的成员呢？为什么又在调用时会自动产生一个self呢？

实例在查找的时候，会先查找class属性中的descriptor。假定class有成员函数f，当使用obj.f时，首先命中这个函数对象，因为这个对象是一个descriptor。descriptor在取值时，会被调用__get__方法，这一方法有obj参数。于是函数对象的默认__get__返回了一个bound method，其中包含了self和函数对象自身。

这种行为在每次调用时都会发生，因此实例成员函数的性能比unbound method直接写对象要慢。