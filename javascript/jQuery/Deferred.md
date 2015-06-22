  Promises/A是由CommonJS组织制定的异步模式编程规范

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
