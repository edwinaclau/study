

代理模式



  特点就是代理类 与 委托类 有同样的接口，代理类

负责为 委托类预处理消息，过滤消息，把消息转发给托给类


动态代理:程序运行，通过反射动态创建生成


静态代理:生成源代码，对其编译，在程序运行前，对.clss文件
代理类已经存在



动态涉及  java.lang.reflect  Proxy 和 invocationhandler


public interface Count {

   public void queryCount();

   update void updateCount();
}


public class CountImpl implements Count {  
    @Override     
    public void queryCount() {     
        System.out.println("查看账户方法...");     
    }     
    @Override     
    public void updateCount() {     
        System.out.println("修改账户方法...");     
    }     
}   


public class CountProxy implements Count {     
    private CountImpl countImpl;     
     
    /**   
     * 覆盖默认构造器   
     *    
     * @param countImpl   
     */     
    public CountProxy(CountImpl countImpl) {     
        this.countImpl = countImpl;     
    }     
     
    @Override     
    public void queryCount() {     
        System.out.println("事务处理之前");     
        // 调用委托类的方法;     
        countImpl.queryCount();     
        System.out.println("事务处理之后");     
    }     
     
    @Override     
    public void updateCount() {     
        System.out.println("事务处理之前");     
        // 调用委托类的方法;     
        countImpl.updateCount();     
        System.out.println("事务处理之后");     
     
    }     
     
}  



public class TestCount {     
    public static void main(String[] args) {     
        CountImpl countImpl = new CountImpl();     
        CountProxy countProxy = new CountProxy(countImpl);     
        countProxy.updateCount();     
        countProxy.queryCount();     
    }     
}    



明显这样代理就只能一个？如果很多那怎么办？




接口和实现类


public interface PersonService {

    public String getPersonname(Integer personId);
   
    public void save(String name);
    
    public void update(Integer personId, String name);

}


public class PersonServiceBean implements PersonService {

       public String user = null;

       public PersonServiceBean(){};
       public PersonServiceBean(String user){
            this.user = user;
}


  public String getPersonName(Integer personId) {
          System.out.println("");
          return this.user;
  }


   public void save(String name) {






  
import java.lang.reflect.InvocationHandler;  
import java.lang.reflect.Method;  
import java.lang.reflect.Proxy;  
  
import com.tech.service.impl.PersonServiceBean;  
  
/** 
 *   
 * 切面   
 * @author ch 
 * 
 */  
public class JDKProxyFactory implements InvocationHandler{  
  
    private Object proxyObject; //目标对象  
  
    /** 
     * 绑定委托对象并返回一个代理类  
     * @param proxyObject 
     * @return 
     */  
    public Object createProxyInstance(Object proxyObject) {  
        this.proxyObject = proxyObject;  
          
        //生成代理类的字节码加载器   
        ClassLoader classLoader = proxyObject.getClass().getClassLoader();  
        //需要代理的接口，被代理类实现的多个接口都必须在这里定义  (这是一个缺陷，cglib弥补了这一缺陷)    
        Class<?>[] proxyInterface = proxyObject.getClass().getInterfaces();//new Class[]{};   
          
        //织入器，织入代码并生成代理类     
        return Proxy.newProxyInstance(classLoader,  
                proxyInterface, this);  
  
    }  
  
    @Override  
    public Object invoke(Object proxy, Method method, Object[] args)  
            throws Throwable {  
        PersonServiceBean bean = (PersonServiceBean)this.proxyObject;  
        Object result = null;  
        //控制哪些用户执行切入逻辑  
        if(bean.getUser() != null) {  
            //执行原有逻辑     
            result = method.invoke(this.proxyObject, args);  
        }  
        return result;  
    }  
}  