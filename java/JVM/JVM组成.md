JVM由4大部分组成：ClassLoader，Runtime Data Area，Execution Engine，Native Interface


2.1.ClassLoader是负责加载class文件，class文件在文件开头有特定的文件标示，并且ClassLoader只负责class文件的加载，至于它是否可以运行，则由Execution Engine决定。

2.2.Native Interface是负责调用本地接口的。他的作用是调用不同语言的接口给JAVA用，他会在Native Method Stack中记录对应的本地方法，然后调用该方法时就通过Execution Engine加载对应的本地lib。原本多于用一些专业领域，如JAVA驱动，地图制作引擎等，现在关于这种本地方法接口的调用已经被类似于Socket通信，WebService等方式取代。

2.3.Execution Engine是执行引擎，也叫Interpreter。Class文件被加载后，会把指令和数据信息放入内存中，Execution Engine则负责把这些命令解释给操作系统。

2.4.Runtime Data Area则是存放数据的，分为五部分：Stack，Heap，Method Area，PC Register，Native Method Stack。几乎所有的关于java内存方面的问题，都是集中在这块。下图是javapapers.com上关于Run-time Data Areas的描述：


Stack是java栈内存，它等价于C语言中的栈，栈的内存地址是不连续的，每个线程都拥有自己的栈。栈里面存储着的是StackFrame，在《JVM Specification》中文版中被译作java虚拟机框架，也叫做栈帧。StackFrame包含三类信息：局部变量，执行环境，操作数栈。局部变量用来存储一个类的方法中所用到的局部变量。执行环境用于保存解析器对于java字节码进行解释过程中需要的信息，包括：上次调用的方法、局部变量指针和操作数栈的栈顶和栈底指针。操作数栈用于存储运算所需要的操作数和结果。StackFrame在方法被调用时创建，在某个线程中，某个时间点上，只有一个框架是活跃的，该框架被称为Current Frame，而框架中的方法被称为Current Method，其中定义的类为Current Class。局部变量和操作数栈上的操作总是引用当前框架。当Stack Frame中方法被执行完之后，或者调用别的StackFrame中的方法时，则当前栈变为另外一个StackFrame。Stack的大小是由两种类型，固定和动态的，动态类型的栈可以按照线程的需要分配。













3.垃圾回收

JVM中对于被标记为垃圾的对象进行回收时又分为了一下3种算法：

1.标记清除算法，该算法是从根集合扫描整个空间，标记存活的对象，然后在扫描整个空间对没有被标记的对象进行回收，这种算法在存活对象较多时比较高效，但会产生内存碎片。

2.复制算法，该算法是从根集合扫描，并将存活的对象复制到新的空间，这种算法在存活对象少时比较高效。

3.标记整理算法，标记整理算法和标记清除算法一样都会扫描并标记存活对象，在回收未标记对象的同时会整理被标记的对象，解决了内存碎片的问题。

JVM中，不同的 内存区域作用和性质不一样，使用的垃圾回收算法也不一样，所以JVM中又定义了几种不同的垃圾回收器（图中连线代表两个回收器可以同时使用）：


1.Serial GC。从名字上看，串行GC意味着是一种单线程的，所以它要求收集的时候所有的线程暂停。这对于高性能的应用是不合理的，所以串行GC一般用于Client模式的JVM中。

2.ParNew GC。是在SerialGC的基础上，增加了多线程机制。但是如果机器是单CPU的，这种收集器是比SerialGC效率低的。

3.Parrallel Scavenge GC。这种收集器又叫吞吐量优先收集器，而吞吐量=程序运行时间/(JVM执行回收的时间+程序运行时间),假设程序运行了100分钟，JVM的垃圾回收占用1分钟，那么吞吐量就是99%。Parallel Scavenge GC由于可以提供比较不错的吞吐量，所以被作为了server模式JVM的默认配置。

4.ParallelOld是老生代并行收集器的一种，使用了标记整理算法，是JDK1.6中引进的，在之前老生代只能使用串行回收收集器。

5.Serial Old是老生代client模式下的默认收集器，单线程执行，同时也作为CMS收集器失败后的备用收集器。

6.CMS又称响应时间优先回收器，使用标记清除算法。他的回收线程数为(CPU核心数+3)/4，所以当CPU核心数为2时比较高效些。CMS分为4个过程：初始标记、并发标记、重新标记、并发清除。

7.GarbageFirst（G1）。比较特殊的是G1回收器既可以回收Young Generation，也可以回收Tenured Generation。它是在JDK6的某个版本中才引入的，性能比较高，同时注意了吞吐量和响应时间。
