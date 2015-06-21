chapter9


进程地址空间


 页和页面调度

     内存管理单元(MMU)
	  虚拟空间由多个页组成

      32位地址空间包含约100W的页，而


	  这些页可能没有任何意义，一般有两种状态，无效(invalid) 和 有效(valid)

	  地址空间 不需要是连续的。虽然是线性编址，实际


	  如果一个有效的页 和 二级存储数据相关，


	 共享 和 写时复制

        虚拟内存中的多个页面，甚至是属于不用级才能呢的虚拟地址空间，可能会映射到一个物理页面



	两个进程可能会映射到大数据库的内存中，


	共享的数据可能是只读，只写，或者可读可写。 一个进程试读写某个


	最简单是内核允许写



	内存区域

	    很多页组成了块(blocks) ,例如读写权限，存区域(memoery regions), 段(segments), 映射(mappings)



	文本段(text segment) 包含作者一个进程的代码，字符串，常量和 一些只读数据

	堆栈段(stack)  一个进程的执行栈,栈会动态伸长 和 收缩

	数据段(data segment) 一个进程的动态内存空间，


	BSS段(bss segment) 包含了没有被初始化的全局变量



动态内存分配


   内存通过 自动变量 和 静态变量获得



#include <stdlib.h>
 
  void * malloc(size_t size);

  获得size大小的内存区域，并指向新的内存首地址，这块内存没有定义，不能当作0来处理

  失败时，malloc() 返回NULL,并把errno值设置为ENOMEM


  malloc() 使用简单

  char *p;

  p = malloc (2048);
  if (!p) 
	perror ("malloc");

  失败时，malloc() 会返回NULL,并把errno 值 设置为ENOMEM




  数组分配
    当按需所分，动态分配内存就会更加复杂，一个很好的例子是为了数组分配动态内存
	其中数组元素是固定大小，分配元素是动态变化

#include <stdlib.h>

void * calloc (size_t nr, size_t size);


调用calloc() 成功时会返回一个指针，指向一块可以存储下整个数组的内存(nr个元素，每个为size个字节)


	int *x, *y;

	x = malloc( 50 * sizeof (int));
	if (!x) {
	     perror("malloc");
		 return -1;
	}

    if (!y) {
	      perror("calloc");
		  return -1;
	}

calloc 将分配的区域全都用0进行初始化，y中50个元素被赋值为0
        但x 数组的元素 是 未定义的，



memset()


vod *malloc0 (size_t size)
{
  return calloc(1, size);
}


void * xmalloc0 (size_t size)
{
   void *p;

   p - calloc (1, size);

   if (!p) {
           perror("xmalloc0");
		   exit (EXIT_FAILURE);
   }
   return p;

}



void *realloc (void *ptr, size_t size);

 #include <stdlib.h>

realloc 会把ptr 指向的内存区域的大小 变为 size 字节


如果size 是 0 ，其效果就和ptr 上调用free() 相同

ptr 是NULL ,调用realloc() 结果 就和 malloc() 一样


struct map  *p;

p = calloc (2, sizeof (struct map));
if (!p) {
     perror ("calloc");
	 return -1;
}

realloc() 调用后，



释放动态内存

  对于自动分配的内存，当栈不再使用，空间会自动释放
  
  #include <stdlib.h>
  void free (void *ptr);

free 会释放ptr 所指向的内存，ptr必须通过调用malloc(),calloc() 或者 realloc


void print_chars (int n, char c) 
{
   int i;

   for (i = 0; i < n; i++) {
         char *s;
		 int j;


		 s = calloc(i + 2, 1);
		 if (!s) {
		      perror("calloc");
			  break;
		 }


		 for (j = 0; j < i; j++) 
			 s[j] = c;

		 printf("%s\n", s);


		 free(s);
   }
}


n个字符数组分配了空间，这n个数组的元素个数依次递增



对齐

  数据对齐(alignment) 内存中存储排列
    
  数据对齐和系统，体系CPU都有所不同的


   预对齐内存的分配

    #include <stdlib.h>

   int posix_memalign (void **memptr,
		               size_t alignment,
					   size_t size);

调用成功时，会返回size 字节的动态内存, 并保证是按照alignment进行对齐

参数alignment 必须是2的整数幂，并且是void 指针大小的整数倍，

调用

