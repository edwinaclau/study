线程同步synchronized和volatile


public class test1 {  
    public static void main(String[] args) {  
        final Outputter output = new Outputter();  
        new Thread() {  
            public void run() {  
                output.output("persion1");  
            };  
        }.start();        
        new Thread() {  
            public void run() {  
                output.output("persion2");  
            };  
        }.start();  
    }  
}  
class Outputter {  
    public void output(String name) {  
        // TODO 为了保证对name的输出不是一个原子操作  
        for(int i = 0; i < name.length(); i++) {  
            System.out.print(name.charAt(i));  
            // Thread.sleep(10);  
        }  
    }  
}  
结果就是 pes1operonsn2



synchronized将需要互斥的代码包含起来，上一把锁

public synchronized void output(String name) {  
    //  
    for(int i = 0; i < name.length(); i++) {  
        System.out.print(name.charAt(i));  
    }  
}  


        1. 获得同步锁；
        2. 清空工作内存；
        3. 从主内存拷贝对象副本到工作内存；
        4. 执行代码(计算或者输出等)；
        5. 刷新主内存数据；
        6. 释放同步锁。


synchronized既保证了多线程的并发有序性，又保证了多线程的内存可见性。


volatile是第二种Java多线程同步的机制