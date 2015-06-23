Python 是半编译半解释,载入源码编译成字节码(Byte Code)
Just in time 二次编译器的PyPy可供选择

当虚拟机开始时，

创建解释器和主线程状态对象,
初始化内置类型，数字列表 都有专门缓存策略

创建_builtin_模块，该模块持有所有内置类型的函数
创建sys 模块，包含了sys.path,modules 等重要运行信息
初始化import 机制
初始化Exception
创建__main__模块
通过sitepy,将site-packages
执行第三方
程序执行结束


类型和对象

#define PyObject_HEAD
     Py_ssize_t ob_refcnt;
	 struct _typeobejct *ob_type;

typedef struct _object {
     PyObject_HEAD
} PyObject;

typedef struct {
      PyObject_HEAD
	  long ob_ival;
} PyIntObject;


名字空间


x = 123

y = __import__("string")

type(y)
<type 'module'>

y = __import__("string")


type (y)
<type 'module'>


import sys

globals() is locals()



内存管理



对象引用传递


a = object()

b = a

a is b

True



import copy 

x = object()

l = [x]  创建一个列表

l2 = copy.copy(l)   #浅复制，仅复制对象自身
l2 is l
False

l2[0] is x
True



l3 = copy.deepcopy(l)
l3 is l
False

l3[0] is x
Flase


引用计数


class User(object):
	def __del__(self):
		print "willbe dead"

a = User()
b = a

import sys
sys.getrefcount(a)
3

del a

sys.getrefcount(b)
2


del b


import sys,weakref

class (object)


Python 两套垃圾回收机制，除了引用计数 还有 专门循环引用GC

typedef union _gc_head {
   struct {
          union_gc_head *gc_next;
   }
}

Python GC回收对象分成3级年龄

GEN0 管理新近加入的年轻对象，GEN1 上次回收后依然活着的对象

GEN2 存储生命周期极长的对象


GC首先检查GEN2，如果阀值突破，合并GEN2 GEN1 GEN0 几个追踪表
没有超过，只检查GEN1，GC将存活对象提升年龄，

可回收对象则被打破循环引用，放到专门列表


Python 是 栈式虚拟机(Stack-Based VM)结构

要运行 Python 语言编写，必须源码编译成字节码

编译器将源码转成字节码后保存在pyc 文件中

编译发生在模块载入那一刻、 pyc 和 py 两种情况

载入pyc 流程
  核对文件Magic标记
  检查时间戳和源码文件修改时间是否相同，
  载入模块

如果没有pyc 那么需要先完成编译

对源码进行AST分析
将分析结果编译成PyCodeObject
将Magic 源码文件修改时间 PyCodeObject保存到pyc文件中
载入模块

Magic 是一个特殊的数字


typedef struct {
   PyObject_HEAD
   int co_argcount;
   int co_nlocals;
   int co_stacksize;
   int co_flags;
   PyObject *co_code;
   PyObject *co_consts;
   PyObject *co_names;
   PyObject *co_varnames;
   PyObject *co_freevars;
   PyObjcet *co_cellvars;
   PyObejct *co_filename;
   PyObject *co_name;
   int co_firstlineno;
   PyObject *co_lnotab;
   void *co_zombieframe;
   PyObject *co_weakreflist;
} PyCodeObject;

>>> pycat test.py
"""
Hello, World!
"""
def add(a, b):
return a + b
c = add(10, 20)
>>> code = compile(open("test.py").read(), "test.py", "exec")
>>> code.co_filename, code.co_name, code.co_names
('test.py', '<module>', ('__doc__', 'add', 'c'))
>>> code.co_consts
('\n Hello, World!\n', <code object add at 0x105b76e30, file "test.py", line 5>, 10, 
20, None)
>>> add = code.co_consts[1]
>>> add.co_varnames
('a', 'b')

除了内置 compile 函数，标准库⾥还有 py_compile、compileall 可供选择。
>>> import py_compile, compileall
>>> py_compile.compile("test.py", "test.pyo")
>>> ls
main.py*! test.py! ! test.pyo
>>> compileall.compile_dir(".", 0)
Listing . ...
Compiling ./main.py ...
Compiling ./test.py ...


数字


bool 

None、0、空字符串，没有元素的容器对象视为False

map(bool, [None, 0, "", u"", list(), tuple(), dict(), set(), frozenset()])
[False, False, False, False, False, False, False, False, False]

int(True)
1

int(Flase)
0


del a

int [-5,257) 缓存




大小数字区别

a = 15

b = 15

sys.getrefocount(a)


PyintBlock 只复用，不回收，
大量整数对象导致内存暴涨

