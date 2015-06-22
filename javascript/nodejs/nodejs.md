Node.js 使用事件驱动， 非阻塞I/O 模型而得以轻量和高效，



V8引擎执行Javascript的速度非常快，性能非常好。


单线程异步式 I/O



整体上比较简单,没有多线程烦恼，也不用担心阻塞问题


java


import 引入包


improt java.util.*;


varsio = require('socket.io'); 


npm install express

和centos 包安装差不多，大家都懂
yun install express

python

easy_install express
pip install  express





var http = require('http');

http.createServer(function (request, response) {
  response.writeHead(200, {'Content-Type': 'text/plain'});
  response.end('Hello World\n');
}).listen(8888);

console.log('Server running at http://127.0.0.1:8888/');


事件
var EventEmmitter = require('events').EventEmitter;
var evet = new EventEmitter();

event.on('some_event', function() {

  console.log('');
}


setTimeout(function() {

    event.emit('some_event');
), 1000);



package.json
{

}





Node.js 调试命令


run          执行脚本
 
restart      重新执行脚本
 
cont, c       继续执行，直到遇到下一个断点

next, n

step, s

out, o

setBreakPoint(), sb()

backtrace, bt

list(5)

watch(expr)

unwatch(expr)

repl

kill

scripts

version


$node debug debug.js

break 
