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



先来看看 $.callbacks('once memory'),
   


// A sample logging function to be added to a callbacks list
var foo = function( value ) {
  console.log( "foo: " + value );
};
 
// Another function to also be added to the list
var bar = function( value ) {
  console.log( "bar: " + value );
};
 
var callbacks = $.Callbacks();
 
// Add the function "foo" to the list
callbacks.add( foo );
 
// Fire the items on the list
callbacks.fire( "hello" );
// Outputs: "foo: hello"
 
// Add the function "bar" to the list
callbacks.add( bar );
 
// Fire the items on the list again
callbacks.fire( "world" );
 
// Outputs:
// "foo: world"
// "bar: world"            


$.Callbacks('once memory').fire







// A sample logging function to be added to a callbacks list
var foo = function( value ) {
  console.log( "foo:" + value );
};
 
var callbacks = $.Callbacks();
 
// Add the function "foo" to the list
callbacks.add( foo );
 
// Fire the items on the list
callbacks.fire( "hello" ); // Outputs: "foo: hello"
callbacks.fire( "world" ); // Outputs: "foo: world"
 
// Add another function to the list
var bar = function( value ){
  console.log( "bar:" + value );
};
 
// Add this function to the list
callbacks.add( bar );
 
// Fire the items on the list again
callbacks.fire( "hello again" );
// Outputs:
// "foo: hello again"
// "bar: hello again"



resolve、 rejct、notify

Defferred中定义了三种动作，resolve（解决）、reject（拒绝）、notify（通知），对应Callbacks对象的fire动作。


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

    deferred.always()

这个方法也是用来指定回调函数的，
它的作用是，不管调用的是deferred.resolve()还是deferred.reject()，最后总是执行。




这两个API语法几乎一样，但是有着很大的差别。deferred.promise()是Deferred实例的一个方法，他返回一个Deferred.Promise实例。一个Deferred.Promise对象可以理解为是deferred对象的一个视图，它只包含deferred对象的一组方法，包括：done(),then(),fail(),isResolved(), isRejected(), always(),这些方法只能观察一个deferred的状态，而无法更改deferred对象的内在状态。这非常适合于API的封装。例如一个deferred对象的持有者可以根据自己的需要控制deferred状态的状态（resolved或者rejected），但是可以把这个deferred对象的Promise对象返回给其它的观察者，观察者只能观察状态的变化绑定相应的回调函数，但是无法更改deferred对象的内在状态，从而起到很好的隔离保护作用。 


$(function(){  
    //  
    var deferred = $.Deferred();  
    var promise = deferred.promise();  
      
    var doSomething = function(promise) {  
        promise.done(function(){  
            alert('deferred resolved.');  
        });  
    };  
      
    deferred.resolve();  
    doSomething(promise);  
})  




deferred.promise()也可以接受一个object参数，此时传入的object将被赋予Promise的方法，并作为结果返回。 


// Existing object  
var obj = {  
  hello: function( name ) {  
    alert( "Hello " + name );  
  }  
},  
// Create a Deferred  
defer = $.Deferred();  
  
// Set object as a promise  
defer.promise( obj );  
  
// Resolve the deferred  
defer.resolve( "John" );  
  
// Use the object as a Promise  
obj.done(function( name ) {  
  this.hello( name ); // will alert "Hello John"  
}).hello( "Karl" ); // will alert "Hello Karl"




deferred.always()

当Deferred（延迟）对象解决或拒绝时，调用添加处理程序。
deferred.done()

当Deferred（延迟）对象解决时，调用添加处理程序。
deferred.fail()

当Deferred（延迟）对象拒绝时，调用添加处理程序。
deferred.isRejected()

确定一个Deferred（延迟）对象是否已被拒绝。
deferred.isResolved()

确定一个Deferred（延迟）对象是否已被解决。
deferred.notify()

根据给定的 args参数 调用Deferred（延迟）对象上进行中的回调 （progressCallbacks）。
deferred.notifyWith()

根据给定的上下文（context）和args递延调用Deferred（延迟）对象上进行中的回调（progressCallbacks ）。
deferred.pipe()

实用的方法来过滤 and/or 链Deferreds。
deferred.progress()

当Deferred（延迟）对象生成进度通知时，调用添加处理程序。
deferred.promise()

返回Deferred(延迟)的Promise（承诺）对象。
deferred.reject()

拒绝Deferred（延迟）对象，并根据给定的args参数调用任何失败回调函数（failCallbacks）。
deferred.rejectWith()

拒绝Deferred（延迟）对象，并根据给定的 context和args参数调用任何失败回调函数（failCallbacks）。
deferred.resolve()

解决Deferred（延迟）对象，并根据给定的args参数调用任何完成回调函数（doneCallbacks）。
deferred.resolveWith()

解决Deferred（延迟）对象，并根据给定的 context和args参数调用任何完成回调函数（doneCallbacks）。
deferred.state()

确定一个Deferred（延迟）对象的当前状态。
deferred.then()

当Deferred（延迟）对象解决，拒绝或仍在进行中时，调用添加处理程序。
jQuery.Deferred()

一个构造函数，返回一个链式实用对象方法来注册多个回调，回调队列， 调用回调队列，并转达任何同步或异步函数的成功或失败状态。
Also in: Core
jQuery.when()

提供一种方法来执行一个或多个对象的回调函数， Deferred(延迟)对象通常表示异步事件。
.promise()

返回一个 Promise 对象用来观察当某种类型的所有行动绑定到集合，排队与否还是已经完成。







ES6对异步的支持

这是一个新的技术，成为2015年的ECMAScript（ES6）标准的一部分。该技术的规范已经完成，但实施情况在不同的浏览器不同，在浏览器中的支持情