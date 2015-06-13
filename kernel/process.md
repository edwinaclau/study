Linux 内核使用 task_struct 数据结构来关联所有与进程有关的数据和结构，Linux 内核所有涉及到进程和程序的所有算法都是围绕该数据结构建立的，是内核中最重要的数据结构之一。该数据结构在内核文件 include/linux/sched.h 中定义，在Linux 3.8 的内核中，该数据结构足足有 380 行之多，在这里我不可能逐项去描述其表示的含义，本篇文章只关注该数据结构如何来组织和管理进程ID的。

进程ID类型
要想了解内核如何来组织和管理进程ID，先要知道进程ID的类型：

PID：这是 Linux 中在其命名空间中唯一标识进程而分配给它的一个号码，称做进程ID号，简称PID。在使用 fork 或 clone 系统调用时产生的进程均会由内核分配一个新的唯一的PID值。
TGID：在一个进程中，如果以CLONE_THREAD标志来调用clone建立的进程就是该进程的一个线程，它们处于一个线程组，该线程组的ID叫做TGID。处于相同的线程组中的所有进程都有相同的TGID；线程组组长的TGID与其PID相同；一个进程没有使用线程，则其TGID与PID也相同。
PGID：另外，独立的进程可以组成进程组（使用setpgrp系统调用），进程组可以简化向所有组内进程发送信号的操作，例如用管道连接的进程处在同一进程组内。进程组ID叫做PGID，进程组内的所有进程都有相同的PGID，等于该组组长的PID。
SID：几个进程组可以合并成一个会话组（使用setsid系统调用），可以用于终端程序设计。会话组中所有进程都有相同的SID。





全局ID：在内核本身和初始命名空间中唯一的ID，在系统启动期间开始的 init 进程即属于该初始命名空间。系统中每个进程都对应了该命名空间的一个PID，叫全局ID，保证在整个系统中唯一。
局部ID：对于属于某个特定的命名空间，它在其命名空间内分配的ID为局部ID，该ID也可以出现在其他的命名空间中。


struct task_struct {
    //...
    struct pid_link pids;
    //...
};

struct pid_link {
    struct hlist_node node;  
    struct pid *pid;          
};

struct pid {
    struct hlist_head tasks;        //指回 pid_link 的 node
    int nr;                       //PID
    struct hlist_node pid_chain;    //pid hash 散列表结点
};

进程状态


TASK_RUNNING


TASK_INTERRUPTIBLE


TASK_UNINTERRUPTLBLE

TASK_STOPPED

TASK_TRACED

EXIT_ZOMBIE

EXIT_DEAD

TASK_NONINTERACTIVE

TASK_DEAD



 本文主要参考了Understanding The LinuxKernel 和水木精华区的分析进程切换宏 switch_to 。感谢相关的作者！本文中有部分内容直接从上面提到的文章中重复，仅仅是为了方便大家阅读。本文中提到的所有内核代码可以到LinuxCross Reference上查阅。欢迎转载本文，转载请保留这份声明。
     本文仅讨论内核进程的切换，而不涉及进程的调度算法。详细讲了switch_to这个宏。
     文中涉及到的Linux内核源码，如没有特别指出，均指2.6.26版本的源码。

    首先简单提一下这个宏和函数的被调用关系：
    schedule() --> context_switch() --> switch_to --> __switch_to() 
    这里面，schedule是主调度函数，涉及到一些调度算法，这里不讨论。当schedule()需要暂停A进程的执行而继续B进程的执行时，就发生了进程之间的切换。进程切换主要有两部分：1、切换全局页表项；2、切换内核堆栈和硬件上下文。这个切换工作由context_switch()完成。其中switch_to和__switch_to()主要完成第二部分。更详细的，__switch_to()主要完成硬件上下文切换，switch_to主要完成内核堆栈切换。
      阅读switch_to时请注意：这是一个宏，不是函数，它的参数prev, next, last不是值拷贝，而是它的调用者context_switch()的局部变量。局部变量是通过%ebp寄存器来索引的，也就是通过n(%ebp)，n是编译时决定的，在不同的进程的同一段代码中，同一局部变量的n是相同的。有关局部变量如何索引的问题，可以参考这里和这里。在switch_to中，发生了堆栈的切换，即ebp发生了改变，所以要格外留意在任一时刻的局部变量属于哪一个进程。关于__switch_to()这个函数的调用，并不是通过普通的call来实现，而是直接jmp，函数参数也并不是通过堆栈来传递，而是通过寄存器来传递。
     在下文中提到一些局部变量和寄存器值，为了不引起混淆，在名字后面加上_X，表示是X进程的成员。如esp_A表示进程A的esp的值，prev_B，表示进程B中的prev变量，等等。


    switch_to切换主要有以下三部分：
