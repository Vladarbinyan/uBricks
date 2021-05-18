import sqlite3
from patterns.creational_patterns import Student, Category, Course
from patterns.creational_patterns import Database


class StudentMapper:

    def __init__(self, db):
        self.connection = db.connection
        self.cursor = db
        self.table_name = 'students'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            uuid, name = item
            student = Student(uuid, name)
            result.append(student)
        return result

    def find_by_id(self, uuid):
        statement = f"SELECT uuid, name FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (uuid,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={uuid} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE uuid=?"
        self.cursor.execute(statement, (obj.name, obj.uuid))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (obj.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:

    def __init__(self, db):
        self.connection = db.connection
        self.cursor = db
        self.table_name = 'categories'

    def all(self):
        statement = """
                    SELECT t1.UUID, t1.name, count(t2.category_id) as course_count from categories as t1
                    left join courses as t2 on t2.category_id = t1.UUID group by t1.UUID
                    """
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            uuid, name, course_count = item
            category = Category(uuid, name)
            category.course_count = course_count
            result.append(category)
        return result

    def find_by_id(self, uuid):
        statement = f"SELECT uuid, name FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (uuid,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={uuid} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE uuid=?"
        self.cursor.execute(statement, (obj.name, obj.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (obj.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CourseMapper:

    def __init__(self, db):
        self.connection = db.connection
        self.cursor = db
        self.table_name = 'courses'

    def all(self):
        statement = """
        SELECT t1.uuid, t1.name, t1.category_id, t2.name from courses as t1 
        left join categories as t2 on t1.category_id = t2.uuid
        """
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            uuid, name, category_id, category_name = item
            course = Course(name, Category(category_id, category_name))
            result.append(course)
        return result

    def all_by_category(self, category):
        statement = f'SELECT * from {self.table_name} WHERE category_id=?'
        self.cursor.execute(statement, (category.uuid,))
        result = []
        for item in self.cursor.fetchall():
            uuid, name, category_id = item
            course = Course(name, category)
            result.append(course)
        return result

    def find_by_id(self, uuid):
        statement = f"SELECT uuid, name, category_id FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (uuid,))
        result = self.cursor.fetchone()
        if result:
            uuid, name, category_id = result
            category = CategoryMapper.find_by_id(category_id)
            return Course(name, category)
        else:
            raise RecordNotFoundException(f'record with id={uuid} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name, category_id) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=?, category=? WHERE uuid=?"
        self.cursor.execute(statement, (obj.name, obj.category.uuid, obj.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (obj.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class SubscribersMapper:

    def __init__(self, db):
        self.connection = db.connection
        self.cursor = db
        self.table_name = 'subscribers'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            student_id, course_id = item
            student = Student(uuid, name)
            result.append(student)
        return result

    def all_by_category(self, category):
        statement = f'SELECT * from {self.table_name} WHERE category_id=?'
        self.cursor.execute(statement, (category.uuid,))
        result = []
        for item in self.cursor.fetchall():
            uuid, name, category_id = item
            course = Course(name, category)
            result.append(course)
        return result

    def find_by_id(self, uuid):
        statement = f"SELECT uuid, name, category_id FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (uuid,))
        result = self.cursor.fetchone()
        if result:
            uuid, name, category_id = result
            category = CategoryMapper.find_by_id(category_id)
            return Course(name, category)
        else:
            raise RecordNotFoundException(f'record with id={uuid} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name, category_id) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=?, category=? WHERE uuid=?"
        self.cursor.execute(statement, (obj.name, obj.category.uuid, obj.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE uuid=?"
        self.cursor.execute(statement, (obj.uuid,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


db = Database().connect()


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
        'subscribers': SubscribersMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(db)
        elif isinstance(obj, Category):
            return CategoryMapper(db)
        elif isinstance(obj, Course):
            return CourseMapper(db)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](db)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
