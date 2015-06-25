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


