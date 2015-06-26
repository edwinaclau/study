innerHTML

如果改变innerHTML,有些浏览器不执行

有些元素属性会关闭，在IE

IE8不能 innerHTML 写入<style? tag

IE8 返回的是大写的tags,甚至

IE9 
•In IE9 and lower innerHTML refuses to work on tables and selects. Solve this by using pure DOM methods instead. See this explanation of the table behaviour by innerHTML’s inventor. I assume something similar goes for selects.



innerText


x.innerTExt



insertAdjacentElement

IE私有 


outerText




tesxtContent





activeElement


I test this property with form fields, links, and buttons.
•Firefox on Mac doesn’t support this when the active element is a button. On Windows and Linux buttons work fine.
•Safari supports it only on form fields; not on links or buttons.
•Blink-based browsers don’t support it on links.




createElement()

	var x = document.createElement('P')

almost


IE8  ('<P>')
IE8  或更低 返回 小写 nodeName
•IE8 and below return a lower-case nodeName for custom elements such as ppk.

createTextNode()

	var x = document.createTextNode('text')
    Create a text node with content text and temporarily place it in x, which is later inserted into the document.
	IE8 和 低  不能加入 <style> tag





getElementById()

var x = document.getElementById('test')

Take the element with id="test" (wherever it is in the document) and put it in x.

If there is more than one element with id="test", the method selects the first in the document. All others are ignored.
•IE7 and lower also return the element with name="test".
	



getElementsByClassName()


document.getElementsByClassName('test')
document.getElementsByClassName('test test2')

The first expression returns a nodeList with all elements that have a class value that contains "test". The second one returns a nodeList will all elements that have a class value that contains both "test" and "test2" (in any order).


getElements​ByTagName()


var x = document.getElementsByTagName('P')

Make x into a nodeList of all P's in the document, so x[1] is the second P etc.
var x = y.getElementsByTagName('P')

Gets all paragraphs that are descendants of node y.
•The * argument, which ought to select all elements in the document, doesn't work in IE 5.5.





nodeName



nodeType




nodeValue





tagName




childNodes[]


firstChild



hasChildNodes()



lastChild




createAttribute()

z = document.createAttribute('title');
z.value = 'Test title';
x.setAttributeNode(z)


This creates a title attribute with a value and sets it on node x.



getAttribute()

x.getAttribute('align')

Gives the value of the align attribute of node x. Upper case attribute names are also allowed.
•In IE5-7, accessing the style attribute gives an object, and accessing the onclick attribute gives an anonymous function wrapped around the actual content.
•IE8 and above return the inline styles, but where the test would expect color: green, IE8 returns COLOR: green, and IE9 and up color: green; (with semicolon).



getAttributeNode()

x.getAttributeNode('align')

Get the attribute object align of node x. This is an object, not a value.
•IE 6/7 don't allow you to access the value of x.getAttributeNode('style').
•IE8 and above return the inline styles, but where the test would expect color: green, IE8 returns COLOR: green, and IE9 and up color: green; (with semicolon).
	


hasAttribute()


x.hasAttribute('align')

Returns true when node x has an align attribute, false when it hasn't.


ownerDocument


x.ownerDocument

Refers to the document object that 'owns' node x. This is the document node.



textContent，nodeValue




tagName


Get the tag name of node x. Correct values are:


Element

Attribute

Text

Comments

Document

the UPPER CASE tag name n/a n/a n/a n/a 

My advice is not to use tagName at all.
nodeName contains all functionalities of tagName, plus a few more. Therefore nodeName is always the better choice.
•In IE8 and lower the tagName of a comment node is !

