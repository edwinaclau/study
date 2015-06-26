jQuery  把 DOM节点包装成JQ对象


DOM 封装成一个数组


   NodeList

      |
      |
   makeArray

      |
      |

   ArrayLike

    {

     0:div
     1:div
     2:div
     ...
    }

$('div').first()



核心转换
Array.prototype.slice方法将 伪数组 转成 数组

Array.prototype.push方法将 数组 转成 伪数组


 var a={length:2,0:'first',1:'second'};
 Array.prototype.slice.call(a);
//  ["first", "second"]
  
 var a={length:2};
 Array.prototype.slice.call(a);
//  [undefined, undefined]