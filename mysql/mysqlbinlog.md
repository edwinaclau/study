###Mysql二进制日志
和二进制日志相关的参数：

max_binlog_size、binlog_cache_size、sync_binlog、binlog-do-db、binlog-ignore-db、log-slave-update、binlog_format


--log-bin[=filename]


STATEMENT

每一条造成数据库影响都将SQL记录在内
从库(slave)

ROW



MIDXED



二.PURGE MASTER LOGS
语法
PURGE {MASTER | BINARY} LOGS TO 'log_name'   --用于删除指定的日志
PURGE {MASTER | BINARY} LOGS BEFORE 'date'  --用于删除日期之前的日志，BEFORE变量的date自变量可以为'YYYY-MM-DD hh:mm:ss'格式
如：（MASTER 和BINARY 在这里都是等效的）
PURGE MASTER LOGS TO 'test-bin.000001';   
PURGE MASTER LOGS BEFORE '2011-01-0100:00:00';


 flush logs;