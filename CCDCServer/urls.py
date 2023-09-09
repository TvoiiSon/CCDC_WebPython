from dataclasses import dataclass
from CCDCServer.view import View
from typing import Type


@dataclass
class Url:
    """
    Класс Url описывает структуру данных для хранения информации о маршруте (URL) и связанном с ним классе View.
    Это может использоваться, например, для маршрутизации веб-приложения, где URL связывается с конкретным
    обработчиком (View). Аннотация Type[View] указывает на ожидаемый тип данных для поля view, который должен
    быть классом, производным от View.
    """

    url: str
    view: Type[View]
