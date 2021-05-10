import quopri
import copy
import sqlite3
from patterns.behavioral_patterns import ConsoleWriter
from patterns.architectural_system_pattern_unit_of_work import DomainObject


# абстрактный пользователь
class User:
    uuid = 0

    def __init__(self, uuid, name):
        self.name = name
        self.uuid = uuid

    def __str__(self):
        return f'{self.uuid}: {self.name}'

    def __repr__(self):
        return self.__str__()


# преподаватель
class Teacher(User):
    pass


# студент
class Student(User, DomainObject):
    def __init__(self, uuid, name):
        super().__init__(uuid, name)
        self._courses = []

    def add_student(self, course):
        self._courses.append(course)

    def get_courses(self):
        return self._courses


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](uuid=0, name=name)


# порождающий паттерн Прототип - Курс
class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    _students = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def get_students(self):
        # TODO тут написать код получения списка студентов курса
        pass


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Категория
class Category(DomainObject):
    uuid = 0

    def __init__(self, uuid, name):
        self.uuid = uuid
        self.name = name
        self.courses = []

    def course_count(self):
        # TODO реализовать счетчик курсов запросом из БД
        pass


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name):
        return Category(name)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Database(metaclass=Singleton):
    connection = None
    cursor_obj = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db.sqlite3")
            self.cursor_obj = self.connection.cursor()
            self.db_init()
        return self.cursor_obj

    def db_init(self):
        self.cursor_obj.execute(
            '''CREATE TABLE IF NOT EXISTS STUDENTS
            (UUID INTEGER PRIMARY KEY AUTOINCREMENT, [name] text)''')
        self.cursor_obj.execute(
            '''CREATE TABLE IF NOT EXISTS CATEGORIES
            (UUID INTEGER PRIMARY KEY AUTOINCREMENT, [name] text)''')
        self.cursor_obj.execute(
            '''CREATE TABLE IF NOT EXISTS COURSES
            (UUID INTEGER PRIMARY KEY AUTOINCREMENT, 
            [name] text, 
            [category] text, 
            FOREIGN KEY (category) references categories(name))''')
        self.connection.commit()


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


# Заметка, можно применить стратегию если добавить стратегию логирования
class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
