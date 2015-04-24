
MyISAM

  .myd文件  表数据文件

  .myi文件  MY Index 索引文件

  .log文件  日志文件

Innodb
     ibdata1 ibdata2 存储了系统信息，用户数据

和索引

文件系统中,myd,myd,myi,ibd

Mysql Type

http://dev.mysql.com/doc/refman/5.6/en/numeric-type-overview.html


Socket 文件

Pid文件

Mysql表结构文件:


存储引擎文件:



Mysql实例启动时,读取配置参数文件my.cnf

 寻找my.cnf位置 

         （1）：默认情况： mysql--help|grep my.cnf

         （2）：后台进程去找：ps–eaf|grep mysql 

         （3）：全局搜索：find /-name my.cnf   

Ø  可以用vim修改里面的参数值 

         （1）dynamic ：可以通过set进行实时修改   

         （2）static，只能在my.cnf里面修改，需要restart生效 


二进制日志、慢查询日志、全查询日志、redo日志、undo日志


show variables like 'log_error';


show variables like 'long_query_time;


二进制日志




mysql binlog3种格式，row,mixed,statement. 解析工作


--base64-output=DECODE-ROWS