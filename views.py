from uBricks.templator import render
from patterns.creational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


# page controller

class Index:
    def __call__(self, request):
        content = render('index.html', data=request.get('data', None))
        return '200 OK', content


class Contact:
    def __call__(self, request):
        content = render('contact.html')
        return '200 OK', content


class About:
    def __call__(self, request):
        content = render('about.html')
        return '200 OK', content


class NotFound404:
    """If page not found"""

    def __call__(self, request):
        return '404 Not Found', f'Error 404: PAGE Not Found'


# контроллер - Расписания
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('categories.html', objects_list=site.categories)


# контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create-category.html', categories=categories)


# контроллер - список курсов
class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('courses.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('courses.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - копировать курс
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('courses.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
