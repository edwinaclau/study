
避免每次寻找length属性 
```javascript
for (var j = 0, l = array.length; j < 1; j++) {
}
```

不比较下标，判断元素是否为true
```javascript
var elem

for ( var i = 0; elems[i]; i++) {  
   elem = elems[i];
}

```
循环方法，然后放在数组里面，对应开启
```javascript
jQuery.each( ("blur focus focusin focusout load resize scroll unload click dblclick " +
    "mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave " +
    "change select submit keydown keypress keyup error").split(" "), function( i, name ) {
    // Handle event binding
    jQuery.fn[ name ] = function( data, fn ) {
       return arguments.length > 0 ?
           this.bind( name, data, fn ) :
           this.trigger( name );
    };
    // 将事件名注册（添加）到jQuery.attrFn，当遇到对同名属性的操作时，转换为对事件接口的调用
    if ( jQuery.attrFn ) {
       jQuery.attrFn[ name ] = true;
    }
});
```
```javascript
jQuery = function( selector, context ) {
    return new jQuery.fn.init( selector, context, rootjQuery );
}
```
这里jQuery对象就是jQuery.fn.init对象

如果执行new jQeury(),生成的jQuery对象会被抛弃，最后返回 jQuery.fn.init对象;

因此可以直接调用jQuery( selector, context )，没有必要使用new关键字
还有一行代码如下：
```javascript
jQuery.fn.init.prototype = jQuery.fn = jQuery.prototype
```

所有挂载到jQuery.fn的方法，相当于挂载到了jQuery.prototype，即挂载到了jQuery 函数上（一开始的 jQuery = function( selector, context ) ），但是最后都相当于挂载到了 jQuery.fn.init.prototype，即相当于挂载到了一开始的jQuery 函数返回的对象上，即挂载到了我们最终使用的jQuery对象上。




jQuery.extend(true, { a : { a : "a" } }, { a : { b : "b" } } );
jQuery.extend( { a : { a : "a" } }, { a : { b : "b" } } );

jQuery.extend = jQuery.fn.extend = function() {
	var src, copyIsArray, copy, name, options, clone,
		target = arguments[0] || {},
		i = 1,
		length = arguments.length,
		deep = false;

	// Handle a deep copy situation
	if ( typeof target === "boolean" ) {
		deep = target;

		// skip the boolean and the target
		target = arguments[ i ] || {};
		i++;
	}

	// Handle case when target is a string or something (possible in deep copy)
	if ( typeof target !== "object" && !jQuery.isFunction(target) ) {
		target = {};
	}

	// extend jQuery itself if only one argument is passed
	if ( i === length ) {
		target = this;
		i--;
	}

	for ( ; i < length; i++ ) {
		// Only deal with non-null/undefined values
		if ( (options = arguments[ i ]) != null ) {
			// Extend the base object
			for ( name in options ) {
				src = target[ name ];
				copy = options[ name ];

				// Prevent never-ending loop
				if ( target === copy ) {
					continue;
				}

				// Recurse if we're merging plain objects or arrays
				if ( deep && copy && ( jQuery.isPlainObject(copy) || (copyIsArray = jQuery.isArray(copy)) ) ) {
					if ( copyIsArray ) {
						copyIsArray = false;
						clone = src && jQuery.isArray(src) ? src : [];

					} else {
						clone = src && jQuery.isPlainObject(src) ? src : {};
					}

					// Never move original objects, clone them
					target[ name ] = jQuery.extend( deep, clone, copy );

				// Don't bring in undefined values
				} else if ( copy !== undefined ) {
					target[ name ] = copy;
				}
			}
		}
	}

	// Return the modified object
	return target;
};