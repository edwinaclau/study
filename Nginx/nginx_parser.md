有比较简单例如

daemon off;



error_page 404 / 404.html;

location /abc {
     index index.html index.ht index.php;
}

locaton项目，有token /abc


Nginx如何处理指令呢？

肯定有指令结构体

  ngx_commandt_t ngx_core_commands[]  = {
              {},
			  {}
			  ngx_null_command
  }


Ngx_str_t name; //项目配置项目名称

Ngx_uint_t type; //配置

char* (*set)      回调函数
	(ngx_conf_t *cf,
	 Ngx_command_t *cmd,
	 void *conf)

Ngx_uint_t conf;  当前字段的位置

Ngx_uint_t offset  字段offset配置精确存放位置

void post;   


CORE MODULE EVENTMODULE


void **ctx数组放在ngx_modules[i]->



2 构造ngx_conf_t conf 填写几个成员变量

   void *ctx 

   ngx_uint_ module_type

   ngx_uint_cmd_type



   ngx_conf_parser(ngx_conf_t conf, xxx) 函数






   if (ngx_conf_param(&conf)) != NGX_CONF_OK {
             environ = senv;
			 ngx_destroy_cycle_pools(&conf);
			 return NULL;
   }


if (ngx_conf_parse(&conf, &cycle->conf_file)) !=
    environ = senv;
	ngx_destory_cycle_pools(&conf);
	return NULL;
	}



struct ngx_conf_s {
      char           *name;    解析指令名称
	  ngx_array_t    *args;    指令参数


	  ngx_cycle_t    *cycle; 
	  ngx_pool_t     *pool;       内存池
	  ngx_pool_t     *temp_pool;  临时内存池
	  ngx_conf_file_t  *conf_file;  解析的配置文件
	  ngx_log_t       *log;        日志

	  void           *ctx;
	  ngx_uint_t     module_type;
	  ngx_uint_t     cmd_type;

	  ngx_conf_handler_pt  handler;
	  char                *handler_conf;
};

typedef struct {

    ngx_file_t     file;
	ngx_buf_t     *buffer;
	ngx_uin_t     line;
} ngx_conf_file_t;


配置上下文ctx

Nginx 配置 分块，常见


 在 Nginx 程序解析配置文件时，每一条指令都应该记录自己所属的作用域范围，而配置文件上下文ctx 变量就是用来存放当前指令所属的作用域的。在Nginx 配置文件的各种配置块中，http 块可以包含子配置块，这在存储结构上比较复杂。


#dfine NGX_DIRECT_CONF
#define NGX_MAIN_CONF
#define NGX_ANY_CONF



 core类型模块支持指令类型


#define NGX_DIRECT_CONF
#define NGX_MAIN_CONF
#define NGX_ANY_CONF


#define NGX_HTTP_MAIN_CONF
#define NGX_HTTP_SRV_CONF
#define NGX_HTTP_LOC_CONF
#define NGX_HTTP_UPD_CONF
#define NGX_HTTP_SIF_CONF
#define NGX_HTTP_LIF_CONF
#define NGX_HTTP_LMT_CONF


 配置解析模块在src/ngx_conf_file.c
 ngx_conf_param,用来解析命令传递
 解析函数ngx_conf_parse

 支持三种不同的解析类型
 1.配置文件
 2.解析block
 3解析命令


