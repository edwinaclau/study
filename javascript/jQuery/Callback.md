$.Callbacks


function fn1(arg){
    console.log("fn1 : "+ arg);}
 function fn2(arg){
    console.log("fn2 : "+ arg);}
}


var callbacks = $.Callbacks();
callbacks.add(fn1);

callbacks.add(fn2);

callbacks.add(fn3);
.remove(fn3);

var callbacks = $.Callbacks("once");

once: 只触发一次回调队列（jQuery的异步队列使用的就是这种类型）

memory: 这个解释起来有点绕，用场景来描述就是，当事件触发后，之后add进来的回调就直接执行了，无需再触发多一次（jQuery的异步队列使用的就是这种类型）
stopOnFalse: 当有一个回调返回是false的时候中断掉触发动作
unique: 队列里边没有重复的回调


callbacks.add(fn1, [fn2, fn3,...])//添加一个/多个回调
callbacks.remove(fn1, [fn2, fn3,...])//移除一个/多个回调
callbacks.fire(args)//触发回调，将args传递给fn1/fn2/fn3……
callbacks.fireWith(context, args)//指定上下文context然后触发回调
callbacks.lock()//锁住队列当前的触发状态
callbacks.disable()//禁掉管理器，也就是所有的fire都不生效
callbacks.has(fn)//判断有无fn回调在队列里边
callbacks.empty()//清空回调队列
callbacks.disabled()//管理器是否禁用
callbacks.fired()//是否已经触发过，即是有没有fire/fireWith过
callbacks.locked()//判断是否锁住队列


var callbacks = JQuery.Callbacks();

callbacks.add(fn1,fn2,fn3,fn4);


callbacks.fire("fire");

例如 fire 正在执行到fn2

fn1 fn2 会被标识  fired = true


当执行到 fn4,fring = false