进程切换
即esp的切换
由于从esp可以找到进程的描述符
硬件上下文切换
__switch_to()
以前通过x86硬件支持，现在使用软件切换
堆栈的切换
即ebp的切换
ebp是栈底指针，它确定了当前变量空间属于哪个进程
                          
     上面的四个步骤中，有三个是在switch_to宏中完成，硬件上下文切换由__switch_to()函数完成。

     下面来具体看switch_to从A进程切换到B进程的步骤。

step1:复制两个变量到寄存器：
    [prev] "a" (prev)
    [next] "d" (next)
    即:
    eax <== prev_A 或eax <==%p(%ebp_A)
    edx <== next_A 或edx <==%n(%ebp_A)
    这里prev和next都是A进程的局部变量。

step2:保存进程A的ebp和eflags
    pushfl
    pushl %ebp
    注意，因为现在esp还在A的堆栈中，所以这两个东西被保存到A进程的内核堆栈中。

step3:保存当前esp到A进程内核描述符中：
    "movl %%esp,%[prev_sp]/n/t"    /*save    ESP   */
    它可以表示成：prev_A->thread.sp <== esp_A
    在调用switch_to时，prev是指向A进程自己的进程描述符的。

step4:从next（进程B）的描述符中取出之前从B切换出去时保存的esp_B。
    "movl%[next_sp],%%esp/n/t" /* restore ESP */
    它可以表示成：esp_B<== next_A->thread.sp
    注意，在A进程中的next是指向B的进程描述符的。
    从这个时候开始，CPU当前执行的进程已经是B进程了，因为esp已经指向B的内核堆栈。但是，现在的ebp仍然指向A进程的内核堆栈，所以所有局部变量仍然是A中的局部变量，比如next实质上是%n(%ebp_A)，也就是next_A，即指向B的进程描述符。

step5:把标号为1的指令地址保存到A进程描述符的ip域：
    "movl $1f,%[prev_ip]/n/t"    /*save    EIP   */
    它可以表示成：prev_A->thread.ip<== %1f，当A进程下次被switch_to回来时，会从这条指令开始执行。具体方法看后面被切换回来的B的下一条指令。

step6:将返回地址保存到堆栈，然后调用__switch_to()函数，__switch_to()函数完成硬件上下文切换。
    "pushl %[next_ip]/n/t"    /*restore EIP   */
    "jmp __switch_to/n"    /* regparmcall  */
    这里，如果之前B也被switch_to出去过，那么[next_ip]里存的就是下面这个1f的标号，但如果进程B刚刚被创建，之前没有被switch_to出去过，那么[next_ip]里存的将是ret_ftom_fork（参看copy_thread()函数）。这就是这里为什么不用call__switch_to而用jmp，因为call会导致自动把下面这句话的地址(也就是1:)压栈，然后__switch_to()就必然只能ret到这里，而无法根据需要ret到ret_from_fork。
    另外请注意，这里__switch_to()返回时，将返回值prev_A又写入了%eax，这就使得在switch_to宏里面eax寄存器始终保存的是prev_A的内容，或者，更准确的说，是指向A进程描述符的“指针”。这是有用的，下面step8中将会看到。

step7:从__switch_to()返回后继续从1:标号后面开始执行，修改ebp到B的内核堆栈，恢复B的eflags：
    "popl %%ebp/n/t"       /* restore EBP   */    
    "popfl/n"           /* restore flags */
    如果从__switch_to()返回后从这里继续运行，那么说明在此之前B肯定被switch_to调出过，因此此前肯定备份了ebp_B和flags_B，这里执行恢复操作。
     注意，这时候ebp已经指向了B的内核堆栈，所以上面的prev,next等局部变量已经不是A进程堆栈中的了，而是B进程堆栈中的（B上次被切换出去之前也有这两个变量，所以代表B堆栈中prev、next的值了），因为prev == %p(%ebp_B)，而在B上次被切换出去之前，该位置保存的是B进程的描述符地址。如果这个时候就结束switch_to的话，在后面的代码中（即 context_switch()函数中switch_to之后的代码）的prev变量是指向B进程的，因此，进程B就不知道是从哪个进程切换回来。而从context_switch()中switch_to之后的代码中，我们看到finish_task_switch(this_rq(), prev)中需要知道之前是从哪个进程切换过来的，因此，我们必须想办法保存A进程的描述符到B的堆栈中，这就是last的作用。

