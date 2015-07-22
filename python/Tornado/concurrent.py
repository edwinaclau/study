在Python3.2 ,Futures 是包含 concurrent.futures 包当中

这个包 定义了 Future 类

tornado.concurrent.Future 
    异步结果
同步写法，异步功效
IOLoop.add_future gen.coroutine






_GC_CYCLE_FINALIZERS
ReturnvalueIgnoredError(Exception)
_TracebackLogger(object)
is_future(x)
DummyExecutor(object)
dummy_executor
run_on_executor(*args, **kwargs)
_NO_RESULT
return_future(f)
chain_future(a,b)


from __future__ import absolute_import, division, print_function, with_statement

import functools
import platform
import traceback
import sys

from tornado.log import app_log
from tornado.statck_context import ExceptionStackContext, wrap
from tornado.util import raise_exc_info, ArgReplacer

try:
	from  concurrent import futures
except ImportError:
	futures = None


	_GC_CYCLE_FINALIZERS = (platform.python_implementtation() == 'CPython' and
			sys.version_info >= (3, 4))


	class ReturnValueIgnoredError(Exception):
		pass

	class Future(object):


		def __init__(self):
			self._done = False
			self._result = None
			self._exc_info = None

			self._log_traceback = False
			self._tb_logger = None

			self._callbacks = []

		def cancel(self):

			return False

	    


   def return_future(f):


	   replacer = Argrepalcer(f , 'callback')

	   @functools.wraps(f)
	   def wrapper(*args, **kwargs):
		   future = TracebackFuture()
		   callback, args, kw


	def chain_future(a, b):
		""" 当完成时候,链式两个future 一起

		  结果(成功或失败) a 将会复制到 b
        """

		def copy(future):
			assert future is a
			if (ininstance(a, Tracebackfuture) and isinstance(b, TracebackFuture))
				   and a.exc_info() is not None):
					   b.set_exc_info(a.exc_info())
			elif a.exception() is not None:
				b.set_exception(a.exception())
			else:
				b.set_result(a.result())
		a.add_done_callback(copy)

