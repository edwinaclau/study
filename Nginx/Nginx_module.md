Nginx是由许多模块构成的，在Nginx中，使用全局数组ngx_modules保存和管理所有Nginx的模块。



必须安装的模块是保证Nginx正常功能的模块，没得选择，这些模块会出现在ngx_modules里。比如ngx_core_module
可以安装的模块通过configure的配置和系统环境，被有选择的安装，这些模块里，被选择安装的模块会出现在ngx_modules数组中。

#include <ngx_config.h>
#include <ngx_core.h>
ngx_module_t *ngx_modules[] = {
    &ngx_core_module,
    
    &ngx_conf_module,
    &ngx_errlog_module,
    &ngx_events_module,
    &ngx_event_core_module,
    &ngx_epoll_module,
    &ngx_regex_module,
    &ngx_http_module,
    &ngx_http_core_module,
    &ngx_http_log_module,
    &ngx_http_upstream_module,
    &ngx_http_static_module,
    &ngx_http_autoindex_module,
    &ngx_http_index_module,
 
    NULL
};


for (i = 0; ngx_modules[i]; i++) {
    ...
}



struct ngx_module_s {
    ngx_uint_t            ctx_index;
    ngx_uint_t            index;

    ngx_uint_t            spare0;
    ngx_uint_t            spare1;
    ngx_uint_t            spare2;
    ngx_uint_t            spare3;

    ngx_uint_t            version;

    void                 *ctx;
    ngx_command_t        *commands;
    ngx_uint_t            type;

    ngx_int_t           (*init_master)(ngx_log_t *log);

    ngx_int_t           (*init_module)(ngx_cycle_t *cycle);

    ngx_int_t           (*init_process)(ngx_cycle_t *cycle);
    ngx_int_t           (*init_thread)(ngx_cycle_t *cycle);
    void                (*exit_thread)(ngx_cycle_t *cycle);
    void                (*exit_process)(ngx_cycle_t *cycle);

    void                (*exit_master)(ngx_cycle_t *cycle);

    uintptr_t             spare_hook0;
    uintptr_t             spare_hook1;
    uintptr_t             spare_hook2;
    uintptr_t             spare_hook3;
    uintptr_t             spare_hook4;
    uintptr_t             spare_hook5;
    uintptr_t             spare_hook6;
    uintptr_t             spare_hook7;
};



1. type

#define NGX_CORE_MODULE      0x45524F43  /* "CORE" */
#define NGX_CONF_MODULE      0x464E4F43  /* "CONF" */
#define NGX_EVENT_MODULE     0x544E5645  /* "EVNT" */
#define NGX_HTTP_MODULE      0x50545448  /* "HTTP" */
#define NGX_MAIL_MODULE      0x4C49414D  /* "MAIL" */

2.index

    ngx_max_module = 0;
    for (i = 0; ngx_modules[i]; i++) {
        ngx_modules[i]->index = ngx_max_module++;
    }


3. ctx_index

   ngx_event_max_module = 0;
    for (i = 0; ngx_modules[i]; i++) {
        if (ngx_modules[i]->type != NGX_EVENT_MODULE) {
            continue;
        }
        ngx_modules[i]->ctx_index = ngx_event_max_module++;
    }


4. ctx

ctx是void *指针型变量，这是指向与模块相关的上下文。

这里先解释一下什么叫与模块相关的上下文。


static ngx_core_module_t  ngx_core_module_ctx = {
    ngx_string("core"),
    ngx_core_module_create_conf,
    ngx_core_module_init_conf
};



typedef struct {
    ngx_str_t             name;
    void               *(*create_conf)(ngx_cycle_t *cycle);
    char               *(*init_conf)(ngx_cycle_t *cycle, void *conf);
} ngx_core_module_t;


ngx_module_t ngx_core_module：用来表示模块本身，保存在ngx_modules数组中；
ngx_core_conf_t core_conf：用来保存对该模块的配置信息；
ngx_core_module_t ngx_core_module_ctx：用来初始化ngx_core_conf_t中的成员变量；


6. commands

commands是ngx_command_t数组，表示一组配置文件中的可配项（指令）。

例如，在配置文件nginx.conf中worker_processes 1;对应commands数组中的一项，该项的定义如下,类型为ngx_command_t：

{ ngx_string("worker_processes"),
      NGX_MAIN_CONF|NGX_DIRECT_CONF|NGX_CONF_TAKE1,
      ngx_set_worker_processes,
      0,
      0,
      NULL }
其中ngx_command_t定义如下：

struct ngx_command_s {
    ngx_str_t             name;
    ngx_uint_t            type;
    char               *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
    ngx_uint_t            conf;
    ngx_uint_t            offset;
    void                 *post;
};



明显的ngx模块结构体，大家的一个基类


然后按照不同模块特点自己编写，ngx_<module name>_conf_t结构体

command可以定义指令

初始化---->用来表示该模块可以在配置文件中配置的项目--->回调指令函数