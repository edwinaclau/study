RDB 最核心的是 rdbSave 和 rdbLoad 两个函数， 前者用于生成 RDB 文件到磁盘， 而后者则用于将 RDB 文件中的数据重新载入到内存中：


SAVE 和 BGSAVE 两个命令都会调用 rdbSave 函数，但它们调用的方式各有不同：

SAVE 直接调用 rdbSave ，阻塞 Redis 主进程，直到保存完成为止。在主进程阻塞期间，服务器不能处理客户端的任何请求。
BGSAVE 则 fork 出一个子进程，子进程负责调用 rdbSave ，并在保存完成之后向主进程发送信号，通知保存已完成。因为 rdbSave 在子进程被调用，所以 Redis 服务器在 BGSAVE 执行期间仍然可以继续处理客户端的请求。


触发rdbSave过程，主要有4种方式： 
1. SAVE命令 
2. BGSAVE命令 
3. master接收到slave发来的sync命令 
4. 定时save(配置文件中制定） 


RDB文件格式比较简单，可以看做是一条条指令序列，每条指令的组成：





 REDIS | RDB-VERSION | SELECT-DB | KEY-VALUE-PAIRS | EOF | CHECK-SUM |


REDIS

文件的最开头保存着 REDIS 五个字符，标识着一个 RDB 文件的开始。

在读入文件的时候，程序可以通过检查一个文件的前五个字节，来快速地判断该文件是否有可能是 RDB 文件。

RDB-VERSION

一个四字节长的以字符表示的整数，记录了该文件所使用的 RDB 版本号。

目前的 RDB 文件版本为 0006 。

因为不同版本的 RDB 文件互不兼容，所以在读入程序时，需要根据版本来选择不同的读入方式。

DB-DATA

这个部分在一个 RDB 文件中会出现任意多次，每个 DB-DATA 部分保存着服务器上一个非空数据库的所有数据。

SELECT-DB

这域保存着跟在后面的键值对所属的数据库号码。

在读入 RDB 文件时，程序会根据这个域的值来切换数据库，确保数据被还原到正确的数据库上。

KEY-VALUE-PAIRS

因为空的数据库不会被保存到 RDB 文件，所以这个部分至少会包含一个键值对的数据。

每个键值对的数据使用以下结构来保存：


| OPTIONAL-EXPIRE-TIME | TYPE-OF-VALUE | KEY | VALUE 