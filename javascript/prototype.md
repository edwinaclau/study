```javascript
var Parent = function(name) {
   this.name = name || 'bash';
};



Parent.prototype.printName = function() {
    console.log(this.name);
};

var Child = function(name) {};

inherit(Child, Parent);

Child.inherit(Parent);
```



var inherit = function(subClass, superClass) {
    subClass.prototype = new superClass();
};


Function.prototype.inherit = function (superClass) {
   this.prototype = new superClass();
};


1.问题对象如果不在属性，对象创建这个属性，并赋值，
存在赋值，




var Parent = function(name) {
   this.name = name || "hello";
   this.printName = function() {
        console.log(this.name);
   };
}


var Child = function (name) {
   Parent.call(this, name);

}


var child = new Child('test');


