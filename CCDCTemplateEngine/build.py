from CCDCServer.request import Request
from CCDCTemplateEngine.main import CCDCTemplateEngine


class CCDCTemplateBuild:
    @staticmethod
    def build_template(request: Request, template_name: str, context: dict) -> str:
        """
        Функция для построения шаблона на основе запроса, контекста и имени шаблона.

        :param request: Объект запроса
        :param template_name: Имя шаблона
        :param context: Контекст
        :return: Готовый шаблон как строка
        """

        # Проверка наличия базового каталога и имени каталога с шаблонами в настройках запроса
        assert request.settings.get('BASE_DIR')
        assert request.settings.get('TEMPLATE_DIR_NAME')
        # Создание экземпляра класса Engine с указанием базового каталога и имени каталога с шаблонами
        engine = CCDCTemplateEngine(
            request.settings.get('BASE_DIR'),
            request.settings.get('TEMPLATE_DIR_NAME'),
            context
        )

        # Вызов метода build у Engine для построения шаблона и возврата результата
        return engine.render_template(template_name)
