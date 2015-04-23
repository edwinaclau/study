Python 单继承对应new style class

非 Class class



typedef struct {
    PyObject_HEAD
    PyObject    *cl_bases;  /* A tuple of class objects */
    PyObject    *cl_dict;   /* A dictionary */
    PyObject    *cl_name;   /* A string */
    /* The following three are functions or NULL */
    PyObject    *cl_getattr;
    PyObject    *cl_setattr;
    PyObject    *cl_delattr;
    PyObject    *cl_weakreflist; /* List of weak references */
} PyClassObject;



typedef struct
{
  PyObject_HEAD
  PyClassobject  *in_class;
  PyObject       *in_dict;
  PyObject       *in_weakreflist;
} PyInstanceObject;



instance.__dict__    => class.__dict__ =? baseclass.__dict__




字段


instnace__dict__

class__dict__

双下划线成员是私有


class User(object):
   table = "t_user"

  def __init__(self, name, age):
             self.name = name
             self.age = age

for k,v in User.__dict__.items():



属性 getter setter deleter






lambda 


class User(object):
        def __init__(self, uid):
             self._uid  = uid

        uid = property(lambda o: o._uid)

        name = property(lambda o, v: seattr(0,"_name", v))

u = User(1)

u.uid





__new__ : 创建对象实例

__init__ : 初始化对象状态

__del__ 对象回收调用


class User(object):
     def __new__(cls, *args, **kwargs):
           


     def __init__(self, name, age):



     def __del__(self):
            print "__del__"


所有方法都存储在class.__dict__
不可能重载




除了基类的实例字段在instance.__dict__





class User(object)

   def aa():pass

   @staticmethod
   def bb():pass


   @classmethod
   def cc(): pass


User.aa

unbound method User.a


User.bb


User.c


特殊方法

  __new__

  __init__

  __del__


class User(object):
        def __new__(cls, *args,**kwargs):
               print   "__new__", cls, args, kwargs
         return object.__new__(cls)

        def __init__(self, name, age):
              print "__init__", name ,age

        def __del__(self):
              print "__del__"

u = user("Tom", 23)




继承 

class User(object):  

     table = "t_user"

   def __init__(self, name, age):
           self._name = name
           self._age = age

   def test(self):
       pirnt self._name, self._age

class Manager(User):
        table = "t_manager"

def __init__(self, name ,age , title):
         User.__init__(self, name ,age)
         self._title = title

def killer(self):
        print "21"


m = Manger("tom", 40, "CXO")

m.__dict__

实例包含所有基类字段


for k, v in Manager.__dict__.items():
     print "{0:5} = {1}".format(k,v)

派生类名字空间没有基类成员



基类引用存储在__base__,直接派生类存储在__subclasses__

用issubclass()继承,isinstanceof()判断实例对象



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





抽象类

Abstract Class


from abc import ABCMeta, abstractmethod, abstractproperty



class User(object): 
    __metaclass__ = ABCMeta

def __init__(self, uid):
 


setattr 和 delattr直接操作实例和类型的名字空间


class User(object):pass

u = User()

setattr(u, "name","tom")



__slots__

class User(object):
         __slots__ = ("__name","_age")

def __init__(self, name ,age):
          self._name = name
          self._age = age

u = User("tom",34)
hasattr(u,"__dict__")
False





__setitem__

class A(object)
          def __init__(self, **kwargs)
                self.__data = kwargs
 
          def __getitem__(self, key):
                return self._data.get(key)

          def __setitem__(self, key, value):
                self._data[key] = value


    def __delitem__(self, key):
             self._data.pop(key,None)

    def __contains__(self, key):
            return key in self._data.keys()

a = A(x=1,y=2)



