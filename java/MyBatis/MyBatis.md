

         SQL查询
支持      存储过程
         高级查询


消除     手工jdbc代码
         参数手工配置
         结果集检索

使用       XML
           注解


      iBATIS核心


mybatis    SqlSessionFactory
       
           SqlSession

           mapper

简单来说就是 根据业务模型变动改变数据 

           ORM 写的东西 可以用在多个数据库平台,


http://mybatis.github.io/mybatis-3/configuration.html#typeHandlers

类型转换

Type Handler   

Java Types 

JDBC Types 



org.apache.ibatis.session.Configuration类：MyBatis全局配置信息类

org.apache.ibatis.session.SqlSessionFactory接口：操作SqlSession的工厂接口，具体的实现类是DefaultSqlSessionFactory

org.apache.ibatis.session.SqlSession接口：执行sql，管理事务的接口，具体的实现类是DefaultSqlSession

org.apache.ibatis.executor.Executor接口：sql执行器，SqlSession执行sql最终是通过该接口实现的，常用的实现类有SimpleExecutor和CachingExecutor,这些实现类都使用了装饰者设计模式

一级缓存的作用域是SqlSession，那么我们就先看一下SqlSession的select过程：
一级缓存的作用域是SqlSession，那么我们就先看一下SqlSession的select过程：

这是DefaultSqlSession（SqlSession接口实现类，MyBatis默认使用这个类）的selectList源码（我们例子上使用的是selectOne方法，调用selectOne方法最终会执行selectList方法）：
