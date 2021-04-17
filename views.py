from uBricks.templator import render


# page controller

class Index:
    def __call__(self, request):
        content = render('templates\\index.html', data=request.get('data', None))
        return '200 OK', [content.encode()]


class Contact:
    def __call__(self, request):
        content = render('templates\\contact.html')
        return '200 OK', [content.encode()]


class About:
    def __call__(self, request):
        return '200 OK', [b'<h2>about<h2>']
