intro.js             -- 全局闭包头部
sea.js               -- 基本命名空间

util-lang.js         -- 语言增强
util-events.js       -- 简易事件机制
util-path.js         -- 路径处理
util-request.js      -- HTTP 请求
util-deps.js         -- 依赖提取

module.js            -- 核心代码
config.js            -- 配置
outro.js             -- 全局闭包尾部


别忘记 seajs 下面有个test 文件包，那里干货很多
为什么呢？我先拿出来给大家看看


tests\specs\util



  var test = require('../../test')
  var assert = test.assert


  assert(dirname('./a/b/c.js') === './a/b/', 'dirname')
  assert(dirname('a/b/c.js') === 'a/b/', 'dirname')
  assert(dirname('/a/b/c.js') === '/a/b/', 'dirname')
  assert(dirname('/d.js') === '/', 'dirname')
  assert(dirname('/') === '/', 'dirname')
  assert(dirname('/xxx') === '/', 'dirname')
  assert(dirname('http://cdn.com/js/file.js') === 'http://cdn.com/js/', 'dirname')
  assert(dirname('http://cdn.com/js/file.js?t=xxx') === 'http://cdn.com/js/', 'dirname')
  assert(dirname('http://cdn.com/js/file.js?t=xxx#zzz') === 'http://cdn.com/js/', 'dirname')
  assert(dirname('http://example.com/page/index.html#zzz?t=xxx') === 'http://example.com/page/', 'dirname')
  assert(dirname('http://example.com/arale/seajs/1.2.0/??sea.js,seajs-combo.js') === 'http://example.com/arale/seajs/1.2.0/', 'dirname')
  assert(dirname('http://cdn.com/??seajs/1.2.0/sea.js,jquery/1.7.2/jquery.js') === 'http://cdn.com/', 'dirname')
  assert(dirname('http://seajs.com/docs/#/abc') === 'http://seajs.com/docs/', 'dirname')



这样你就懂得dirname到底搞了什么，so 你懂的....

seajs 比较直观 从上而下感觉，比requirejs

加载js文件
肯定是创建script tag,插入DOM


模块管理在于依赖问题，和公共方法接口输出

     像恋爱三角关系 甚至 四角



Module  根据 CMD (id, deps, factory)

  save

  resolve

  load
  


Function的toString 返回 code
util-deps.js
* util-deps.js - The parser for dependencies
* 专门分析解决依赖
function parseDependencies(s) {
  if(s.indexOf('require') == -1) {
    return []
  }

匹配require 关键字 后面的 关键字( var test = require('../../test'))


通过id来匹配url地址

function id2Uri(id, refUri) {
  if (!id) return ""

  id = parseAlias(id)
  id = parsePaths(id)
  id = parseVars(id)
  id = normalize(id)

  var uri = addBase(id, refUri)
  uri = parseMap(uri)

  return uri
}



获取seajs绝对路径都简单，

这个不说了，就是分成6个状态

var STATUS = Module.STATUS = {
  // 1 - The `module.uri` is being fetched
  FETCHING: 1,
  // 2 - The meta data has been saved to cachedMods
  SAVED: 2,
  // 3 - The `module.dependencies` are being loaded
  LOADING: 3,
  // 4 - The module are ready to execute
  LOADED: 4,
  // 5 - The module is being executed
  EXECUTING: 5,
  // 6 - The `module.exports` is available
  EXECUTED: 6
}

* FETCHING 开始加载当前模块
* SAVED 当前模块加载完成并保存模块数据
* LOADING 开始加载依赖的模块
* LOADED 依赖模块已经加载完成
* EXECUTING 当前模块执行中
* EXECUTED 当前模块执行完成


跳跃一下我们再看看他们怎么实现js 
util-request.js

明显就是来异步加载

  var doc = document
  var head = doc.head || doc.getElementsByTagName("head")[0] || doc.documentElement
  var baseElement = head.getElementsByTagName("base")[0]

  var currentlyAddingScript

  function request(url, callback, charset, crossorigin) {
    var node = doc.createElement("script")

    if (charset) {
      node.charset = charset
    }

    if (!isUndefined(crossorigin)) {
      node.setAttribute("crossorigin", crossorigin)
    }

    addOnload(node, callback, url)

    node.async = true
    node.src = url
    currentlyAddingScript = node

    // ref: #185 & http://dev.jquery.com/ticket/2709
    baseElement ?
        head.insertBefore(node, baseElement) :
        head.appendChild(node)

    currentlyAddingScript = null




  function addOnload(node, callback, url) {
    var supportOnload = "onload" in node

    if (supportOnload) {
      node.onload = onload
      node.onerror = function() {
        emit("error", { uri: url, node: node })
        onload(true)
      }
    }
    else {
      node.onreadystatechange = function() {
        if (/loaded|complete/.test(node.readyState)) {
          onload()
        }
      }
    }





再来看一看util-cs.js


var interactiveScript

function getCurrentScript() {
  if (currentlyAddingScript) {
    return currentlyAddingScript
  }

  // For IE6-9 browsers, the script onload event may not fire right
  // after the script is evaluated. Kris Zyp found that it
  // could query the script nodes and the one that is in "interactive"
  // mode indicates the current script
  // ref: http://goo.gl/JHfFW
  if (interactiveScript && interactiveScript.readyState === "interactive") {
    return interactiveScript
  }

  var scripts = head.getElementsByTagName("script")

  for (var i = scripts.length - 1; i >= 0; i--) {
    var script = scripts[i]
    if (script.readyState === "interactive") {
      interactiveScript = script
      return interactiveScript
    }
  }



明显看到 return currentlyAddingScript,可以看到正在加载的Script 


而 IE6~9兼容问题，就是循环用readyState 等于 interactive 


以后再补