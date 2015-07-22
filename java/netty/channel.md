Channel 
ChannelPipeline，
ByteBuf 
Handler 


Channel 网线

ChannelPipeline  交换机的通道

ChannelBuffer  数据


当前channel的状态（比如是否open，connected） 
当前channel的配置参数（比如receive buffer size） 
当前channel支持的操作（比如read, write, connect, and bind）




ChannelFuture 是 利用 concurrent.Future扩展


Channel有一个parent。比如，SocketChannel是ServerSocketChannel的"accept方法"的返回值（ServerSocketChannel中并没有accept方法，但是在ServerSocket中是存在的）。所以，SocketChannel的 parent()返回ServerSocketChannel。



ChannelPipeline  网线，处理所有数据的请求
每个ChannelHandler接口的实现类完成了一定的功能


ServerSocketChannel, SocketChannel, ByteBuffer 


由不同的 情况 交到 Channel工厂产生不同类型的Channel

例如NioServerSocketChannel



java.nio.SocketChannel 和 java.nio.ServerSocketChannel

io.netty.channel.Channel 是Netty抽象 

读 写 建立连接， 关闭连接，


socketChannel      ServerSocketChannel


JDK SocketChannel   ServerSocketChannel

自定义的Channel


remoteAddress()

read()

isOpen()

isActive()

metaData()

localAddress()

remoteAddress()

closeFuture()
disconnect()

close()

bind(SocketAdddress, ChannelPromise)

connect
write(Object)
write(Object, ChannelPromise)
writeAndFlush
writeAndFlush(object)



1.eventLoop() Channel 需要注册到EventLoop() 多路复用器


2.metadata()方法 , 创建Socket 指定TCP参数3


3.parent channel 一般 parent为空,对于客户端
就是创建它的ServerSocketChannel

4. 用户获取Channel 标识的id(), 它返回 ChannelId对象
ChannelId 是Channel 唯一标识，




Channel是顶层接口，继承了AttributeMap, ChannelOutboundInvoker, ChannelPropertyAccess, Comparable<Channel>


ChannelPipeline 是ChannelHandler的容器:

一个Channel包含一个 ChannelPipeline


ChannelHandler: ChannelUpstreamHandler和ChannelDownstreamHandler,Handler是互相独立的


ChannelSink.eventSunk，可以接受任意ChannelEvent