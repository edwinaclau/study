这个模块就是兼容为主



author__ = "Benjamin Peterson <benjamin@python.org>"
__version__ = "1.9.0"


# Useful for very coarse version differentiation.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

    if sys.platform.startswith("java"):
        # Jython always uses 32 bits.
        MAXSIZE = int((1 << 31) - 1)
    else:
        # It's possible to have sizeof(long) != sizeof(Py_ssize_t).
        class X(object):
            def __len__(self):
                return 1 << 31
        try:
            len(X())
        except OverflowError:
            # 32-bit
            MAXSIZE = int((1 << 31) - 1)
        else:
            # 64-bit
            MAXSIZE = int((1 << 63) - 1)
        del X


  MovedAttribute("urlopen", "urllib2", "urllib.request"),
    MovedAttribute("install_opener", "urllib2", "urllib.request"),
    MovedAttribute("build_opener", "urllib2", "urllib.request"),
    MovedAttribute("pathname2url", "urllib", "urllib.request"),
    MovedAttribute("url2pathname", "urllib", "urllib.request"),
    MovedAttribute("getproxies", "urllib", "urllib.request"),
    MovedAttribute("Request", "urllib2", "urllib.request"),



Name	Python 2 name	Python 3 name
builtins	__builtin__	builtins
configparser	ConfigParser	configparser
copyreg	copy_reg	copyreg
cPickle	cPickle	pickle
cStringIO	cStringIO.StringIO()	io.StringIO
dbm_gnu	gdbm	dbm.gnu
_dummy_thread	dummy_thread	_dummy_thread
email_mime_multipart	email.MIMEMultipart	email.mime.multipart
email_mime_nonmultipart	email.MIMENonMultipart	email.mime.nonmultipart
email_mime_text	email.MIMEText	email.mime.text
email_mime_base	email.MIMEBase	email.mime.base
filter	itertools.ifilter()	filter()
filterfalse	itertools.ifilterfalse()	itertools.filterfalse()
http_cookiejar	cookielib	http.cookiejar
http_cookies	Cookie	http.cookies
html_entities	htmlentitydefs	html.entities
html_parser	HTMLParser	html.parser
http_client	httplib	http.client
BaseHTTPServer	BaseHTTPServer	http.server
CGIHTTPServer	CGIHTTPServer	http.server
SimpleHTTPServer	SimpleHTTPServer	http.server
input	raw_input()	input()
intern	intern()	sys.intern()
map	itertools.imap()	map()
queue	Queue	queue
range	xrange()	range
reduce	reduce()	functools.reduce()
reload_module	reload()	imp.reload()
reprlib	repr	reprlib
shlex_quote	pipes.quote	shlex.quote
socketserver	SocketServer	socketserver
_thread	thread	_thread
tkinter	Tkinter	tkinter
tkinter_dialog	Dialog	tkinter.dialog
tkinter_filedialog	FileDialog	tkinter.FileDialog
tkinter_scrolledtext	ScrolledText	tkinter.scrolledtext
tkinter_simpledialog	SimpleDialog	tkinter.simpledialog
tkinter_ttk	ttk	tkinter.ttk
tkinter_tix	Tix	tkinter.tix
tkinter_constants	Tkconstants	tkinter.constants
tkinter_dnd	Tkdnd	tkinter.dnd
tkinter_colorchooser	tkColorChooser	tkinter.colorchooser
tkinter_commondialog	tkCommonDialog	tkinter.commondialog
tkinter_tkfiledialog	tkFileDialog	tkinter.filedialog
tkinter_font	tkFont	tkinter.font
tkinter_messagebox	tkMessageBox	tkinter.messagebox
tkinter_tksimpledialog	tkSimpleDialog	tkinter.simpledialog
urllib.parse	See six.moves.urllib.parse	urllib.parse
urllib.error	See six.moves.urllib.error	urllib.error
urllib.request	See six.moves.urllib.request	urllib.request
urllib.response	See six.moves.urllib.response	urllib.response
urllib.robotparser	robotparser	urllib.robotparser
urllib_robotparser	robotparser	urllib.robotparser
UserDict	UserDict.UserDict	collections.UserDict
UserList	UserList.UserList	collections.UserList
UserString	UserString.UserString	collections.UserString
winreg	_winreg	winreg
xmlrpc_client	xmlrpclib	xmlrpc.client
xmlrpc_server	SimpleXMLRPCServer	xmlrpc.server
xrange	xrange()	range
zip	itertools.izip()	zip()
zip_longest	itertools.izip_longest()	itertools.zip_longest()




官网参考

http://pythonhosted.org/six/index.html#module-six