简单来说，requirejs是一个遵循 AMD(Asynchronous Module Definition)规范的模块载入框架。


看requirejs

1.无非就是找到入口

2.如何加载js模块

3.如何处理js的依赖关系


4.检查加载是否成功

全面都有一大堆方法使用，这里不说,大家看名字就懂，无非是一些
遍历，反向遍历，判断是否 函数  数组,balalala...

        function isFunction(it) {}
        function isArray(it) {}
        function each(ary, func) {}
        function eachReverse(ary, func) {}
        function hasProp(obj, prop) {}
        function getOwn(obj, prop) {}
        function eachProp(obj, func) {}

function newcontest(contestName)

     var inCheckLoaded, Module, context, handlers,
            function trimDots(ary) {}
            function normalize(name, baseName, applyMap) {}
            function removeScript(name) {}
            function hasPathFallback(id) {}
            function splitPrefix(name) {}
            function makeModuleMap(name, parentModuleMap, isNormalized, applyMap) {}
            function getModule(depMap) {}
            function on(depMap, name, fn) {}
            function onError(err, errback) {}
            function takeGlobalQueue() {}
            handlers = {};
            function cleanRegistry(id) {}
            function breakCycle(mod, traced, processed) {}
            function checkLoaded() {}
            Module = function (map) {};
            Module.prototype = {};
            function callGetModule(args) {}
            function removeListener(node, func, name, ieName) {}
            function getScriptData(evt) {}
            function intakeDefines() {}
            context = {}
            context.require = context.makeRequire();
            return context;


这部分是重点，提供加载，检查加载，获取或移除html script节点
全局队列，获取模块，

      req = requirejs = function (deps, callback, errback, optional) {};
        req.config = function (config) {};
        req.nextTick = typeof setTimeout !== 'undefined' ? function (fn) {
            setTimeout(fn, 4);
        } : function (fn) { fn(); };

        req.onError = defaultOnError;
        req.createNode = function (config, moduleName, url) {};
        req.load = function (context, moduleName, url) {};
        define = function (name, deps, callback) {};
        req.exec = function (text) {};
        req(cfg);



总是data-main入口实现 ：