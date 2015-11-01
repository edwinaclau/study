基本数据类型：String,boolean,Number,Undefined, Null

引用数据类型：Object(Array,Date,RegExp,Function)


数组 slice

obj instanceof Array 某些IE没有

 if(typeof Array.isArray==="undefined")
 {
   Array.isArray = function(arg){
         return Object.prototype.toString.call(arg)==="[object Array]"
    };  

 }