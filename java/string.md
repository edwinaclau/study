
String字符常量

String:创建后不可修改


stringBuffer (thread safe)

字符串可变

StringBuilder (non thread safe)

StringBuffer 类基本相同，都是可变字符换字符串序列，不同点是  是线程安全的，StringBuilder 是线程不安全的。 在性能方面，由于 String 类的操作是产生新的 String 对象，而 StringBuilder 和 StringBuffer 只是一个字符数组的扩容而已，所以 String 类的操作要远慢于 StringBuffer 和 StringBuilder。






String S1 = "This is " + "easy" + "fafjkl"


String S1 = "This is easy fafjkl"


总结：
1、当使用任何方式来创建一个字符串对象s时，Java运行时（运行中JVM）会拿着这个X在String池中找是否存在内容相同的字符串对象，如果不存在，则在池中创建一个字符串s，否则，不在池中添加。
2、Java中，只要使用new关键字来创建对象，则一定会（在堆区或栈区）创建一个新的对象。 
3、使用直接指定或者使用纯字符串串联来创建String对象，则仅仅会检查维护String池中的字符串，池中没有就在池中创建一个，有则罢了！但绝不会在堆栈区再去创建该String对象。 
4、使用包含变量的表达式来创建String对象，则不仅会检查维护String池，而且还会在堆栈区创建一个String对象。