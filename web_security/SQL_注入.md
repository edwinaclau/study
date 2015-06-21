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

<?php
//用户输入的数据
$name = 'admin';
$pass = '123456';
//首先新建mysqli对象,构造函数参数中包含了数据库相关内容。
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
//设置sql语句默认编码
$this->mysqli->set_charset("utf8");
//创建一个使用通配符的sql语句
$sql = 'SELECT user_id FROM admin WHERE username=? AND password=?;';
//编译该语句，得到一个stmt对象.
$stmt = $conn->prepare($sql);
/********************之后的内容就能重复利用，不用再次编译*************************/
//用bind_param方法绑定数据
//大家可以看出来，因为我留了两个?，也就是要向其中绑定两个数据，所以第一个参数是绑定的数据的类型(s=string,i=integer)，第二个以后的参数是要绑定的数据
$stmt->bind_param('ss', $name, $pass);
//调用bind_param方法绑定结果（如果只是检查该用户与密码是否存在，或只是一个DML语句的时候，不用绑定结果）
//这个结果就是我select到的字段，有几个就要绑定几个
$stmt->bind_result($user_id);
//执行该语句
$stmt->execute();
//得到结果
if($stmt->fetch()){
    echo '登陆成功';
    //一定要注意释放结果资源，否则后面会出错
    $stmt->free_result();
    return $user_id; //返回刚才select到的内容
}else{echo '登录失败';}
?>


