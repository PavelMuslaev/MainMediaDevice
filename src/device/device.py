from abc import ABC, abstractmethod
from datetime import datetime
from typing import Literal, Any

import copy

from src.review.review import Review


class Device(ABC):
    """Супер класс модель любого устройства приложения."""

    CategoryType = Literal["Смартфоны", "Наушники", "Планшеты", "Умные часы",]
    ALLOWED_CATEGORIES = [
        "Смартфоны", "Наушники", "Планшеты", "Умные часы",
    ]

    def __init__(self, brand: str, model: str, category: CategoryType,
                 year: int=None, image: str=None, specs: dict=None, review: Review = None):
        """
        Инициализирует экземпляр устройства.
        :param brand:       Брэнд устройства.
        :param model:       Модель устройства.
        :param category:    Категория устройства.
        :param year:        Год выпуска устройства.
        :param image:       Картинка устройства.
        :param specs:       Характеристики устройства.
        :param review:      Актуальный обзор на устройство.
        """
        self.brand = brand
        self.model = model

        # Присваиваем через свойства
        self.category = category
        self.year = year
        self.image = image
        self.specs = specs
        self.review = review

    @property
    def category(self) -> CategoryType:
        """Возвращает категорию устройства."""
        return self._category

    @category.setter
    def category(self, value: CategoryType) -> None:
        """
        Устанавливает категорию устройства.
        :param value: Категория устройства.
        :return: None.
        """
        if value.title() in self.ALLOWED_CATEGORIES:
            self._category = value.title()
        else:
            print(f'"value" must be in {self.ALLOWED_CATEGORIES}')

    @property
    def year(self) -> int:
        """Возвращает установленный год выпуска устройства."""
        return self._year

    @year.setter
    def year(self, new_year: int | None) -> None:
        """
        Устанавливает год выпуска устройства между текущим и 1900 годом.
        :param new_year: Год выпуска устройства.
                         Если None, то будет установлен текущий год.
        :return: None.
        """
        if new_year is None:
            self._year = datetime.now().year
        elif not isinstance(new_year, int):
            print('"new_year" must be int or None')
        elif new_year < 1900 or new_year > datetime.now().year:
            print(f'"new_year" must be between 1900 and {datetime.now().year}')
        else:
            self._year = new_year

    @property
    def image(self) -> str | None:
        """Возвращает ссылку на изображение устройства."""
        return self._image

    @image.setter
    def image(self, new_image: str | None) -> None:
        """
        Устанавливает новое изображение устройства.
        :param new_image: Новое изображение устройства.
                            Если None, то будет установлена картинка по умолчанию.
        :return: None.
        """
        if new_image is None:
            self._image = "/" # ПОКА ЗАГЛУШКА, В БУДУЩЕМ ИСПРАВИТЬ
        elif not isinstance(new_image, str):
            print('"new_image" must be str')
        else:
            self._image = new_image

    @property
    def specs(self) -> dict:
        """Возвращает характеристики устройства."""
        return copy.deepcopy(self._specs)

    @specs.setter
    def specs(self, new_specs: dict | None) -> None:
        """
        Устанавливает набор характеристик устройства.
        :param new_specs: Словарь характеристик устройства.
                          Если None, то будет создан пустой словарь.
        :return: None.
        """
        if new_specs is None:
            self._specs = {}
        elif not isinstance(new_specs, dict):
            print('"new_specs" must be None or a dict')
        else:
            self._specs = copy.deepcopy(new_specs)

    @property
    def review(self) -> Review | None:
        """Возвращает актуальный обзор на устройство."""
        return self._review

    @review.setter
    def review(self, new_review: Review | None) -> None:
        """
        Устанавливает обзор устройству.
        :param new_review:  Обзор на устройство.
        :return: None.
        """
        if new_review is not None and not isinstance(new_review, Review):
            print('"new_review" must be None or a Review')
        else:
            self._review = new_review

    def add_spec(self, key: str, value: Any):
        """
        Добавляет или обновляет характеристику в словаре _specs по
        ключу key со значением value.
        :param key:     Ключ словаря.
        :param value:   Значение ключа.
        :return: None.
        """
        self._specs[key] = value

    def remove_spec(self, key: str):
        """
        Удаляет характеристику по ключу key.
        :param key: Ключ по которому будет произведен поиск.
        :return: None.
        """
        if key in self._specs:
            del self._specs[key]
        else:
            print(f'{key=} not found.')

    @abstractmethod
    def get_device_type(self) -> str:
        """Возвращает строку с типом устройства."""
        pass

    @abstractmethod
    def get_short_description(self) -> str:
        """Возвращает краткое описание устройства."""
        pass
