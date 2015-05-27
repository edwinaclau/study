##php的for测试


###code

```

<?php

  $arr = array('adf','fda','fdas','zdcvzv','vcvdf','oij');

  //for循禄路卤茅
  for($temp = 0;$temp < count($arr);$temp++){
   echo "$arr[$temp]<br/>";
  }
?>
```
    



```
Finding entry points
Branch analysis from position: 0
Jump found. Position 1 = 20, Position 2 = 15
Branch analysis from position: 20
Jump found. Position 1 = -2
Branch analysis from position: 15
Jump found. Position 1 = 12
Branch analysis from position: 12
Jump found. Position 1 = 8
Branch analysis from position: 8
filename:       /root/php_opcode/php_array.php
function name:  (null)
number of ops:  21
compiled vars:  !0 = $arr, !1 = $temp
line     #* E I O op                           fetch          ext  return  operands
-------------------------------------------------------------------------------------
   5     0  E >   INIT_ARRAY                                       ~0      'adf'
         1        ADD_ARRAY_ELEMENT                                ~0      'fda'
         2        ADD_ARRAY_ELEMENT                                ~0      'fdas'
         3        ADD_ARRAY_ELEMENT                                ~0      'zdcvzv'
         4        ADD_ARRAY_ELEMENT                                ~0      'vcvdf'
         5        ADD_ARRAY_ELEMENT                                ~0      'oij'
         6        ASSIGN                                                   !0, ~0
   8     7        ASSIGN                                                   !1, 0
         8    >   SEND_VAR                                                 !0
         9        DO_FCALL                                      1  $3      'count'
        10        IS_SMALLER                                       ~4      !1, $3
        11      > JMPZNZ                                       15          ~4, ->20
        12    >   POST_INC                                         ~5      !1
        13        FREE                                                     ~5
        14      > JMP                                                      ->8
   9    15    >   FETCH_DIM_R                                      $6      !0, !1
        16        ADD_VAR                                          ~7      $6
        17        ADD_STRING                                       ~7      ~7, '%3Cbr%2F%3E'
        18        ECHO                                                     ~7
  10    19      > JMP                                                      ->12
  12    20    > > RETURN                                                   1

branch: #  0; line:     5-    8; sop:     0; eop:     7; out1:   8
branch: #  8; line:     8-    8; sop:     8; eop:    11; out1:  20; out2:  15
branch: # 12; line:     8-    8; sop:    12; eop:    14; out1:   8
branch: # 15; line:     9-   10; sop:    15; eop:    19; out1:  12
branch: # 20; line:    12-   12; sop:    20; eop:    20; out1:  -2
path #1: 0, 8, 20,
path #2: 0, 8, 15, 12, 8, 20, 



```