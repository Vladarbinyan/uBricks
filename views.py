from uBricks.templator import render


# page controller

class Index:
    def __call__(self, request):
        content = render('index.html', data=request.get('data', None))
        return '200 OK', [content.encode()]


class Contact:
    def __call__(self, request):
        content = render('contact.html')
        return '200 OK', [content.encode()]


class About:
    def __call__(self, request):
        content = render('about.html')
        return '200 OK', [content.encode()]
