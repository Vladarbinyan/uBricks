"""
Используем шаблонизатор jinja2
"""
from jinja2 import Template, Environment, FileSystemLoader


def render(template_name, folder='templates', **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param folder: путь к папке с шаблонами (от корня приложения)
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)
