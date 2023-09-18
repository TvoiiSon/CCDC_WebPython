import os
import re
import ast
from pprint import pprint


class CCDCTemplateEngine:
    def __init__(self, base_dir: str, template_dir: str, context: dict):
        """
        Конструктор класса Engine.

        :param base_dir: Базовый каталог веб-приложения
        :param template_dir: Имя каталога с шаблонами
        :param context: Контекст
        """

        self.template_dir = os.path.join(base_dir, template_dir)
        self.context = context

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

    def render_template(self, template_name: str):
        template_content = self._get_template_as_string(template_name)
        rendered_template = self._render_variables(template_content)
        rendered_template = self._render_if_else(rendered_template)
        rendered_template = self._render_for(rendered_template)
        return rendered_template

    def _render_variables(self, template_content: str):
        def replace_variable(match):
            variable_expression = match.group(0)
            variable_name = match.group(1)

            # Разбиваем переменную на части, разделенные точкой
            variable_parts = variable_name.split('.')
            current_value = self.context

            # Перебираем части переменной и обращаемся к ним в контексте
            for part in variable_parts:
                if part in current_value:
                    current_value = current_value[part]
                else:
                    # Если какая-то часть не найдена в контексте, оставляем переменную без замены
                    return variable_expression

            # Если все части найдены, возвращаем значение переменной
            return str(current_value)

        pattern = r'{{\s*([\w_.]+)\s*}}'  # Обновленное регулярное выражение для поддержки точечной нотации
        rendered_template = re.sub(pattern, replace_variable, template_content)
        return rendered_template

    def _render_if_else(self, template_content: str):
        pattern = r'{% if (.*?) %}(.*?){% else %}(.*?){% endif %}'

        def evaluate_expression(expression):
            try:
                parsed_expr = ast.parse(expression, mode='eval')
                evaluated_result = eval(compile(parsed_expr, filename='<string>', mode='eval'), self.context)
                return evaluated_result
            except Exception as e:
                print(e)
                return None

        def replace_if_else(match):
            if_expression = match.group(1)
            if_body = match.group(2)
            else_body = match.group(3)

            if_result = evaluate_expression(if_expression)

            if if_result:
                return if_body
            else:
                return else_body

        rendered_template = re.sub(pattern, replace_if_else, template_content, flags=re.DOTALL)
        return rendered_template

    def _render_for(self, template_content: str):
        pattern = r'{% for (\w+) in ([\w.]+) %}(.*?){% endfor %}'

        def evaluate_expression(expression):
            try:
                parsed_expr = ast.parse(expression, mode='eval')
                evaluated_result = eval(compile(parsed_expr, filename='<string>', mode='eval'), self.context)
                return evaluated_result
            except Exception as e:
                print(e)
                return None

        def replace_for(match):
            variable_name = match.group(1)
            iterable_expression = match.group(2)
            loop_body = match.group(3)
            print(variable_name, iterable_expression, loop_body)

            iterable = evaluate_expression(iterable_expression)

            if iterable is not None and isinstance(iterable, (list, tuple, set, dict)):
                result = ""
                for i, item in enumerate(iterable, start=1):
                    # Генерируем уникальное имя переменной
                    unique_variable_name = f"{variable_name}{i}"

                    # Добавляем элемент item в контекст под уникальным именем
                    self.context[unique_variable_name] = item

                    # Рендерим тело цикла
                    rendered_loop_body = self._render_variables(loop_body)

                    result += rendered_loop_body

                return result
            else:
                return ""

        rendered_template = re.sub(pattern, replace_for, template_content, flags=re.DOTALL)
        return rendered_template

