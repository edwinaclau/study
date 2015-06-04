AIGABRT  abort()

SIGALRM   alarm()

SIBBUS 硬件或对齐

SIGLD  子进程终止

SIGCONT 



SIGBUS 

当程序发生除了内存保护外的硬件




内存保护会产生SIGSEGV



SIGSEGV 


SIGCHLD
当进程终止或停止 ,内核会给进程的父进程发送此信号

SIGCONT


SIGFPE

SIGHUP 当会话终端开时，内核会发送给会话


SIGILL

当进程试图执行一个非法机器指令,内核发送该信号

SIGINT

SIGTTOU


SIGRG


基本信号管理

 #include <signal.h>
 sighandler_t signal (int signo, sighandler_t handler);


 singal调用成功


 SIG_DEL
  

 SIG_IGN



等待信号

signal()函数 返回该信号先前的操作


static void sigint_handler (int signo)
{
    printf("Caught SGINT")
	exit (EXIT_SUCCESS);
}


int main(void)
{
    if (signal (SIGINT, sigint_handler) == SIG_ERR) {
	     fprintf(stderr, "Cannot handle");
		 exit (EXIT_FAILURE);
	}
}




执行 和 继承

fork 创建子进程时，子进程继承父进程的所有信号处理。子进程会
从父进程拷贝为每个信号

 

                        继承的信号行为
信号行为            通过fork                      通过exec创建

忽略                 继承                         继承

默认                 继承                         继承


处理                 继承                         不继承

挂起信号             不继承                       继承

这个进程职位有个重要


shell 后台 执行一个进程时


extern const char * const sys_siglist[];

#define _GNU_SOURCE
#include <string.h>
 char *strsignal (int signo);



 int ret;

 ret = kill (1722, SIGHUP);
 if (ret)
	perror("kill");

kill -HUP 1722,



#inclde <singnal.h>
int raise (int signo);

kill (getpid (), signo);



给整个进程组发送信号

 kill (-pgrp, signo);




 重入

 abort()    accept()   access()

 aio_error()  aio_return() 


信号集

#include <signal.h>

int sigemptyset (sigset_t *set);


int sigfillset (sigeset_t *set, int signo);

int sigismember (const sigset_t *set, int signo);


更多的信号集函数

#define __GNU_SOURCE
#define <signal.h>

int sigisemptyset (sigset_t *set);

int sigorset(sigset_t *dest, sigset_t *left, sigset_t *right);

int sigandset (sigset_t *dest, sigset_t *left, sigset_t *right);

 sigorset() 将信号集left  和 right 的并集 赋给 dest 成功两者返回0
 出错将errno 设置为 EINVAL



  阻塞信号

   重入和由信号处理程序 异步 运行印发的问题

   POSIX定义，Linux 实现了一个管理进程号掩码的函数

   #include <signal.h>

   int sigprocmck(int how,
		          const sigset_t *set,
				  sigset_t *oldset);

 SIG_SETMASK


 SIG_BLOCK

 SIG_UNBLOCK

 获取等待处理信号

 POSIX 定义了一个函数，尅获取待处理信号集













挂起信号
