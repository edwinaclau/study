SELECT * FROM employees WHERE AGE < $age



SELECT * FROM employees WHERE AGE < 1;DELETE FROM employes


注入成功


对策
 （1）使用占位符
  (2) 应用程序拼接SQL语句，确保字面量正确处理


SELECT * FROM employees WHERE author = ? ORDERY BY id

占位符 有 分 动态 和 静态

SELECT * FROM users
WHERE ID * AND PWD = *

占位符编译结果



LIKE 语句与通配符

WHERE name LIKE '%山田%'




各种列的排序


SELECT * FROM books ORDER BY $row





SQL 将有特殊意义字符串和符号都转义


确保数值字面中不被混入数值意外的字符

