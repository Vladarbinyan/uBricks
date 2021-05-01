from datetime import date



# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'value'


fronts = [secret_front, other_front]


