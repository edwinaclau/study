

中间 middleware


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


就是过滤 穿透过来。。。。


process_request()
process_view()
During the response phase, after calling the view, middleware are applied in reverse order, from the bottom up. Three hooks are available:

process_exception() (only if the view raised an exception)
process_template_response() (only for template responses)
process_response()




