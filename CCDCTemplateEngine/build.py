from CCDCServer.request import Request
from CCDCTemplateEngine.main import CCDC_TemplateEngine


class CCDC_TemplateBuild:
    def __init__(self, context: dict):
        self.context = context

    def build_template(self, request: Request, template_name: str) -> str:
        """
        Функция для построения шаблона на основе запроса, контекста и имени шаблона.

        :param self:
        :param request: Объект запроса
        :param template_name: Имя шаблона
        :return: Готовый шаблон как строка
        """

        # Проверка наличия базового каталога и имени каталога с шаблонами в настройках запроса
        assert request.settings.get('BASE_DIR')
        assert request.settings.get('TEMPLATE_DIR_NAME')
        # Создание экземпляра класса Engine с указанием базового каталога и имени каталога с шаблонами
        engine = CCDC_TemplateEngine(
            request.settings.get('BASE_DIR'),
            request.settings.get('TEMPLATE_DIR_NAME')
        )

        # Вызов метода build у Engine для построения шаблона и возврата результата
        return engine.build(self.context, template_name)
