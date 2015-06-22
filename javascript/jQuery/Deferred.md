  Promises/A是由CommonJS组织制定的异步模式编程规范


var el = document.getElementById('test');
// (callback hell)”
setTimeout(function(){
  left(function(){
    setTimeout(function(){
       left(function(){
         setTimeout(function(){
           left();
         },2000);
       });
    }, 2000);
  });
}, 2000);







var 上课 = function(){};
var 下课 = function(){};
var 晚饭 = function(){};
var 回家 = function(){};

// 流程部分
next(上课)
    .wait(10*60)
    .next(下课)
    .wait(10*60) 
    .next(晚饭)
    .wait(10*60) 
    .next(回家);


创建三个$.Callbacks对象，分别表示成功，失败，处理中三种状态
创建了一个promise对象，具有state、always、then、primise方法
通过扩展primise对象生成最终的Deferred对象，返回该对象

deferred对象的多种方法，下面做一个总结：
　　（1） $.Deferred() 生成一个deferred对象。
　　（2） deferred.done() 指定操作成功时的回调函数
　　（3） deferred.fail() 指定操作失败时的回调函数
　　（4） deferred.promise() 没有参数时，返回一个新的deferred对象，该对象的运行状态无法被改变；接受参数时，作用为在参数对象上部署deferred接口。
　　（5） deferred.resolve() 手动改变deferred对象的运行状态为"已完成"，从而立即触发done()方法。
　　（6）deferred.reject() 这个方法与deferred.resolve()正好相反，调用后将deferred对象的运行状态变为"已失败"，从而立即触发fail()方法。
　　（7） $.when() 为多个操作指定回调函数。
除了这些方法以外，deferred对象还有二个重要方法，上面的教程中没有涉及到。
　　（8）deferred.then()