step8:将eax写入last，以在B的堆栈中保存正确的prev信息。
    "=a" (last)  即 last_B <== %eax
    而从context_switch()中看到的调用switch_to的方法是：
    switch_to(prev, next, prev);
    所以，这里面的last实质上就是prev，因此在switch_to宏执行完之后，prev_B就是正确的A的进程描述符了。   
    这里，last的作用相当于把进程A堆栈中的A进程描述符地址复制到了进程B的堆栈中。

     至此，switch_to已经执行完成，A停止运行，而开始了B。在以后，可能在某一次调度中，进程A得到调度，就会出现switch_to(C, A)这样的调用，这时，A再次得到调度，得到调度后，A进程从context_switch()中switch_to后面的代码开始执行，这时候，它看到的prev_A将指向C的进程描述符。

     如果读者不是十分清楚这个过程，最好自己画一下堆栈的变化，注意，这里有两个堆栈，在这个过程中，有一个时期esp和ebp并不在同一个堆栈上，要格外注意这个时期里所有涉及堆栈的操作分别是在哪个堆栈上进行的。记住一个简单的原则即可，pop/push这样的操作，都是对esp所指向的堆栈进行的，这些操作同时也会改变esp本身，除此之外，其它关于变量的引用，都是对ebp所指向的堆栈进行的。
    

    下面我们从switch_to被调用的情况来看一下这个执行过程。

     这里，为了便于理解，我们首先忽略switch_to中的具体细节，仅仅把它当作一个普通的指令。对A进程来说，它始终没有感觉到自己被打断过，它认为自己一直是不间断执行的。switch_to这条“指令”，除了改变了A进程中的prev变量外，对A没有其它任何影响。在系统中任何进程看到的都是这个样子，所有进程都认为自己在不间断的独立运行。然而，实际上switch_to的执行并不是一瞬间完成的，switch_to执行花了很长很长的时间，但是，在执行完switch_to之后，这段时间被从A的记忆中抹除，所以A并没有觉察到自己被打断过。
     接着，我们再来看这个“神奇”的switch_to。switch_to是从A进程到B进程的过渡，我们可以认为在switch_to这个点上，A进程被切出，B进程被切入。但是，如果把粒度放小到switch_to里面的单个汇编语句，这个界限就不明显了。进入switch_to的宏里面之后，首先 pushfl和pushl ebp肯定仍然属于进程A，之后把esp指向了B的堆栈，严格的说，从此时开始的指令流都属于B进程了。但是，这个时候B进程还没有完全准备好继续运行，因为ebp、硬件上下文等内容还没有切换成B的，剩下的部分宏代码就是完成这些事情。
     另外需要格外强调的是，这部分代码是内核代码，它们跟用户代码不在同一个代码段，所有进程在内核态共用这一段内核代码。这里涉及到的所有堆栈都是内核堆栈，而不涉及用户堆栈。进程切换时需要的页表项的切换不是在这里面做的。

    我们现在再向“上“看，从一个高级语言程序员的角度看，内核态的东西就好比这里的switch_to一样，对高级语言程序员是透明的。高级语言程序员始终认为自己的进程在不间断连续执行，而调度点的语句以及调度点之后的整个过程对该程序是完全没有影响的。
 
关于内核进程切换就讲这么多吧。switch_to只是个普通的宏，但是却能实现进程的切换，很多人对此比较费解。为了正确的理解，大家需要注意：
      这些代码是所有进程共用的，代码本身不属于某一个特定的进程，所以判定当前在哪一个进程不是通过看执行的代码是哪个进程的，而是通过esp指向哪个进程的堆栈来判定的。所以，对于上面图中的切换点也可以这样理解，在这一点处，esp指向了其它进程的堆栈，当前进程即被挂起，等待若干时间，当esp指针再次指回这个进程的堆栈时，这个进程又重新开始运行。