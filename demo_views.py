from uBricks.templator import render


# page controller
def index_view(request):
    output_test = render('demo_page.html', request=request)
    return '200 OK', [output_test.encode()]


def abc_view(request):
    print(request)
    return '200 OK', [b'<h1>ABC</h1>']


