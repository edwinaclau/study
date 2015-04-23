


#define PyObject_HEAD                   \  
    _PyObject_HEAD_EXTRA                \  
    Py_ssize_t ob_refcnt;               \  
    struct _typeobject *ob_type;  


typedef struct _typeobject {  
    PyObject_VAR_HEAD  
    const char *tp_name; /* For printing, in format "<module>.<name>" */  
    Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */  
  
    /* Methods to implement standard operations */  
  
    destructor tp_dealloc;  
    printfunc tp_print;  
    getattrfunc tp_getattr;  
    setattrfunc tp_setattr;  
    cmpfunc tp_compare;  
    reprfunc tp_repr;  
  
    /* Method suites for standard classes */  
  
    PyNumberMethods *tp_as_number;  
    PySequenceMethods *tp_as_sequence;  
    PyMappingMethods *tp_as_mapping;  
  
  ...  
    allocfunc tp_alloc;  
    newfunc tp_new;  
    freefunc tp_free; /* Low-level free-memory routine */  
    inquiry tp_is_gc; /* For PyObject_IS_GC */  
    PyObject *tp_bases;  
    PyObject *tp_mro; /* method resolution order */  
    PyObject *tp_cache;  
    PyObject *tp_subclasses;  
    PyObject *tp_weaklist;  
    destructor tp_del;  
  
...  
} PyTypeObject;  



PyObject 作为python的基类，PyObject* 指针能够指向派生类，而派生类中各个类对象对成员ob_type都有自己的解释（PyIntObject：PyInt_Type PyDictObject：PyDict_Type


ob_type依据类的类型构建了基本操作的回调函数，从而，基类指针指向派生类对象后调用的通用接口，如print函数，将被解释为具体派生类的print函数，例如；
PyObject *ppy = &pyintobj；
ppy -> ob_type -> tp_print     即为： pyintobj -> ob_type -> int_print

PyObject *ppy = &pydictobj；
ppy -> ob_type -> tp_print     即为： pyintobj -> ob_type -> dict_print

总结：多态，通过不同类对ob_type进行初始化，为通用函数接口注册相应的回调函数，即可实现了多态；