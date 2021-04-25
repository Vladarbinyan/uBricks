import quopri


class NotFound404:
    """If page not found"""

    def __call__(self, request):
        return '404 Not Found', [b'Error 404: PAGE Not Found']


class InvalidRequestMethod:
    """If http method not supported."""

    def __call__(self, request):
        return '405 Method Not Allowed', [b'Error 405: Method Not Allowed']


def parse_input_data(data):
    result = {}
    if data:
        # делим параметры через &
        params = data.split('&')
        for item in params:
            # делим ключ и значение через =
            k, v = item.split('=')
            # Приводим строковые значения к RFC 1522 чтобы декодировать
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            result[k] = val_decode_str
    return result


def get_wsgi_input_data(env) -> bytes:
    # получаем длину тела
    content_length_data = env.get('CONTENT_LENGTH')
    # приводим к int
    content_length = int(content_length_data) if content_length_data else 0
    # считываем данные если они есть
    data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
    return data


def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        # декодируем данные
        data_str = data.decode(encoding='utf-8')
        # собираем их в словарь
        result = parse_input_data(data_str)
    return result


def get_request_params(env, method):
    if method == 'GET':
        query_string = env['QUERY_STRING']
        data = parse_input_data(query_string)
        return data

    elif method == 'POST':
        data = parse_wsgi_input_data(get_wsgi_input_data(env))
        return data
    else:
        return {}


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
            if path in self.routes:
                view = self.routes[path]
                request_params = get_request_params(environ, method)
                print(f'{method}: {request_params}')
            else:
                view = NotFound404()
        else:
            view = InvalidRequestMethod()

        # front controllers
        request = {}
        for front in self.fronts:
            front(request)
        status, body = view(request)
        response_headers = [('Content-Type', 'text/html')]
        start_response(status, response_headers)
        return body
