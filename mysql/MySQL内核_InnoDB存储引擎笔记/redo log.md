
日志缓冲(redo log buffer)

 redo log 用来保证事务的持久性

 undo log 帮助文件进行读取

 undo log 需要进行随机进行读/行



MySQL 

 两种日志记录， 

binlog 

  T1 T4 T3 T2 T8 T6 T7 T5
  
  T1 T2 T1 *T2 T3 T1 T3 T1

物理逻辑日志
  重做日志