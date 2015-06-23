ifconfig

sudo ethtool eht0|egrep 'Sppend|Duplex'

w
平均负载反应当前运行状态

每5秒统计一次

如果多CPU，Linux会先对每个CPU进行平均运算




df -h 
查看挂载盘，总容量，和使用量，Inode的总量


mkfs格式化的时候,inode自动分配完成,block/bytes/inode来自动计算
-N参数来指定一个值

dd if=/dev/zero of =disk.img count=1024 bs=1024KB
mkfs.ext2 -N 50000 -b  -I

最小和最大



ps auxfww输出


VSZ(virtual Memory Size)
进程可以占用内存地址空间大小
RSS(Resident Set Size)
进程实际占用内存空间大小

pmap -d 




free

vmstat

内存情况，si和so,两列一直都是0,说明swap没有真正的I/O动作

sysctl中有一个参数,vm.swappiness 默认为60

netstat -plnt


netstat -tan | awk '$4~:80$/{++state[$NF]} END {for(key in state) print key,"\t",state[key]}'

计算当前80端口网络连接数


netstat -st | grep conn



iostat -x

rrqm/s
wrqm/s
r/s
w/s
rsec/s
wsec/s


IOPS(input/output Operations per second)
5400              50 ~ 80
7200   



多块磁盘组



IOPS 影响最大的一个因素，而RAID级别

IOPS = d x dIOPS
       ---------
       %r + (F x %w)

d:    磁盘数
dIOPS 每块盘的IOPS
%r    读负载的百分比
%w    写负载百分比
F: 


%r =     rd



sar


dstat

lspci -vvv | grep MSI
cat /proc/interrrups | grep eth




mtr





stap -ve 'probe begin{ log("hello world") exit() }'


kernel.function("sys_sync").call


kernel.function("sys_syc").return

syscall.read

kernel.function(



目标变量$$vars 打印probe点处的每个变量

stap在这里会区分变量类型,

$$vars,打印probe 处的每个变量，

$$locals $$vars 子集,仅打印local 变量
$$parms  $$vars 子集,仅包含函数参数

$$return 

stap -e 'probe kernel.function("vfs_read") {printf(""}

nginx-systemtap





SmokePing