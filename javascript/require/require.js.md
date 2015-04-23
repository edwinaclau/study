
data-main="main"
明显就是个入口，然后自动执行

根据源码注释，这个事初始化context
req({{})

到底这个

req 是何须东西？

req = requirejs = function(deps, callback, errback, optional) {}


首先当然是查找data-main,毕竟入口在那里
查找源码data-main字眼

 dataMain = script.getAttribute('data-main');


requireJS不是只针对浏览器，只是临时连接不上，
scripts()


eachReverse

明显是逆序查找

用 getxxx查找所有script,返回所有script tags

head 你是一定不用要

我们需要的是data-main,

dataMain = script.getAttribute('data-main');

main.js只是默认，入口是可以自己选择


cfg.deps = cfg.deps ? cfg.deps.concat(mainScript) : [mainScript];





查找第一个依赖的数组


context 

变成


return context.require(deps, callback, errback);