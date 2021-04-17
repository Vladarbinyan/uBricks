import cgi


def not_found_404(request):
    """If page not found"""
    return '404 Not Found', [b'Error 404: PAGE Not Found']


def invalid_request(request):
    """If http method not supported."""
    return [b'Error 405: Method Not Allowed']


def parse_input_data(data):
    result = {}
    if data:
        # делим параметры через &
        params = data.split('&')
        for item in params:
            # делим ключ и значение через =
            k, v = item.split('=')
            result[k] = v
    return result


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

        path = environ['PATH_INFO'] if environ['PATH_INFO'].endswith('/') else environ['PATH_INFO'] + '/'
        method = environ['REQUEST_METHOD']
        if method in ('GET', 'POST'):
            print(path)
            if path in self.routes:
                view = self.routes[path]
                print('method', method)
                parsed = cgi.parse(environ)
                print(parsed)
                # получаем параметры запроса
                query_string = environ['QUERY_STRING']
                print(query_string)
                # превращаем параметры в словарь
                request_params = parse_input_data(query_string)
                print(request_params)
            else:
                view = not_found_404
        else:
            view = invalid_request

        # front controllers
        request = {}
        for front in self.fronts:
            front(request)
        status, body = view(request)
        response_headers = [('Content-Type', 'text/html')]
        start_response(status, response_headers)
        return body
