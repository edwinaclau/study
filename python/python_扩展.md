PyObject* pInt = Py_BuildValue("i", 2003);

PyObject* pFloat = Py_BuildValue('f', 3.14f);

PyObject* pString = Py_BuildValue("s", "Python");

PyObject* pTuple = PyTuple_New(3);


PyObject* pList = PyList_New(3);

for (int i = 0; i < 3; i++)
       PyList_SetItem(pList, i , Py_BuildValue("i", i));


PyObject* pDict = PyDict_New();

PyDict_setItemString(pDict, "first", Py_buildValue("i", 2003));

PyDict_setItemString(pDict, "second",Py_buildValue("f", 3.14f));

PyObject* pKeys = PyDict_keys();

int fact(int n) {
     if (n <= 1)
		 return 1:
	else
		 return n * fact(n - 1);
}

#include <Python.h>

PyObject* wrap_fact(PyObject*self, PyObject* )
      int n, result:
	  if (! PyArg_ParseTuple(args, "i:fact", &n))
	     return NULL;
	  result = fact(n);
	  return Py_BuildValue("i", result);}

static PyMethodDef exampleMethods[] = {

}

void init example() {
  PyObject* m; 
  m = Py_initModule("example", exampleMethods);
}


PyObject* method(PyObject* self, PyObject* args):

PyObject* method(PyObject *self, PyObject *args) {
   Py_INCREF(Py_None);
}

PyObject* method(PyObject* self, PyObject* args);


PyObject* method(PyObject *self, PyObject *args) { Py_INCREF(Py_None)};


static PyMethodDef exampleMethods[]



static PyObject *MyFunction( PyObject *self, PyObject *args);

static PyObject *MyFunctionWithKeywords(PyObbject *self,
		                PyObject *args,
						PyObject *kw);



static PyObject *MyFunctionWithArgs( PyObject *self);

static PyObject *module_func(PyObject *self, PyObject *args) {
       Py_RETURN_NONE;
}





static PyMethodDef {
    char *ml_name;
	PyCFunction ml_metch;
	int ml_flags;
	char *ml_doc;
};


ml_name  函数名称

ml_meth

ml_falgs


static PyMethod module_methods[] = {

}



博客 – 伯乐在线
高性能的Python扩展（1）
分享到： 0
Android面试常客Handler详解
见证Android消息推送时刻
Android中的WebView实战详解
Android智能机器人“小慕”的实现
本文由 伯乐在线 - Janzou 翻译。未经许可，禁止转载！
英文出处：J. David Lee。欢迎加入翻译小组。
简介

通常来说，Python不是一种高性能的语言，在某种意义上，这种说法是真的。但是，随着以Numpy为中心的数学和科学软件包的生态圈的发展，达到合理的性能不会太困难。

当性能成为问题时，运行时间通常由几个函数决定。用C重写这些函数，通常能极大的提升性能。

在本系列的第一部分中，我们来看看如何使用NumPy的C API来编写C语言的Python扩展，以改善模型的性能。在以后的文章中，我们将在这里提出我们的解决方案，以进一步提升其性能。

文件

这篇文章中所涉及的文件可以在Github上获得。

模拟

作为这个练习的起点，我们将在像重力的力的作用下为N体来考虑二维N体的模拟。

以下是将用于存储我们世界的状态，以及一些临时变量的类。

# lib/sim.py
 
class World(object):
    
"""World is a structure that holds the state of N bodies and
    
additional variables.
 
    
threads : (int) The number of threads to use for multithreaded
              
implementations.
 
    
STATE OF THE WORLD: 
 
    
N : (int) The number of bodies in the simulation.
    
m : (1D ndarray) The mass of each body.
    
r : (2D ndarray) The position of each body.
    
v : (2D ndarray) The velocity of each body.
    
F : (2D ndarray) The force on each body.
 
    
TEMPORARY VARIABLES:
 
    
Ft : (3D ndarray) A 2D force array for each thread's local storage.
    
s  : (2D ndarray) The vectors from one body to all others. 
    
s3 : (1D ndarray) The norm of each s vector. 
 
    
NOTE: Ft is used by parallel algorithms for thread-local
          
storage. s and s3 are only used by the Python
          
implementation.
    
"""
    def __init__(self, N, threads=1, 
                 m_min=1, m_max=30.0, r_max=50.0, v_max=4.0, dt=1e-3):
        self.threads = threads
        self.N  = N
        self.m  = np.random.uniform(m_min, m_max, N)
        self.r  = np.random.uniform(-r_max, r_max, (N, 2))
        self.v  = np.random.uniform(-v_max, v_max, (N, 2))
        self.F  = np.zeros_like(self.r)
        self.Ft = np.zeros((threads, N, 2))
        self.s  = np.zeros_like(self.r)
        self.s3 = np.zeros_like(self.m)
        self.dt = dt
