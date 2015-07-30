    public SqlSessionFactory build(InputStream inputStream)
    public SqlSessionFactory build(InputStream inputStream, String environment) 
    public SqlSessionFactory build(InputStream inputStream, Properties properties)
    
    
    

(1) 读取xml文件

    String resource = "org/mybatis/example/mybatis-config.xml";
    　　InputStream inputStream = Resources.getResourceAsStream(resource);
    　　SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream) ;


(2)
DataSource dataSource = BlogDataSourceFactory.getBlogDataSource();
TransactionFactory transactionFactory = new JdbcTransactionFactory();
Environment environment = new Environment("development", transactionFactory, dataSource);
Configuration configuration = new Configuration(environment);
configuration.addMapper(BlogMapper.class);
SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(configuration) ;
