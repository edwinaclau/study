```php

<?php
$arr = array("one", "two", "three");
reset($arr);
while (list($key, $value) = each($arr)) {
    echo "Key: $key; Value: $value<br />\n";
}

foreach ($arr as $key => $value) {
    echo "Key: $key; Value: $value<br />\n";
}

?>

```
### 执行命令
```shell
[root@d php_opcode]# ls
php_array.php
[root@d php_opcode]# vim php_array.php 
[root@d php_opcode]# php -dvld.active=1 php_array.php 
Finding entry points
Branch analysis from position: 0
Jump found. Position 1 = 13, Position 2 = 20
Branch analysis from position: 13
Jump found. Position 1 = 6
Branch analysis from position: 6
Branch analysis from position: 20
Jump found. Position 1 = 21, Position 2 = 32
Branch analysis from position: 21
Jump found. Position 1 = 22, Position 2 = 32
Branch analysis from position: 22
Jump found. Position 1 = 21
Branch analysis from position: 21
Branch analysis from position: 32
Jump found. Position 1 = -2
Branch analysis from position: 32
filename:       /root/php_opcode/php_array.php
function name:  (null)
number of ops:  34
compiled vars:  !0 = $arr, !1 = $key, !2 = $value
line     #* E I O op                           fetch          ext  return  operands
-------------------------------------------------------------------------------------
```


   2     0  E >   INIT_ARRAY                                       ~0      'one'
         1        ADD_ARRAY_ELEMENT                                ~0      'two'
         2        ADD_ARRAY_ELEMENT                                ~0      'three'
         3        ASSIGN                                                   !0, ~0
   3     4        SEND_REF                                                 !0
         5        DO_FCALL                                      1          'reset'
   4     6    >   SEND_REF                                                 !0
         7        DO_FCALL                                      1  $3      'each'
         8        FETCH_DIM_R                                      $4      $3, 1
         9        ASSIGN                                                   !2, $4
        10        FETCH_DIM_R                                      $6      $3, 0
        11        ASSIGN                                                   !1, $6
        12      > JMPZ                                                     $3, ->20
   5    13    >   ADD_STRING                                       ~8      'Key%3A+'
        14        ADD_VAR                                          ~8      ~8, !1
        15        ADD_STRING                                       ~8      ~8, '%3B+Value%3A+'
        16        ADD_VAR                                          ~8      ~8, !2
        17        ADD_STRING                                       ~8      ~8, '%3Cbr+%2F%3E%0A'
        18        ECHO                                                     ~8
   6    19      > JMP                                                      ->6
   8    20    > > FE_RESET                                         $9      !0, ->32
        21    > > FE_FETCH                                         $10     $9, ->32
        22    >   OP_DATA                                          ~12     
        23        ASSIGN                                                   !2, $10
        24        ASSIGN                                                   !1, ~12
   9    25        ADD_STRING                                       ~14     'Key%3A+'
        26        ADD_VAR                                          ~14     ~14, !1
        27        ADD_STRING                                       ~14     ~14, '%3B+Value%3A+'
        28        ADD_VAR                                          ~14     ~14, !2
        29        ADD_STRING                                       ~14     ~14, '%3Cbr+%2F%3E%0A'
        30        ECHO                                                     ~14
  10    31      > JMP                                                      ->21
        32    >   SWITCH_FREE                                              $9
  12    33      > RETURN                                                   1

branch: #  0; line:     2-    4; sop:     0; eop:     5; out1:   6
branch: #  6; line:     4-    4; sop:     6; eop:    12; out1:  13; out2:  20
branch: # 13; line:     5-    6; sop:    13; eop:    19; out1:   6
branch: # 20; line:     8-    8; sop:    20; eop:    20; out1:  21; out2:  32
branch: # 21; line:     8-    8; sop:    21; eop:    21; out1:  22; out2:  32
branch: # 22; line:     8-   10; sop:    22; eop:    31; out1:  21
branch: # 32; line:    10-   12; sop:    32; eop:    33; out1:  -2
path #1: 0, 6, 13, 6, 20, 21, 22, 21, 32, 
path #2: 0, 6, 13, 6, 20, 21, 32, 
path #3: 0, 6, 13, 6, 20, 32, 
path #4: 0, 6, 20, 21, 22, 21, 32, 
path #5: 0, 6, 20, 21, 32, 
path #6: 0, 6, 20, 32, 
Key: 0; Value: one<br />
Key: 1; Value: two<br />
Key: 2; Value: three<br />
Key: 0; Value: one<br />
Key: 1; Value: two<br />
Key: 2; Value: three<br />