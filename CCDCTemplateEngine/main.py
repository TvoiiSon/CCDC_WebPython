import os
import re

VARIABLE_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z\'"\[\].]+) }}')

FOR_BLOCK_PATTERN = re.compile(r'{% for (?P<variable>[a-zA-Z]+) in '
                               r'(?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)'
                               r'(?={% endblock %}){% endblock %}')

IF_BLOCK_PATTERN = re.compile(r'{% if (?P<condition>[^%]+) %}(?P<content>[\S\s]+)'
                              r'(?:{% else %}(?P<else_content>[\S\s]+))?{% endif %}')


class CCDC_TemplateEngine:
    def __init__(self, base_dir: str, template_dir: str, context: dict):
        """
        Конструктор класса Engine.

        :param base_dir: Базовый каталог веб-приложения
        :param template_dir: Имя каталога с шаблонами
        :param context: Контекст
        """

        self.template_dir = os.path.join(base_dir, template_dir)
        self.context = context

    def _add_value_to_global_variable(self, key, value):
        if key in self.context:
            # Если ключ уже существует в словаре, добавляем значение в множество
            self.context[key].add(value)
        else:
            # Если ключа нет, создаем новую запись в словаре с ключом и множеством значений
            self.context[key] = {value}

    def _get_value_to_global_context(self):
        return self.context

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

    def _build_block(self, raw_template_block: str) -> str:
        """
        Статический метод для замены переменных в блоке шаблона на их значения из контекста.

        :param raw_template_block: Блок шаблона с переменными
        :return: Блок шаблона с замененными переменными из контекста
        """

        used_vars = VARIABLE_PATTERN.findall(raw_template_block)
        if used_vars is None:
            return raw_template_block

        for var in used_vars:
            var_in_template = '{{ %s }}' % var
            raw_template_block = re.sub(var_in_template, str(self.context.get(var, '')), raw_template_block)
            print(var, str(self.context.get(var, '')))
            self._add_value_to_global_variable(var, str(self.context.get(var, '')))

        test = self._get_value_to_global_context()
        print(test)
        return raw_template_block

    def _build_for_block(self, raw_template: str) -> str:
        """
        Метод для обработки блоков цикла "for" в шаблоне.

        :param raw_template: Исходный текст шаблона
        :return: Шаблон с обработанными блоками цикла "for"
        """

        for_block = FOR_BLOCK_PATTERN.search(raw_template)
        if for_block is None:
            return raw_template

        build_for_block = ''
        for item in self.context.get(for_block.group('seq'), []):
            if isinstance(item, dict):
                # Если элемент списка - это словарь, заменяем обращения к ключам с помощью []
                updated_context = {**self.context, **item}  # Обновляем контекст, добавляя элемент словаря
                build_for_block += self._build_block(updated_context)
            else:
                # Если элемент списка не является словарем, оставляем его без изменений
                build_for_block += self._build_block(
                    for_block.group('content')
                )
        return FOR_BLOCK_PATTERN.sub(build_for_block, raw_template)

    def _build_if_block(self, raw_template: str) -> str:
        """
        Метод для обработки блоков условия "if" и "else" в шаблоне.

        :param raw_template: Исходный текст шаблона
        :return: Шаблон с обработанными блоками условия "if" и "else"
        """

        def evaluate_condition(cond):
            try:
                return eval(cond, {}, self.context)
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

    def build(self, template_name: str) -> str:
        """
        Метод для построения конечного шаблона на основе контекста и имени шаблона.

        :param template_name: Имя шаблона
        :return: Готовый шаблон как строка
        """

        raw_template = self._get_template_as_string(template_name)
        raw_template = self._build_for_block(raw_template=raw_template)
        raw_template = self._build_if_block(raw_template=raw_template)

        return self._build_block(raw_template)