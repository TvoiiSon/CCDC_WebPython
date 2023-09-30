import jinja2


class LoadTemplate:
    def __init__(self, template_folder: str, template_name: str, **kwargs):
        """
        Конструктор класса LoadTemplate.

        :param template_folder: Строка, представляющая путь к папке с шаблонами.
        :param template_name: Строка, представляющая имя файла шаблона.
        :param kwargs: Дополнительные аргументы, включая контекст для шаблона.
        """

        if not template_folder:
            raise ValueError("Не указана папка с шаблонами")
        if not template_name:
            raise ValueError("Не указано имя шаблона")

        self.template_folder = template_folder
        self.template_name = template_name
        self.context = kwargs.get('context')
        if self.context is not None and not isinstance(self.context, list):
            raise ValueError("Контекст должен быть списком")

    def load_template(self):
        """
        Загружает и рендерит Jinja2 шаблон.

        :return: Строка, содержащая результат рендеринга шаблона.
        """
        template_loader = jinja2.FileSystemLoader(searchpath=self.template_folder)
        jinja_env = jinja2.Environment(loader=template_loader)
        template = jinja_env.get_template(self.template_name)
        if self.context is not None:
            html_content = template.render(self.context)
        else:
            html_content = template.render()

        return html_content