range 创建一个巨大数字列表，这需要一个
足够多的PyIntBlock 为数字对象提供存储空间


PyIntBlock 数字提供存储空间



xrange就不同，每次迭代，数字都会被回收

xrange是每次迭代后，数字对象呗回收，占用内存空闲出来并被复用
内存不会暴涨

运⾏下⾯测试代码前，必须先安装 psutil 包，⽤来获取内存统计数据。
$ sudo easy_install -U psutil
$ cat test.py
#!/usr/bin/env python
import gc, os, psutil
def test():
x = 0
for i in range(10000000):! # xrange
x += i
return x
def main():
print test()
gc.collect()
p = psutil.Process(os.getpid())
25
print p.get_memory_info()
if __name__ == "__main__":
main()
对⽐ range 和 xrange 所需的 RSS 值。
range: meminfo(rss=93339648L, vms=2583552000L)! # 89 MB
xrange: meminfo(rss=8638464L, vms=2499342336L)! # 8 MB


long,超出int自动转换成long,


	a = sys.maxint

long python没有专门优化


float 

3/2
1

float(3)/2


字符串  池化(intern) 编码(encode)


	字符串是不可变，保存字符序列
	二进制数据


	短的存储在arena区域，str,unicode 单字符会被永久缓存
	str没有缓存机制，unicode 则保留
	内部包含hash值，str另有标记用来判断是否池化

	字符串 单引号 双引号 三引号



	s = "".join(["a","b","c"])

	s is "abc"
	False

	itern(s) is "abc"
	True




列表

 list 

 列表对象和存储元素 指针的数组分开两块内存，
 后者在堆上，

 虚拟机保留80个列表复用对象，其余元素指针数组会被释放

 列表会动态调用指针数组大小，预分配内存多余实际元素

[]



['a' , 'b']  * 3

['a', 'b'] + ['c', 'd']


list("abcd")


[x for x in range(3)]


l = list("abc")

l[1] = 2



import bisect

l = ["a", "b","c","e"]
l.sort()

l.count('b')
l.index("a", 2) 从指定位置查找

l = list("abc")
l.extend(range(3))



有序列表插入元素
import bisect

l = ["a","d","c","e"]
l.sort()
l





列表用realloc()来调整指针数组大小，可能需要复制，插入 删除
会循环移动后续元素，潜在性能隐患

测试两种创建列表性能差异


import itertools,gc

gc.disable()

def test(n):
	return len([0 for i in xrange(n)])

def test2(n):
	return len(list(itertools.repeat(0, n)))





考虑用数组代替列表，列表存储对象指针不同

数组是直接内嵌数据



import array

a = array.array("l", range(10))

a


a.tolist()


a = array.array("c")


a.forstring("abc")



tuple 元组

只读对象，元组和元素指针数据内存是一次性连续分配

虚拟机缓存n个元素小于20的元组复用对象


尽量使用元组，内存复用高，还利用并发，因为都是读

其他序列转换元组

a = (4)

type(a)
<type 'int'>

a = (4,)
type(a)
<type 'tuple'>

s = tupe("abcdef")
('a','b','c')

s.count(a)


s.index("d")


from collections import namedtuple

