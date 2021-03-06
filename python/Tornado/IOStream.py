"""Utility classes to write to and read from non-blocking files and sockets.

Contents:

* `BaseIOStream`: Generic interface for reading and writing.
*  读写的接口 
* `IOStream`: Implementation of BaseIOStream using non-blocking sockets.
* IOStream 接口 BaseIOStream,使用非阻塞的sockets
* `SSLIOStream`: SSL-aware version of IOStream.
* SSL
* `PipeIOStream`: Pipe-based IOStream implementation.
* 管道 IOStream
"""


 绑定 socket


 绑定ioloop

 read_buffer


 write_buffer


 class IOStream(object):

	   self.io_loop = io_loop or ioloop.IOLoop.current()
        self.max_buffer_size = max_buffer_size or 104857600
        self.read_chunk_size = read_chunk_size
        self.error = None
        self._read_buffer = collections.deque()
        self._write_buffer = collections.deque()
        self._read_buffer_size = 0
        self._write_buffer_frozen = False
        self._read_delimiter = None
        self._read_regex = None
        self._read_bytes = None
        self._read_until_close = False
        self._read_callback = None
        self._streaming_callback = None
        self._write_callback = None
        self._close_callback = None
        self._connect_callback = None
        self._connecting = False
        self._state = None
        self._pending_callbacks = 0
        self._closed = False




  首先注册再回调


  read_util    read_bytes

  self._run_callback(callback, self._consume(data_length)) 执行回调


  _read_to_buffer 过程截取数据的方法不同

  read_until 读取到delimiter终止



  read_unitl_regex 相当于 delimiter 正则 表达式的read_until

  read_until_close

  read_until_close

  write ---> buffer

  write_buffer

  def _handle_events(self, fd, events):


  def _add_io_state(self, state):

  def _consume(self, loc) 合并读缓冲区loc个字节

