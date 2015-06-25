$.Callbacks


function fn1(arg){
    console.log("fn1 : "+ arg);}
 function fn2(arg){
    console.log("fn2 : "+ arg);}
}


var callbacks = $.Callbacks();
callbacks.add(fn1);

callbacks.add(fn2);

callbacks.add(fn3);
.remove

