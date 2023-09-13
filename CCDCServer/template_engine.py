import os
import re
from CCDCServer.request import Request


VARIABLE_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z\'"\[\].]+) }}')

FOR_BLOCK_PATTERN = re.compile(r'{% for (?P<variable>[a-zA-Z]+) in '
                               r'(?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)'
                               r'(?={% endblock %}){% endblock %}')

IF_BLOCK_PATTERN = re.compile(r'{% if (?P<condition>[^%]+) %}(?P<content>[\S\s]+)'
                              r'(?:{% else %}(?P<else_content>[\S\s]+))?{% endif %}')


class Engine:
    def __init__(self, base_dir: str, template_dir: str):
        """
        Конструктор класса Engine.

        :param base_dir: Базовый каталог веб-приложения
        :param template_dir: Имя каталога с шаблонами
        """

        self.template_dir = os.path.join(base_dir, template_dir)

    def _get_template_as_string(self, template_name: str):
        """
        Приватный метод для получения содержимого шаблона как строки.

        :param template_name: Название шаблона
        :return: Содержимое файла шаблона
        """

        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.isfile(template_path):
            raise Exception(f'{template_path} не является файлом')
        with open(template_path) as f:
            return f.read()

    @staticmethod
    def _build_block(context: dict, raw_template_block: str) -> str:
        """
        Статический метод для замены переменных в блоке шаблона на их значения из контекста.

        :param context: Контекст
        :param raw_template_block: Блок шаблона с переменными
        :return: Блок шаблона с замененными переменными из контекста
        """

        used_vars = VARIABLE_PATTERN.findall(raw_template_block)
        if used_vars is None:
            return raw_template_block

        for var in used_vars:
            var_in_template = '{{ %s }}' % var
            raw_template_block = re.sub(var_in_template, str(context.get(var, '')), raw_template_block)

        return raw_template_block

    def _build_for_block(self, context: dict, raw_template: str) -> str:
        """
        Метод для обработки блоков цикла "for" в шаблоне.

        :param context: Контекст
        :param raw_template: Исходный текст шаблона
        :return: Шаблон с обработанными блоками цикла "for"
        """

        for_block = FOR_BLOCK_PATTERN.search(raw_template)
        if for_block is None:
            return raw_template

        build_for_block = ''
        for item in context.get(for_block.group('seq'), []):
            if isinstance(item, dict):
                # Если элемент списка - это словарь, заменяем обращения к ключам с помощью []
                updated_context = {**context, **item}  # Обновляем контекст, добавляя элемент словаря
                build_for_block += self._build_block(updated_context, for_block.group('content'))
            else:
                # Если элемент списка не является словарем, оставляем его без изменений
                build_for_block += self._build_block(
                    {**context, for_block.group('variable'): item},
                    for_block.group('content')
                )
        return FOR_BLOCK_PATTERN.sub(build_for_block, raw_template)

    @staticmethod
    def _build_if_block(context: dict, raw_template: str) -> str:
        """
        Метод для обработки блоков условия "if" и "else" в шаблоне.

        :param context: Контекст
        :param raw_template: Исходный текст шаблона
        :return: Шаблон с обработанными блоками условия "if" и "else"
        """

        def evaluate_condition(cond):
            try:
                return eval(cond, {}, context)
            except Exception as e:
                raise Exception(f"Error evaluating condition: {str(e)}")

        if_block = IF_BLOCK_PATTERN.search(raw_template)
        while if_block is not None:
            condition = if_block.group('condition')
            content = if_block.group('content')
            else_content = if_block.group('else_content')

            if evaluate_condition(condition):
                replacement = content
            elif else_content:
                replacement = else_content
            else:
                replacement = ''

            raw_template = IF_BLOCK_PATTERN.sub(replacement, raw_template, count=1)
            if_block = IF_BLOCK_PATTERN.search(raw_template)

        return raw_template

    def build(self, context: dict, template_name: str) -> str:
        """
        Метод для построения конечного шаблона на основе контекста и имени шаблона.

        :param context: Контекст
        :param template_name: Имя шаблона
        :return: Готовый шаблон как строка
        """

        raw_template = self._get_template_as_string(template_name)
        raw_template = self._build_for_block(context, raw_template)
        raw_template = self._build_if_block(context, raw_template)

        return self._build_block(context, raw_template)


def build_template(request: Request, context: dict, template_name: str) -> str:
    """
    Функция для построения шаблона на основе запроса, контекста и имени шаблона.

    :param request: Объект запроса
    :param context: Контекст
    :param template_name: Имя шаблона
    :return: Готовый шаблон как строка
    """

    # Проверка наличия базового каталога и имени каталога с шаблонами в настройках запроса
    assert request.settings.get('BASE_DIR')
    assert request.settings.get('TEMPLATE_DIR_NAME')

    # Создание экземпляра класса Engine с указанием базового каталога и имени каталога с шаблонами
    engine = Engine(
        request.settings.get('BASE_DIR'),
        request.settings.get('TEMPLATE_DIR_NAME')
    )

    # Вызов метода build у Engine для построения шаблона и возврата результата
    return engine.build(context, template_name)
