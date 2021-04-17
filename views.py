from uBricks.templator import render


# page controller

class Index:
    def __call__(self, request):
        content = render('templates\index.html', data=request.get('data', None))
        return '200 OK', [content.encode()]


class About:
    def __call__(self, request):
        return '200 OK', [b'about']


class NotFound404:
    def __call__(self, request):
        return '404 Not Found', '404 PAGE Not Found'
