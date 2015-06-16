/etc/puppet/mainfests/site.pp


import 'nodes.pp'
 $puppetserver = 'vmserver62'




# cat /etc/puppet/manifests/noded.pp
 node 'vmclient63' {               ---说明在哪一个节点生效
 include sudo                            --读取sudo模块
 }






[root@vmserver62 manifests]
# vi /etc/puppet/modules/sudo/manifests/init.pp
class sudo {
    package { sudo: ensure => present }             ---判断sudo是否安装，没有就安装
    file { "/etc/sudoers":                          ---文件资源
        owner => "root",                            ---文件所属人员
        group => "root",
        mode => 0440,                               ---文件的权限
        source => "puppet:///modules/sudo/etc/sudoers",    ---定义配置文件sudoers从puppet服务器读取，从：/etc/puppet/modules/sudo/files/etc/sudoers 读取文件，模块目录files为文件类型资源的根目录
        require => Package["sudo"] }           ---定义依赖，需要执行package，才能执行这一步
}


很明显是三个步骤安装--->配置--->服务启动

mysql:install

mysql::config

mysql::service子类


# vi /etc/puppet/modules/mysql/manifests/install.pp
class mysql::install {
    package { "mysql-server":           ---yum安装mysql-server包
                ensure => present,
                require => User["mysql"]            ---定义mysql用户为mysql
    }
    user { "mysql":
            ensure => present,                  ---判断是否有mysql用户，没有就创建
            comment => "MySQL user",       ---用户的描述信息
            gid => "mysql",
            shell => "/sbin/nologin",                         ---mysql用户的shell信息
            require => Group["mysql"]             ---定义依赖的group资源中的mysql组
    }
    group { "mysql":
            ensure => present
    }
}



mainifests目录中创建mysql类

class mysql {
    include mysql::install,mysql::config,mysql::service
}


