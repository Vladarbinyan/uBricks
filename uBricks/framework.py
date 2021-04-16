def not_found_404_view(request):
    print(request)
    return '404 Not Found', [b'404 PAGE Not Found']


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
        path = environ['PATH_INFO']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view
        request = {}
        # front controller
        for front in self.fronts:
            front(request)
        status, body = view(request)
        response_headers = [('Content-Type', 'text/html')]
        start_response(status, response_headers)
        return body
