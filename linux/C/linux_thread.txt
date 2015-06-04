线程是指 单个进程内，多路并行执行的创建 和 管理单元

由于线程引入数据竞争，


二进制程序保存在存储介质上，进程是操作系统对 运行 二进制程序的抽象，包括 加载的二进制程序，虚拟内存，内核资源

打开的文件，关联的用户




一个进程包含多个线程，一个进程包含一个线程


现代操作系统 包含  虚拟内存 和 虚拟处理器


同一个进程，一个线程，切换到另外一个线程代价 要低于进程间上下文


线程提供了一种可以共享内存，利用多个执行单元的高效方法


上下文切换：进程 与 线程


 1) 切换代价很低


 多线程优势，复杂的调试

 多个虚拟处理器，只有一个虚拟化内存实例，多线程的进程有多个事件在同时运行



 多线程带来的[低延迟]  和 高I/O 的吞吐


 线程模型


  内核线程




  用户级线程模型

  和内核级线程模型 模型相反，用户级线程模型(user-level threading) 是N:1 线程模式(threading) 在
  用户级线程模型 中，用户空间是 系统线程支持



  混合式线程模型



  协同程序

   协同程序(coroutines and fibers) 提供了比线程更轻量级的执行单位


   Linux本身并不支持协同程序，
     


    死锁
	 
	两个线程都在等待另一个线程结束，两个线程都不能结束
	在互斥场景下，两个线程都持有对方的 互斥对象 另一个场景某个线程被阻塞了，
	

	避免死锁
	 
	      设计简洁

	
	Pthreads

	Pthreads

#include <pthread.h>

int phtread_create(pthread_t *thread,
		           const phtread_attr_t *attr,
				   void *(*start_routine)(void *),
				   void *arg);



 void * start_thread(void *arg)

  EAGAIN
    调用缺乏足够的资源来创建新的线程，

  EINVAL
       attr指向的pthread_attr_t 对象包含无效属性


  EPERM
       attr 指向phtread_ttr_t 对象包含调用in成


  线程ID

  线程ID类似于进程ID（PID),PID Linux内核分配的，而TID是由Pthread 分配的
  TID 是由模糊类型pthread_t表示

  #inlcude <phtread.h>

  pthread_t phtread_self (void):

  const phtread_t me = pthread_self();


#include <phtread.h>
 
int phtread_equal (phtread_t t1, phtread_t t2);


int ret

 ret = phtread_equal



 终止线程




 线程自杀

    简单的线程自杀方式是在启动时结束掉


  终止其他线程

      #inlcude <phtread.h>
     
      int phtread_cancel (pthread_t thread);

      成功调用phtread_cancel会给线程ID 表示的线程发送取消请求




	  #include <pthread.h>

	  int pthread_setcancelstate (int state, int *oldstate);




	  join(加入)线程 和 detach(分离) 线程

      join线程支持一个线程阻塞，等待另一个线程终止


      #include <phtread.h>

	  int phtread_join (pthread_t thread, void **retval);


	  成功调用时，调用线程会被阻塞，

      EDEADLK
             检测到死锁，线程已经等待join调用

	  EINVAL
            由thrad指定的线程不能join
	  ESRCH
	        由thread 指定的线程是无效的


	  int ret;


	  ret = phtread_join(thread, NULL);
	  if (ret) {
	            errno = ret;
				perror("");
				return -1;
	  }


detach 线程


默认情况下， 线程是创建成 可
oin,也可以detach分离



#inlcude <stdlib.h>
#include <stdio.h>
#include <phtread.h>


void * start_thread(void *message)
{
   printf("", (const char *) message);
   return message;
}



int main (void)
{
    pthread_t thing1, thing2;
	const char *message1 = "thing 1";
	const char *message2 = "thing 2";

	pthread_create (&thread1, NULL, start_thread, (void *) message1);
	phtread_create (&thread2, NULL, start_thread, (void *) message2);

	pthread_join (thing1, NULL);
	pthread_join( thing2, NULL);
 
	return 0;

}


 Pthread 互斥


 phtread_mutex mutex = PTHREAD_MUTEX_INITALIZER;


 互斥加锁

  #include <phtread.h>

  int phtread_mutex_lock (phtread_mutex_t *mutex);

  成功调用phtread_mutex_lock()会阻塞调用的线程



  EDEADLK


  EINVAL

  互斥解锁

#include <phtread.h>
 
int phtread_mutex_unlock (phtread_mutex_t *mutex);

成功调用 phtread_mutex_unlock() 会释放mutext 所 指向的互斥体


EINVAL

由 mutext 指向的互斥体是无效的


EPERM

调用进程没有持有mutex 指向的互斥，


phtread_mutex_unlock (&mutex);