char *
ngx_conf_parse(ngx_conf_t *cf, ngx_str_t *filename)
{
   char         *rv;
   ngx_fd_t     fd;
   ngx_int_t    rc;
   ngx_buf_t    buf;
   ngx_conf_file_t *prev, conf_file;

   enum {
         parse_file = 0,
		 parse_block,
		 parse_param
   } type;

 #if (NGX_SUPPRESS_WARN)
   fd = NGX_INVALID_FILE;
   prev = NULL;
 #endif

   if (filename) {
      
	   fd = ngx_open_file(filename->data, )
	   if (fd == NGX_INVALID_FILE) {
	        ngx_conf_log_error(NGX_LOG)
	   }

	   return NGX_CONF_ERROR;
   }

   prev = cf->conf_file;

   cf->conf_file = &conf_file;


   if (ngx_fd_info(fd, &cf-con)) {
   
   }


   cf->conf_file->buffer = &buf;

   buf.start = ngx_alloc(NGX_CONF_BUFFER,)
   if (buf.start == NULL) {
        go failed;
   }


   buf.pos = buf.start;
   buf.last = buf.start;
   buf.end = buf.last + NGX_CONF_BUFFER;
   buf.temporary = 1;


    cf->conf_file->file.fd = fd;  
        cf->conf_file->file.name.len = filename->len;  
        cf->conf_file->file.name.data = filename->data;  
        cf->conf_file->file.offset = 0;  
        cf->conf_file->file.log = cf->log;  
        cf->conf_file->line = 1;  
    

     type = parse_file;  /* 解析配置文件 */  
  
    } else if (cf->conf_file->file.fd != NGX_INVALID_FILE) {  
  
        type = parse_block; /* 解析block块 */  
  
    } else {  
        type = parse_param; /* 解析命令行配置 */  
    }  
  
  
    for ( ;; ) {  
        /* 状态机  */
        rc = ngx_conf_read_token(cf);  
  
        /* 
         * ngx_conf_read_token() may return 
         * 
         *    NGX_ERROR             there is error 
         *    NGX_OK                the token terminated by ";" was found 
         *    NGX_CONF_BLOCK_START  the token terminated by "{" was found 
         *    NGX_CONF_BLOCK_DONE   the "}" was found 
         *    NGX_CONF_FILE_DONE    the configuration file is done 
         */  
  
        if (rc == NGX_ERROR) {  
            goto done;  
        }  
  
		if (rc == NGX_CONF_BLOCK_DONE) {
		    
			if (type != parse_block) {
			    ngx_conf_log_error(NGX_LOG_EMERG)
			    goto failed;
			}


			goto done;
		}


		if (rc == NGX_CONF_FILE_DONE) {
		     
			if (type == parse_block) {
			     ngx_conf_log_error()

			}
		}


		if ( rc == NGX_CONF_BLOCK_START) {
		   
			 if (type == parse_param) {
			     ngx_conf_log_error()


			     goto failed;
			 }
		}


		if (cf->handler) {
		
		     if (rc == NGX_CONF_BLOCK_START) {
			     ngx_conf_log_error()
				 goto failed;
			 }


			 fv = (*cf->handler)(cf, NULL, cf->handler)
			 if (rv == NGX_CONF_OK) {
			     continue;
			 }

			 if (rv == NGX_CONF_ERROR) {
			       goto failed;
			 }


			 ngx_conf_log_error()

			go failed;
		}

failed:
		rc = NGX_ERROR;

done:
		 if (filename) {
		     if (cf->conf_file->buffer->start) {
			    ngx_free(cf->conf_file->buffer->start);
			 }

			 if (ngx_close(fd)) == NGX_FILE_ERROR {
			     ngx_log_error

			    return NGX_CONF_ERROR;
			 }

			 cf->conf_file = prev;
		 }


		 if (rc == NGX_ERROR) {
		     return NGX_CONF_ERROR;
		 }
       return NGX_CONF_OK;
}

 配组织解析函数源码，语法分析  指令解析

 ngx_conf_read_token() 函数完成

 1) 内置指令

 2）自定义指令

 if （cf->handler) {
 
      if (rc == NGX_CONF_BLOCK_START)
  
 }




static ngx_int_t
ngx_conf_handler(ngx_conf_t *cf, ngx_int_t last)
{
    char          *rv;
	void          *conf, **confp;
	ngx_uint_t    i, found;
	ngx_str_t     *name;
	ngx_command_t *cmd;


	name = cf->args->elts;

	found = 0;

	for ( i = 0; ngx_modules[i]; i++) {
	
	     cmd = ngx_commandles[i]->commands;
		 if (cmd == NULL) {
		     continue;
		 }

		 for ( ; cmd->name.len; cmd++) {
		      
			 if (name->len != cmd->name.len) {
			     continue;
			 }

			 if (ngx_strcmp(name->data, cmd-?))
				 continue;
		 }

		 found = 1;

		 if (ngx_modules[i]->type != NGX_CONF_MODULE)
			 && ngx_modules[i]->type != cf->module_type)
			 {
			    continue;
			 }


		 if (!(cmd->type & cf->cmd_type)) {
		     continue;
		 }


		 if (!(cmd->type && NGX_CONF_BLOCK) && last != NGX_OK)


			 return NGX_ERROR;
	}


}









struct ngx_command_s {    
    /* 配置项名称 */    
    ngx_str_t             name;    
    /* 配置项类型，type将指定配置项可以出现的位置以及携带参数的个数 */    
    ngx_uint_t            type;    
    /* 处理配置项的参数 */    
    char               *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);    
    /* 在配置文件中的偏移量，conf与offset配合使用 */    
    ngx_uint_t            conf;    
    ngx_uint_t            offset;    
    /* 配置项读取后的处理方法，必须指向ngx_conf_post_t 结构 */    
    void                 *post;    
};   

