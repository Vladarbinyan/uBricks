from datetime import date
from views import Index, About, Contact, CoursesList, CategoryList, CreateCategory, CreateCourse, CopyCourse, StudyPrograms


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'value'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/courses/': CoursesList(),
    '/categories/': CategoryList(),
    '/create-category/': CreateCategory(),
    '/create-course/': CreateCourse(),
    '/copy-course/': CopyCourse(),
    '/study_programs/': StudyPrograms(),
}
