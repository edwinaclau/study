动态代理必须实现一个或N个接口，如果代理没有实现接口呢？

CGLIB


通过JAVA字节码操作，


public class BookServiceBean {  
 public void create(){     
        System.out.println("create() is running !");     
    }     
    public void query(){     
        System.out.println("query() is running !");     
    }     
    public void update(){     
        System.out.println("update() is running !");     
    }     
    public void delete(){     
        System.out.println("delete() is running !");     
    }     
}  


public class BookServiceFactory {  
 private static BookServiceBean service = new BookServiceBean();  
 private BookServiceFactory() {  
 }  
 public static BookServiceBean getInstance() {  
  return service;  
 }  
}  



public class Client {     
    
    public static void main(String[] args) {     
        BookServiceBean service = BookServiceFactory.getInstance();   
        doMethod(service);     
    }     
    public static void doMethod(BookServiceBean service){     
        service.create();  
        service.update();  
        service.query();  
        service.delete();   
    }     
}   