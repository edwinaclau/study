
http://dev.mysql.com/doc/refman/5.5/en/explain-output.html


一般都是没有索引(key 是null)

很多处理过行(rows)

很多possabile key


SHOW INDEXES FROM wp_posts\G

SHOW TABLE STATUS 

SHOW SESSION STATUS LIKE 'handler_read%';

主键
  每个表只可能有一个主键
  主键不能包含NULL值
  通过主键获取表中任意特定行
  如果

唯一键

  表可以有多个唯一键
  唯一键可以有包含NULL值
 



EXPLAIN 是SQL语句查询执行计划(QEP)




EXPLAIN SELECT * FROM BIKE WHERE item_id =1231\G;

id: 
select_type
table
type
possible_keys
key:
key_len:
ref:
rows:
Extra: Using where

如果rows 记录大，没有key 就是全表扫描





如果优化过大概是下面情况

id: 1  
03.select_type: SIMPLE  
04.table: inventory  
05.type: ref  
06.possible_keys: item_id  
07.key: item_id  
08.key_len: 3  
09.ref: const  
10.rows: 1  
11.Extra:  


select_type

SIMPLE Simple SELECT (not using UNION or subqueries) 

PRIMARY Outermost SELECT 



  


每个表使用索引，索引分很多种

ROWS

MySQL 优化器估计值




possible_keys

优化器出来的选定索引
一般就是2~3区间左右，太多就会觉得没效，有大量索引
意味这些索引没有被使用到


ken_len 

  4
  5
  30
  32

CREATE TABLE `wp_posts` (  
02. `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,  
03. `post_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',  
04. `post_status` varchar(20) NOT NULL DEFAULT 'publish' ,  
05. `post_type` varchar(20) NOT NULL DEFAULT 'post',  
06. PRIMARY KEY (`ID`),  
07. KEY `type_status_date`(`post_type`,`post_status`,`post_date`,`ID`)  
08.) DEFAULT CHARSET=utf8  
09.  
10. CREATE TABLE `wp_posts` (  
11. `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,  
12. `post_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',  
13. `post_status` varchar(20) NOT NULL DEFAULT 'publish' ,  
14. `post_type` varchar(20) NOT NULL DEFAULT 'post',  
15. PRIMARY KEY (`ID`),  
16. KEY `type_status_date`(`post_type`,`post_status`,`post_date`,`ID`)  
17.) DEFAULT CHARSET=utf8  


 EXPLAIN SELECT ID, post_title FROM wp_posts WHERE post_type='post' AND post_date > '2010-06-01';

这个查询的QEP 返回的key_len 是62。这说明只有post_type列上的索引用到了(因为(20×3)+2=62)。




table 列是EXPLAIN 命令输出结果中的一个单独行的唯一标识符。这个值可能是表名、表的别名或者一个为查询产生临时表
 的标识符，如派生表、子查询或集合。下面是QEP 中table 列的一些示例：
 table: item
 table: <derivedN>
 table: <unionN,M>

table 

The name of the table to which the row of output refers. This can also be one of the following values: 


◾ <unionM,N>: The row refers to the union of the rows with id values of M and N. 


◾ <derivedN>: The row refers to the derived table result for the row with an id value of N. A derived table may result, for example, from a subquery in the FROM clause. 



 select_type
 select_type 列提供了各种表示table 列引用的使用方式的类型。最常见的值包括SIMPLE、PRIMARY、DERIVED 和UNION。其他可能
 的值还有UNION RESULT、DEPENDENT SUBQUERY、DEPENDENT UNION、UNCACHEABLE UNION 以及UNCACHEABLE QUERY


Extra 列提供了有关不同种类的MySQL 优化器路径的一系列
 额外信息。Extra 列可以包含多个值，可以有很多不同的取值


 例如临时表，文件排序

Distinct 去重

全面扫描 在 没有 key 情况下


HAVING
 大部分获取不到所选择行


Not exists 
SELECT * FROM t1 LEFT JOIN t2 ON t1.id=t2.id
  WHERE t2.id IS NULL;


 2.10 ref
 ref 列可以被用来标识那些用来进行索引比较的列或者常量。



 2.12 type
 type 列代表QEP 中指定的表使用的连接方式。下面是最常用的几种连接方式：
  const 当这个表最多只有一行匹配的行时出现system 这是const 的特例，当表只有一个row 时会出现
  eq_ref 这个值表示有一行是为了每个之前确定的表而读取的
  ref 这个值表示所有具有匹配的索引值的行都被用到
  range 这个值表示所有符合一个给定范围值的索引行都被用到
  ALL 这个值表示需要一次全表扫描其他类型的值还有fulltext 、ref_or_null 、index_merge 、unique_subquery、index_subquery 以及index


