GRO 作用，GRO要软硬都支持，内核和硬件本身

GRO和TSO 比较相似，TSO支持发送数据包

tcp层大的段会在网卡分割，传送过去，
如果没有GRO ，又是小的短就会一个一个送到协议栈



GRO在接收端，一个 逆向的动作，将TSO切好的包，合并成一个
大包发送给传递协议栈


GRO调用了NAPI




GRO主要就是将一个大的数据包(skb) 给协议栈

Scatter_gather IO 

skb的struct skb_shared_info


gro_receive是将输入skb尽量合并到我们gro_list中。

gro_complete则是当我们需要提交gro合并的数据包到协议栈时被调用的。

http://en.wikipedia.org/wiki/Large_segment_offload