User = namedtuple("User","name age"

u = User("user1",10)
u.name, u.age



字典


字典(dict)采用开放地址法的哈希表


自带元素容量 8个 smalltable


缓存80个字典复用对象


按需动态调整容量，扩容，收缩操作重新分配内存，
重新哈希

删除元素操作不会立即收缩内存

{}


{"a":1, "b":2}



dict(["a", 1], ["b",2])


dict(zip("ab", range(2)))
{'a': 1, 'b' : 2}

dict(map(None, "abc", range(2)))
{'a':0, 'c': None, 'b': 1}


dict.fromkeys("abc", 1)



d = {"a":1,"b" : 2}
"b" in d
True

d = {"a":1,"b":2}
del d["b"]

d = {"a":1, "b":3}
d.pop("b")
d


dict((["a", 1],["b", 2]))

dict(map(None, "abc", range(2)))
{a}




对于大字典，keys(),values(),items()构造同样巨大列表
建议迭代器





s = set("abc")
>>>s
set(['a','c','b'])


{v for v in "abc"}
set([])


>>>"b" in s
True










命名规则

  必须以字母或下划线开头，且只能是下划线，字母和数字
  不能喝语言保留字相同
  名字区分大小
  模块中以下划线开头的名字视为私有
  以双下划线开头的类成员名字视为私有
  单一下划线代表最后表达式的返回值


  s = set("abc")
  s.pop()
  'a'



   x = 1
   print "+" if x > 0 else ("-" if x < 0 else "0")

   print "+" if x >0 else

   x = 1
   print (x > 0 and "+") or (x < 0 and "-") or "0"


   if (x = 1) > 0: pass


   for i in xrange(3): print i


   for k, v in {"a":1,"b":2}.items(): print k, v


	


函数


typedef struct {
 PyObject_HEAD
 PyOjbect *func_code;
 PyOjbect *func_globals;
 PyObject *func_defaults;
 PyObject *func_closure;
 PyObject *func_doc;


} PyFunctionObject;


创建

 名字空间中，名字是唯一的主键
 函数总是有返回值，没有return
 支持递归调用,但进行尾递归优化

 def test(name):
	 if name == "a":
	    def a(): pass
		return a
	else:
		 def b(): pass
		 return b

test("a").__name__


add = lambda x,y = 0: x + y
add(1,2)
3

add(3)
3

def test(a, b):
	print a, b

test(b = "x", a= 100)


def test(x, ints = []):
	ints.append(x)
	return ints

test(1)
[1]


test(2)
[1, 2]

test(1,[])
[1]

test(3)
[1, 2, 3]


def test(a, b, *args, **kwargs):
	print a, b
	print args
	print kwargs


名字查找顺序: locals -> enclosing function -> globals -> __builtins__

locals: 函数内部名字空间，包括局部变量和形参

enclosing function:   外部嵌套函数的名字空间

globals              函数定义在模块名字空间

__builitins__:       内置模块的名字空间


引入__builtins__ 名字空间





闭包


def test():
	x = [1, 2]
	print hex(id(x))


	def a():
		x.append(3)
		print hex(id(x))

	def b():
		print hex(id(x)),x

	return a, b

a, b = test()
0x10

a()
ox10

b()
ox10 [1,2,3]


func_code

    co_cellvars:内部函数引用的名字列表
	co_freevars：当前函数引用外部的名字列表




堆栈


typedef struct _frame {

	   PyObject_VAR_HEAD
	   struct _frame *f_back;
	   PyCodeObject  *f_code;
	   PyObject      *f_builtins;
	   PyObject      *f_globals;
	   Pyobject      *f_locals;
	   PyObject     **f_valuestack;


}


迭代器


 __iter__() 和 next()两个方法 前者是迭代对象

class Data(obejct):
	def __init__(self):
		self._data = []
	
	def add(self, x):
		self._data.append(x)
	
	def data(self):
		return iter(self._data)

d = Data()

d.add(1)
d.add(2)

 迭代器返回self._data




class Data(object):
	def _init__(self, *args):
		self._data = lst(args)

	def __iter_(self):
		return DataIter(self)




class Data(object):
	def __init__(self, *args):
		self._data = list(args)

	def __iter__(self):
		for x in self._data:
		yield x

d = Data(1 2, 3)


模式 

   善用迭代器，





第6章模块

__name__:模块名<package><module>
__file__:模块完整文件名
__dict__:模块globals 名字空间



import sys, types

m = types.ModuleType("sample", "sample module")
m
<module 'sample' (built-in)>

m.__dict__
{'__name__':'sample','__doc__':'sample module'}

sample in sys.modules


模块动态添加函数成员,函数

def test(): print "test:", __name__

test()

test: __main__

m.test = test
m.test()


搜索路径

虚拟机按一下顺序搜索模块

 当前进程根目录
 PYTHONPATH环境变量指定的路径列表
 Python 标准库目录列表
 路径文件(.pth)

 虚拟机顺序匹配一下目标模块

 py源代码
 pyc字节码
 egg包文件或目录
 so,dll,pyd 等扩展文件
 内置模块
 其他

获取模块文件信息

 import imp
 imp.find_modle("os")

 
 import 不会导入 ____



 __all__






 __iport__

 __all__


 __path__




类

  有两种类模型

  但继承在Python 对应 New-Style Class
                      ClassicClass

   Python3 保留了 New-Sytle Class
   2.x 默认是 classic Class


   
class User: pass


type(User)
<type 'classobj'>

issubclass(User, object)  显然不是从object 继承
False

__metaclass__ = type    指定默认元类

class Manager: pass    没有object继承

type(Manager)          已经是New-Style Class
<type 'type'>


issubclass(Manager, object)  
True



名字空间


typedef struct 
{
  PyObject_HEAD
  PyObject *cl_bases;
  PyObject *cl_dict;
  PyObject *cl_name;

  PyObject *cl_getattr;
  PyObject *cl_setattr;
  PyObjcct *cl_delattr;

} PyClassObject;


class User(object): pass
u = User()

type(u)
<class '__main__.User'>

u.__class__
<class '__main__.User'>

typedef struct 
{
   PyObeject_HEAD
   PyClassObject    *in_class;
   PyObject         *in_dict;
   PYObject         *in_weakreflist;
} PyInstanceObject;

User.__dict__


u.__dict__






instance.__dict__  -> class.__dict__ -> baseclass.__dict__



字段


 字段(Field) 和 属性(Property)


	 实例字段在instance.__dict__
	 静态字段在class.__dict__
	 必须通过类型和实例对象才访问字段

双下划线的class和 instance成员视为私有

class User(object):
	table = "t_user"
	def __init__(self, name, age):
		self.name = name
		self.age = age

u1 = User("user1", 20)
u1.__dict__


u2 = User("user2", 30)
u2.__dict__

for k,v in User.__dict__.items():
	print 


User.table
't_user'

u1.table
't_user'

u2.table
't_user'




class User(object):
	__table = "t_user"


	def __init__(self, name, age):
		self.__name = name
		seff.__age = age

	def __str__(self):
		return "{0}".format(
				self.__table,
				self.__name,
				self.__age
				)

 u = User("tom", 20)

 u.__dict__


 str(u)
 't_user: tom, 20'

 User.__dict__.keys()
 ['_User__table',..]


 属性 getter setter deleter 几个方法

 class User(object):
	 @property
	  def name(self): return self.__name
	 @name.setter
	  def name(self, value): self.__name = value

	@name.deleter
	def name(self): del self.__name

u = User()
u.name = "Tom"

u.__dict__
{}



class User(object):
	def __init__(self uid):
		self._uid = uid


		uid = property(lambda o: o._uid)
	  
	    name = property(lambda 0: o.__name,\
				lambda o, v: setattr(o, "_name", v))

u = User(1)

u.name = "Tom"
u.__dict__


{"_uid" : 1, "_name" : 'Tom'}


u.__dict__["uid"] = 10000
u.__dict__["name"] = "xxxx"






方法

class User(object):
	def pirnt_id(slef):
		print hex(id(self))

u = User()

u.print_id()


class User(object):
	def a(): pass

	@staticmethod
	def b(): pass

	@classmethod
	def c(cls): pass

User.a




__new__: 创建对象实例
__init__:  初始化对象状态
__del__:   对象回收前被调用




继承

class User(object):
	table = "t_user"


	def __init__(self, name, age):
		self._name = name
		self._age = age
	
	def test(self):
		print self._name, self._age

class Manager(User):
	table = "t_manager"

	def __init__(self, name ,age , title):
		User.__init__(self, name, age)
		self._title = title
	
	def kill(self):
		print "213...."

m = Manager("Tom", 40 , "CX0")

m.__dict__




User.__subclasses__()

issubclass(Manager, User)
True

issubclass(Manager, object)
True

isinstance(m, Manager)
True

isinstance(m, object)
True


class User(object):
	def abc(self):
		print "User.abc"

class Manager(User):
	@staticmethod
	def abc():
		print "Manager.static.abc"

	def test(self):
		self.abc()
		User.abc(self)

Manager().test()





多重继承

class A(objet):
	def __init__(self, a):
		self._a = a

class B(object):
	def __init__(self, b):
		self._b = b

class C(A, B):
	def __init__(self, a ,b):
		A.__init__(self, a)
	    B.__init__(self, b)

C.__bases__


(<class '__main__.A')


c = C(1, 2)


c.__dict__
{'_b':2, '_a' : 1}


issubclass(C, A), isinstance(c , A)
(True, True)

issubclass(C, B), isinstance(c, B)
(True, True)


C.mro()

C.__mro__


super()

class A(object):
	def a(self): print "a"
	
class B(object):
	def b(self): print "b"


class C()



抽象类(Abstract Class)无法实例法


from abc import ABCMeta, abstractmethod, abstractproperty

class User(object):
	__metaclass__ = ABCMeta


	def __init__(self, uid):
         self._uid = uid

	@abstractmethod
	def print_id(self): pass

	name = abstractproperty()

class Manager(User):
	def __init__(self, uid):
		User.__init__(self, uid)

	def print_id(self):





Python 正则表达式

\d
\D
\s
\S
\w
\W
|
^
$
\b
\B
*
?
+


正则函数

re有几个重要的函数:
 
 match(): 匹配字符串开始位置

 search(): 扫描字符串，找到第一个位置

 findall():全部匹配，以列表返回

 finditer():找到全部匹配,迭代器返回




MatchObject

group():
start():
end():
span():
groups():
groupdict():
