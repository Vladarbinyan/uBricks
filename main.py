from wsgiref.simple_server import make_server

from uBricks.framework import WebFramework
from routes import routes, fronts

demo_application = WebFramework(routes, fronts)

with make_server('', 8000, demo_application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
