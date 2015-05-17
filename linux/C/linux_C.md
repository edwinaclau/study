信号:

   SIGHUP 表示挂断

   SIGSTOP(进程停止)
  
   SIGKILL(进程关闭)


文件I/O

  内核会维护一个文件table,文件描述符(fds),其中有包含指向(inode)

文件描述符采用 int 

默认上线1024，负数不合法


每个进程都会有三个文件描述符 0 ,1 , 2
  sdtin   stdout  stderr


int open (const char *name, int flags)
int open (const char *name, int flags, mode_t mode);

flags O_RDONLY

      O_WRONLY
 
      O_RDWR


O_APPED

O_ASYNC

O_CLOEXEC

O_CREAT

O_DIRECT





新建文件的权限


两种open()系统调用


S_IR_WXU


S_IWUSR

S_IXUSR


S_IRGRP

S_IWGRP

S_IXGRP

S_IRWXO

S_IROTH

S_IXOTH

mode参数 和用户的文件创建 掩码(umask)

unsigned logn word;
ssize_r nr;

ssize_r read (int fd, void *buf, size_t len)

nr = read (fd, &word, sizeof (unsigned long));

if (n == -1)




非阻塞读

 read()没有数据可读会阻塞，


通过read(读文件)

