from wsgiref.simple_server import make_server
from datetime import date
from uBricks.framework import WebFramework
from routes import routes


# front controller
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'value'


fronts = [secret_front, other_front]

demo_application = WebFramework(routes, fronts)

with make_server('', 8000, demo_application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
