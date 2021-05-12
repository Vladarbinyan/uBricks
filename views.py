from datetime import date
from uBricks.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import ListView, CreateView, BaseSerializer, EmailNotifier, SmsNotifier
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.architectural_system_pattern_mappers import MapperRegistry

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
student_mapper = MapperRegistry.get_current_mapper('student')
course_mapper = MapperRegistry.get_current_mapper('course')
category_mapper = MapperRegistry.get_current_mapper('category')
subscribers_mapper = MapperRegistry.get_current_mapper('subscribers')

"""
Перенесли определение маршрутов в представления, будем использовать декоратор AppRoute, обернув в него все имеющиеся 
представления. Декоратор сработеат при импорте модуля views, и произойдет заполнение словаря с маршрутами (routes)
"""
routes = {}


# page controller
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        content = render('index.html', objects_list=site.categories)
        return '200 OK', content


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        content = render('contact.html')
        return '200 OK', content


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        content = render('about.html')
        return '200 OK', content


class NotFound404:
    """If page not found"""

    def __call__(self, request):
        return '404 Not Found', f'Error 404: PAGE Not Found'


# контроллер - Расписания
@AppRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', date=date.today())


# контроллер - список категорий
@AppRoute(routes=routes, url='/categories/')
class CategoryListView(ListView):
    template_name = 'categories.html'

    def get_queryset(self, *request):
        return category_mapper.all()


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CategoryCreateView(CreateView):
    template_name = 'create-category.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_category(name)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


# контроллер - список курсов
@AppRoute(routes=routes, url='/courses/')
class CourseListView(ListView):
    template_name = 'courses.html'

    def get_context_data(self, request):
        print(request)
        context = super().get_context_data(request)
        category = category_mapper.find_by_id(int(request['request_params']['category_uuid']))
        context['name'] = category.name
        context['category_uuid'] = category.uuid
        return context

    @Debug(name='CourseListView')
    def get_queryset(self, *request):
        logger.log('Список курсов')
        request = request[0]
        category = category_mapper.find_by_id(int(request['request_params']['category_uuid']))
        return course_mapper.all_by_category(category)


# контроллер - создать курс
@AppRoute(routes=routes, url='/create-course/')
class CourseCreateView(CreateView):
    template_name = 'create-course.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        category = category_mapper.find_by_id(int(request['request_params']['category_uuid']))
        context['name'] = category.name
        context['category_uuid'] = category.uuid
        return context

    def create_obj(self, data: dict):
        category_uuid = data['category_uuid']
        category_uuid = site.decode_value(category_uuid)
        category = category_mapper.find_by_id(category_uuid)
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_course('record', name, category)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()
        # Добавляем наблюдателей на курс
        # course.observers.append(email_notifier)
        # course.observers.append(sms_notifier)


# контроллер - копировать курс
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
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


@AppRoute(routes=routes, url='/students/')
class StudentListView(ListView):
    template_name = 'students.html'

    @Debug(name='StudentListView')
    def get_queryset(self, *request):
        logger.log('Список студентов')
        return student_mapper.all()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['courses'] = course_mapper.all()
        context['students'] = student_mapper.all()
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_uuid = data['student_uuid']
        student_uuid = site.decode_value(student_uuid)
        student = student_mapper.find_by_id(student_uuid)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
