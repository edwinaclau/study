锁的基本概念 和 实现



安全锁存的理由 

``` java

public synchronized boolean add(E e) {
     modCount++;
     ensureCapacityHelper(elementCount + 1);
     elementData[elementCount++] = e;
     return true;
}

```

关键synchronized 保证了每次只有一个线程可以访问对象实例

确保多线程环境对象内部数据的一致性


对象头和锁


Java虚拟机有一个头 Mark Word

25位比特

4个表示年龄

1位表示是否有偏向锁

避免残酷的竞争，锁在java虚拟机中实现和优化


偏向锁

程序没有竞争，已经取得锁，一但线程获取后，进入偏向模式，当两次请求这个锁后，无需要相关同步操作,节省时间

JVM -XX:+UseBiasedLocking 启动偏向锁适应在没有太多竞争条件之下

轻量级锁

 JVM BasicObjectLock 对象实现，

 Mark Word 指向BasicLock对象指针



锁的膨胀，

虚拟机使用重量级 MarkWord 又是改变指针



自旋锁

 膨胀后,进入ObjectMonitor 的 线程挂起，这样线程上下文的性能  比较大

 转而执行一个空循环,

 使用自旋后，线程被挂起的几率相对减少

1

