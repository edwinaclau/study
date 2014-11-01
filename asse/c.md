```c
#include <stdio.h>
#include <stdlib.h>

int add(int a,int b)
{
     int c=0;
     c=a+b;
     return c;
}

int main(void)
{
     int x=0;
     int y=3;
     int z=4;
     x=add(y,z);
     return 0;
}
```
```c
        .file   "test.c" 
        .text 
.globl add 
        .type   add, @function 
add: 
        pushl   %ebp 
        movl    %esp, %ebp 
        subl    $16, %esp 
        movl    $0, -4(%ebp) 
        movl    12(%ebp), %eax 
        movl    8(%ebp), %edx 
        leal    (%edx,%eax), %eax 
        movl    %eax, -4(%ebp) 
        movl    -4(%ebp), %eax 
        leave 
        ret 
        .size   add, .-add 
.globl main 
        .type   main, @function 
main: 
        pushl   %ebp 
        movl    %esp, %ebp 
        subl    $24, %esp 
        movl    $0, -12(%ebp) 
        movl    $3, -8(%ebp) 
        movl    $4, -4(%ebp) 
        movl    -4(%ebp), %eax 
        movl    %eax, 4(%esp) 
        movl    -8(%ebp), %eax 
        movl    %eax, (%esp) 
        call    add 
        movl    %eax, -12(%ebp) 
        movl    $0, %eax 
        leave 
        ret 
        .size   main, .-main 
        .ident  "GCC: (GNU) 4.4.7 20120313 (Red Hat 4.4.7-4)" 
        .section        .note.GNU-stack,"",@progbits 
~                                                           
	

```


```c
#include <stdio.h>
#include <stdlib.h>


int main(void)
{
     int x=1;
     int *y;
     *y = x;
     return 0;
}

```

```c
      .file   "test.c"
        .text
.globl main
        .type   main, @function
main:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $16, %esp
        movl    $1, -8(%ebp)
        movl    -4(%ebp), %eax
        movl    -8(%ebp), %edx
        movl    %edx, (%eax)
        movl    $0, %eax
        leave
        ret
        .size   main, .-main
        .ident  "GCC: (GNU) 4.4.7 20120313 (Red Hat 4.4.7-4)"
        .section        .note.GNU-stack,"",@progbits
~       
```























```c

void main()  
  
{  
            int myvar = 12;  
            int *p = &myvar;  
            int **pa = &p;  
            int ***pb = &pa;  
            printf("The Value of   myvar is %8d./n" , myvar);  
            printf("The Address of myvar is %X./n" , &myvar);  
            printf("The Value of   p  is %X./n" , p);  
            printf("The Address of p  is %X./n" , &p);  
            printf("The value of *p is      %8d./n" , *p);  
            printf("The Value of   pa    is %X./n" , pa);  
            printf("The Address of pa    is %X./n" , &pa);  
            printf("The value of **pa is    %8d./n" , **pa);  
            printf("The Value of   pb    is %X./n" , pb);  
            printf("The Address of pb    is %X./n" , &pb);  
            printf("The value of ***pb is   %8d./n" , ***pb);  
}      

```
```c

.file   "test.c"
.section        .rodata
.align 4
.LC0:
        .string "The Value of   myvar is %8d./n"
.LC1:
        .string "The Address of myvar is %X./n"
.LC2:
        .string "The Value of   p  is %X./n"
.LC3:
        .string "The Address of p  is %X./n"
        .align 4
.LC4:
        .string "The value of *p is      %8d./n"
.LC5:
        .string "The Value of   pa    is %X./n"
.LC6:
        .string "The Address of pa    is %X./n"
        .align 4
.LC7:
        .string "The value of **pa is    %8d./n"
.LC8:
        .string "The Value of   pb    is %X./n"
.LC9:
        .string "The Address of pb    is %X./n"
        .align 4
.LC10:
        .string "The value of ***pb is   %8d./n"
        .text
.globl main
        .type   main, @function
main:
        pushl   %ebp
        movl    %esp, %ebp
        andl    $-16, %esp
        subl    $32, %esp
        movl    $12, 28(%esp)
        leal    28(%esp), %eax
        movl    %eax, 24(%esp)
        leal    24(%esp), %eax
        movl    %eax, 20(%esp)
        leal    20(%esp), %eax
        movl    %eax, 16(%esp)
        movl    28(%esp), %edx
        movl    $.LC0, %eax
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    $.LC1, %eax
        leal    28(%esp), %edx
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    24(%esp), %edx
        movl    $.LC2, %eax
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    $.LC3, %eax
        leal    24(%esp), %edx
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    24(%esp), %eax
        movl    (%eax), %edx
        movl    $.LC4, %eax
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    20(%esp), %edx
        movl    $.LC5, %eax
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    $.LC6, %eax
        leal    20(%esp), %edx
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    20(%esp), %eax
        movl    (%eax), %eax
        movl    (%eax), %edx
        movl    $.LC7, %eax
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    16(%esp), %edx
        movl    $.LC8, %eax
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    $.LC9, %eax
        leal    16(%esp), %edx
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        movl    16(%esp), %eax
        movl    (%eax), %eax
        movl    (%eax), %eax
        movl    (%eax), %edx
        movl    $.LC10, %eax
        movl    %edx, 4(%esp)
        movl    %eax, (%esp)
        call    printf
        leave
        ret
        .size   main, .-main
        .ident  "GCC: (GNU) 4.4.7 20120313 (Red Hat 4.4.7-4)"
        .section        .note.GNU-stack,"",@progbits  

```                                            