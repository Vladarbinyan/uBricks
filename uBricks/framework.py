from .requests import get_request_params


class NotFound404:
    """If page not found"""

    def __call__(self, request):
        return '404 Not Found', f'Error 404: PAGE Not Found'


class InvalidRequestMethod:
    """If http method not supported."""

    def __call__(self, request):
        return '405 Method Not Allowed', f'Error 405: Method Not Allowed'


class WebFramework:
    """
    Конструктор
    :param routes: dict {url: view} связываем url и его представление
    :param fronts: dict {key: value} будет использоваться для передачи параметров во front controllers
    """

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    """
    Callable объект 
    :param environ: dict {key: value} словарь переменных окружения - это то что мы должны получить согласно WSGI
    :param start_response обработчик запроса, принимает два обязательных и один необязательный аргумент. 
    Первый код ответа, второй заголовки запроса
    """

    def __call__(self, environ, start_response):

        request = {}
        path = environ['PATH_INFO'] if environ['PATH_INFO'].endswith('/') else environ['PATH_INFO'] + '/'
        method = environ['REQUEST_METHOD']
        if method in ('GET', 'POST'):
            if path in self.routes:
                view = self.routes[path]
                request_params = get_request_params(environ, method)
                # собираем request
                request['method'] = method
                if method == 'POST':
                    request['data'] = request_params
                elif method == 'GET':
                    request['request_params'] = request_params
                # print(f'{method}: {request_params}')
            else:
                view = NotFound404()
        else:
            view = InvalidRequestMethod()

        for front in self.fronts:
            front(request)
        status, body = view(request)
        response_headers = [('Content-Type', 'text/html')]
        start_response(status, response_headers)
        return [body.encode('utf-8')]


# Режим отладки приложения, дублировать в консоль всё что находится в окружении запроса
class DebugApplication(WebFramework):

    def __init__(self, routes, fronts):
        self.application = WebFramework(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class FakeApplication(WebFramework):

    def __init__(self, routes, fronts):
        self.application = WebFramework(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
