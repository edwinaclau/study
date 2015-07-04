DOM模型提供


insertBefore() , appendChild(), removeChild(), closeNode(), replaceChild()


jQuery.fn.extend ({
     test: function( text ) { ... },
     wrapAll: function( html ) { ... },
     wrapInner: function( html ) {... },
     unwrap:
     append
     remove
     empty:
     clone
     html
     replaceWith
     detach
     domManip
after



.domManip( args, table, callback)



elems 转换HTML代码数组

context

fagment 文档碎片

scripts 脚本数组

.domManip()是jQuery DOM操作的核心函数

* 1. 将args转换为DOM元素，并放在一个文档碎片中，调用jQuery.buildFragment和jQuery.clean实现

* 2. 遍历匹配元素集合，执行callback，将DOM元素作为参数传入，由callback执行实际的插入操作

* 3. 转换后在DOM中出现 sciprt元素


 domManip: function ( args, type, table, callback)

 转换HTML 代码为 DOM 
 调用回调函数插入DOM

首先jQuery 一定涉及到兼容，操控 DOM，这个是一定的

例如IE body 克隆元素属性 复制复选框的选中状态 


args : DOM 元素，元素数组，jQuery对象,HTML字符串





HTML代码转换 DOM元素

执行回调函数插入元素



执行转换后DOM元素中的script 元素












jQuery.buildFragment 

.append(content,[,content]
.prepend
.before
.after


.append( content, [, content])

.prepend( content, [, content])


.before(content, [, content])


.after( content,[,content])



.appendTo(target) , .prepend(target), .insertBefore( target )

.insertAfter(target)















.html([value])

  匹配元素集合第一个元素的HTML元素，设置，通过inner方法

  getfirst,setall

没有传入参数情况

 HTML代码不需要修正









.text([text])

用来匹配元素集合中所有元素合并后的文本内容

text: function ( text )




.remove( selector, keepData);

 从文档中移除匹配元素，遍历匹配的元素集合，先移除后代元素和匹配[元素关联]的 数据 和 时间



.empty()
  用于文档中移除匹配元素的所有子元素。 
  先移除后代元素关联的数据 和 时间， 避免内存泄露，


.detach( selector )
   调用.remove(selector, keepData)

  用于从文档中移除匹配元素集合，但是保留后代元素和匹配元素关联的数据 和 事件


