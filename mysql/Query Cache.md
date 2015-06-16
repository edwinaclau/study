mysql> show variables like '%cache%';  
02.+------------------------------+----------------------+  
03.| Variable_name                | Value                |  
04.+------------------------------+----------------------+  
05.| binlog_cache_size            | 32768                |  
06.| binlog_stmt_cache_size       | 32768                |  
07.| have_query_cache             | YES                  |  
08.| key_cache_age_threshold      | 300                  |  
09.| key_cache_block_size         | 1024                 |  
10.| key_cache_division_limit     | 100                  |  
11.| max_binlog_cache_size        | 18446744073709547520 |  
12.| max_binlog_stmt_cache_size   | 18446744073709547520 |  
13.| metadata_locks_cache_size    | 1024                 |  
14.| query_cache_limit            | 1048576              |  
15.| query_cache_min_res_unit     | 4096                 |  
16.| query_cache_size             | 33554432             |  
17.| query_cache_type             | ON                   |  
18.| query_cache_wlock_invalidate | OFF                  |  
19.| stored_program_cache         | 256                  |  
20.| table_definition_cache       | 400                  |  
21.| table_open_cache             | 512                  |  
22.| thread_cache_size            | 8                    |  
23.+------------------------------+----------------------+  
24.18 rows in set (0.00 sec)  
25.  
26.  
27.mysql>  




Qcache_free_blocks  剩下多少blocks

写过内存池同学都懂

Qcache_free_memory: Query Cache

目前剩余多少内存大小


Qcache_hits 命中

Qcache_inserts



Qcache_lowmem_prunes 内存不足被清除Query Cache

Qcache_not_cached 

Qcache_queries_in_cache

Qcache_total_blocks 当前Query Cache 中的block 数量

