from wsgiref.simple_server import make_server
from uBricks.framework import WebFramework
from demo_routes import routes


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'value'


fronts = [secret_front, other_front]

demo_application = WebFramework(routes, fronts)

with make_server('', 8000, demo_application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
