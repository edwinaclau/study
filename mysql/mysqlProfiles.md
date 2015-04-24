mysql> show profiles;

set profiling=1; //打开

mysql> show variables like '%pro%';
+---------------------------+-------+
| Variable_name             | Value |
+---------------------------+-------+
| have_profiling            | YES   |
| profiling                 | ON    |
| profiling_history_size    | 15    |
| protocol_version          | 10    |
| proxy_user                |       |
| slave_compressed_protocol | OFF   |


drop table bike_shop;

显示profiles 结果

show profiles;

检查

show profile for query 3;

profiling_history_size


 if profiling is enabled. The default value is 15. The maximum value is 100. Setting the value to 0 effectively disables profiling