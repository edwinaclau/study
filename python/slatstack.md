Slatstack 

file_roots:
  base:
    - /srv/salt/
  dev:
    - /srv/salt/dev
  prod:
    - /srv/salt/prod






user              nginx; 
worker_processes  {{ grains['num_cpus'] }}; 
{% if grains['num_cpus'] == 2 %} 
worker_cpu_affinity 01 10; 
{% elif grains['num_cpus'] == 4 %} 
worker_cpu_affinity 1000 0100 0010 0001; 
{% elif grains['num_cpus'] >= 8 %} 
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 10000000; 
{% else %} 
worker_cpu_affinity 1000 0100 0010 0001; 
{% endif %} 
worker_rlimit_nofile {{ grains['max_open_file'] }}; 


{% if grains['os'] == 'Ubuntu' %}
host: {{ grains['host'] }}
{% elif grains['os'] == 'CentOS' %}
host: {{ grains['fqdn'] }}
{% endif %}

 探测OS


salt '*' cmd.run "uname -r" 

批量执行命令



grains_module



四、配置pillar
    本例使用分组规则定义pillar，即不同分组引用各自的sls属性
1)定义入口top.sls
#vi /srv/pillar/top.sls
base:  
  web1group:  
    - match: nodegroup  
    - web1server  
  web2group:  
    - match: nodegroup  
    - web2server  



4)同步配置
#salt '*' state.highstate



/srv/slat/xxx软件包

   conf.sls
         xxx软件包
         xxx软件包.tar.gz
         xxx.config
         xxx.sh
         xxx.sub_config
init.sls
install.sls
vhost.sls



init.sls
    include:
           xxx.install
           xxx.conf
           xxx.


install.sls

file.managed:
   name:
   unless
   source:


extract_xxx:
  cmd.run:
      


nginx_user:
    user.present:
        name: nginx
        uid: 1501
        createhome:
         gid_

         shell:/sbin/nlogin

xxx_pkg:
       pkg.installed:
            pkgs:
                   gcc
                   openssl-devel 
                   pcre-devel
                   zlib-devel



xxx_compile:

   cmd.run:
   cwd:/tmp/xxx
   names:
            ./configure



    make
    make install


require:





cache_dir
   cmd.run
   name:
     mkdir -p /xxx/xxx/
   unless
   require:
          cmd.run:


配置管理文件 conf.sls

 include:
       xxx.install 


include:
  - nginx.install     //引用安装
{% set nginx_user = 'nginx' + ' ' + 'nginx' %}  //设置用户变量
nginx_conf:
  file.managed:   //nginx主配置文件管理
    - name: /usr/local/nginx/conf/nginx.conf
    - source: salt://nginx/files/nginx.conf
    - template: jinja
    - defaults:
      nginx_user: {{ nginx_user }}      
      num_cpus: {{grains['num_cpus']}}  //根据cpu的个数来设置nginx.conf文件
nginx_service:  //nginx服务管理
  file.managed:
    - name: /etc/init.d/nginx
    - user: root
    - mode: 755
    - source: salt://nginx/files/nginx
  cmd.run:    //将服务由chkconfig管理
    - names:
      - /sbin/chkconfig --add nginx
      - /sbin/chkconfig  nginx on
    - unless: /sbin/chkconfig --list nginx
  service.running:     //nginx是启动状态
    - name: nginx
    - enable: True
    - reload: True
    - watch:
      - file: /usr/local/nginx/conf/*.conf
nginx_log_cut:                 //nginx日志管理
  file.managed:
    - name: /usr/local/nginx/sbin/nginx_log_cut.sh
    - source: salt://nginx/files/nginx_log_cut.sh
  cron.present:             //将日志切割脚本加入crontab定时执行
    - name: sh /usr/local/nginx/sbin/nginx_log_cut.sh
    - user: root
    - minute: 10
    - hour: 0
    - require:
      - file: nginx_log_cut





使用到了pillar，根据pillar配置不同的client使用不同的配置文件，先来看pillar的配置

/srv/pillar

top.sls


vhost.sls

top.sls

vhost:
  {% if 'test8' in grains['id'] %}    //如果id中有test8字符，使用vhost_www.conf配置文件，反之使用vhost_bbs.conf配置文件
  - name: www 
    target: /usr/local/nginx/conf/vhost_www.conf
  {% else %}
  - name: bbs
    target: /usr/local/nginx/conf/vhost_bbs.conf
  {% endif %}


vhost.sls


{% for vhostname in pillar['vhost'] %}

{{vhostname['name']}}:
  file.managed:
    - name: {{vhostname['target']}}
    - source: salt://nginx/files/vhost.conf
    - target: {{vhostname['target']}}
    - template: jinja
    - defaults:
      server_name: {{grains['fqdn_ip4'][0]}} 
      log_name: {{vhostname['name']}}
    - watch_in:
      service: nginx

{% endfor %}







pillar 是 Salt 非常重要的一个组件，它用于给特定的 minion 定义任何你需要的数据， 这些数据可以被 Salt 的其他组件使用



saltstack 自带grains 可以去收集一些信息  但是默认的信息资源有限 当然你也可以去自定义采集grains信息  但是grains信息有个缺点就是 他不是实时的  你定义的这些信息 它会在你重启minion或者你在master去同步grains的时候 会去采集一次 等采集完了这个值 不会发生变化 除非你再去重复上面2个动作 或者他的值 一直不变  。