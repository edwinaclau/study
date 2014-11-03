理解javaScript 定时器

js是单线程异步，


setTimeout 和 setInterval

一般都认为多少毫秒执行该函数，

setTimeout 在指定的毫秒数后，加入执行队列尾

setInterval 每定时毫秒后，加入执行队列尾


如果一个定时器的回调执行完成时间

到下一个回调开始时间是为  **时间间隔**


对于setTimeout ，时间间隔是大于delay

对于setInterval 时间是小于等于delay

var endTime = null;
setInterval(count, 200);

function count() {
    var elapsedTime = end ? 
    i++;
    console.log('');
    endTime = new Date();
}

大概每次相差10MS左右


修改后:


function count() {
    var elapsedTime = end ? 
    i++;
    console.log('');
    sleep(100);
    endTime = new Date();
}


200
91
100
100
100


99
101
100
100

再修改
function count() {
  var elapsedTime = endTime ? (new Date() - endTime) : 200;
  i++;
  console.log('current count: ' + i + '.' + 'elapsed time: ' + elapsedTime + 'ms');
  sleep(400); //sleep 400ms
  endTime = new Date();
}

间隔居然没了，为何会缩小这么小间隔
如果setInterval定时时间到，前一个回调还没有执行完时
,就会把回调放在尾，如果setInterval 定时间多次触发
，最前一个回调还在执行，机会放弃本次回调