jQuery有几种不同绑定事件方法，

简单来说jQury和我们一般绑定不同就是有代理机制，其实就是和平时我们上网路由一个道理
,同一由路由管理我们上网的包,当然有一些没有用代理机制


bind 方法是直接绑定在元素上，
    （和原生的attchevent addlistener 一样的)



live 方法是绑定在一个document元素上








delegate ，实现事件委托,jQuery 

$().delegate('a', 'click',function()


事件冒泡到 $()里面的元素中，就会检查该事件的click,和source 是否和CSS selector一样
 


其实 .bind(), .live(), .delegate()都是通过.on()来实现的，.unbind(), .die(), .undelegate()也是一样的都是通过.off()来实现的，提供了一种统一绑定事件的方法。


on绑定事件

add 绑定 addEventListener


出发事件执行 addEventListener 回调  dispatch

fix对象


handlers 把 委托和 原生分开


执行内存的事件回调，传入内部对象


.on event selector data handler(eventObject)

事件名
选择器字符串
传递给事件处理函数
事件被触发，执行函数