Redis持久化有RDB和AOF两种方式，而针对AOF有appendonly和rewrite两种方式。

redis通过multi、discard、watch、exec实现数据库事务操作

客户端[发送命令]--->服务器--->保存被执行命令--->[AOF文件]


打开appendonly标志时，数据库服务器执行的每条命令都会添加到aof_buf中，feedAppendOnlyFile函数进行该动作。该函数执行的动作如下：
若当前命令的数据库与aof数据不同，则先添加SELECT命令，然后再按照Redis协议写入命令。



利用aof rewrite_buf可以有效的减少数据库持久化文件大小。AOF基本流程如下所示：
fork子进程把当前数据库状况写入AOF文件，期间禁用数据库rehash操作（防止大量的内存页写，导致数据库占用内存高，因为父进程大量写时，子进程会复制父进程的页）。
在子进程写AOF文件过程中，所有对父进程的操作都会添加到rewrite_buf中；该buf总大小近似为 (buf数 - 1) * 10MB + 最后一个rewrite_buf->used，填充时总是填充满最后一个buf未用完的空间，再分配下一个rewrite_buf（每个rewrite_buf都为10MB）。
后台子进程AOF完成后，在服务器serverCron过程中，检测到子进程结束事件，根据进程是否正常结束进行下述操作：
正常结束，将rewrite_buf追加到临时AOF文件中，进行AOF文件同步，打开REDIS_AOF_ON标志（这意味着后续的操作将写入aof_buf中），同时删除旧的（若有）aof_filename，将临时aof文件重命名为aof_filename；
非正常结束，重新调度，状态转为REDIS_AOF_WAIT_REWRITE，下次进入serverCron时重新开始AOF基本流程。



