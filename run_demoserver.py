from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from uBricks.framework import WebFramework
from demo_routes import routes


<<<<<<< HEAD

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults

# def simple_app(environ, start_response):
#     setup_testing_defaults(environ)
#
#     status = '200 OK'
#     headers = [('Content-type', 'text/plain; charset=utf-8')]
#
#     start_response(status, headers)
#
#     ret = [("%s: %s\n" % (key, value)).encode("utf-8")
#            for key, value in environ.items()]
#     return ret

# Front controllers

=======
>>>>>>> step1
def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'value'


fronts = [secret_front, other_front]

demo_application = WebFramework(routes, fronts)

with make_server('', 8000, demo_application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
