#copy_on_write


```
$person = array("eric",25,"leng"); 
```


```
$programmer = $person; //数组没有被复制 
```

* 为了省内存，将数组映射到同一地方

* 当要更改后，首先复制原本结构到新的结构，再引用新的东西


就是

```
$programmer---->   programmer_array
    $person   ----->   programmer_array
```


```
$people[1] = 30; //数组被复制，值发生变化
```

发生改变
```
    $programmer----> programmer_array
    $person   -----> person_array
```

* http://php.net/manual/en/features.gc.refcounting-basics.php