在开始模拟时，N体被随机分配质量m，位置r和速度v。对于每个时间步长，接下来的计算有：

合力F，每个体上的合力根据所有其他体的计算。
速度v，由于力的作用每个体的速度被改变。
位置R，由于速度每个体的位置被改变。
第一步是计算合力F，这将是我们的瓶颈。由于世界上存在的其他物体，单一物体上的力是所有作用力的总和。这导致复杂度为O（N^2）。速度v和位置r更新的复杂度都是O（N）。

如果你有兴趣，这篇维基百科的文章介绍了一些可以加快力的计算的近似方法。

纯Python

在纯Python中，使用NumPy数组是时间演变函数的一种实现方式，它为优化提供了一个起点，并涉及测试其他实现方式。

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
# lib/sim.py
 
def compute_F(w):
    
"""Compute the force on each body in the world, w."""
    for i in xrange(w.N):
        w.s[:] = w.r - w.r[i]
        w.s3[:] = (w.s[:,0]**2 + w.s[:,1]**2)**1.5
        w.s3[i] = 1.0 
# This makes the self-force zero.
        w.F[i] = (w.m[i] * w.m[:,None] * w.s / w.s3[:,None]).sum(0)
 
def evolve(w, steps):
    
"""Evolve the world, w, through the given number of steps."""
    for _ in xrange(steps):
        compute_F(w)
        w.v += w.F * w.dt / w.m[:,None]
        w.r += w.v * w.dt
合力计算的复杂度为O（N^2）的现象被NumPy的数组符号所掩盖。每个数组操作遍历数组元素。

可视化

这里是7个物体从随机初始状态开始演化的路径图：

State Machine Diagram

性能

为了实现这个基准，我们在项目目录下创建了一个脚本，包含如下内容：

1
2
3
import lib
w = lib.World(101)
lib.evolve(w, 4096)
我们使用cProfile模块来测试衡量这个脚本。

1
python -m cProfile -scum bench.py
前几行告诉我们，compute_F确实是我们的瓶颈，它占了超过99％的运行时间。

1
2
3
4
5
6
7
8
9
10
11
428710 function calls (428521 primitive calls) in 16.836 seconds
 
Ordered by: cumulative time
 
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    0.000    0.000   16.837   16.837 bench.py:2(<module>)
     1    0.062    0.062   16.756   16.756 sim.py:60(evolve)
  4096   15.551    0.004   16.693    0.004 sim.py:51(compute_F)
413696    1.142    0.000    1.142    0.000 {method 'sum' ...
     3    0.002    0.001    0.115    0.038 __init__.py:1(<module>)
   ...
在Intel i5台式机上有101体，这种实现能够通过每秒257个时间步长演化世界。

简单的C扩展 1

在本节中，我们将看到一个C扩展模块实现演化的功能。当看完这一节时，这可能帮助我们获得一个C文件的副本。文件src/simple1.c，可以在GitHub上获得。

关于NumPy的C API的其他文档，请参阅NumPy的参考。Python的C API的详细文档在这里。

样板

文件中的第一件事情是先声明演化函数。这将直接用于下面的方法列表。

static PyObject *evolve(PyObject *self, PyObject *args);
接下来是方法列表。

static PyMethodDef methods[] = {
   { "evolve", evolve, METH_VARARGS, "Doc string."},
   { NULL, NULL, 0, NULL } /* Sentinel */
};
这是为扩展模块的一个导出方法列表。这只有一个名为evolve方法。

样板的最后一部分是模块的初始化。
PyMODINIT_FUNC initsimple1(void) {
   (void) Py_InitModule("simple1", methods);
   import_array();
}



