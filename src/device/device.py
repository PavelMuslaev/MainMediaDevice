from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Any
import copy

from ..review.review import Review
from ..common.exceptions import InvalidChoiceError
from ..common.validators import validate_non_empty_string, validate_range_year
from .categories import AllowedCategory


class Device(ABC):
    """Супер класс модель любого устройства приложения."""

    def __init__(
        self,
        brand: str,
        model: str,
        category: AllowedCategory,
        year: int | None = None,
        image: str | None = None,
        specs: dict | None = None,
        review: Review | None = None,
    ):
        """
        Инициализирует экземпляр устройства.
        :param brand:       Брэнд устройства.
        :param model:       Модель устройства.
        :param category:    Категория устройства.
        :param year:        Год выпуска устройства.
        :param image:       Картинка устройства.
                            Если image is None, будет автоматически установлена
                            картинка по умолчанию.
        :param specs:       Характеристики устройства.
                            Если specs is None, будет автоматически создан
                            пустой словарь.
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
    def category(self) -> AllowedCategory:
        """Возвращает категорию устройства."""
        return self._category

    @category.setter
    def category(self, value: AllowedCategory | str) -> None:
        """
        Устанавливает категорию устройства.
        :param value: Категория устройства.
        :raises InvalidAllowedCategoryError: Если категория устройства установлена
                    не из перечисления AllowedCategory.
        :return: None.
        """
        try:
            self._category = AllowedCategory(value)
        except ValueError as exc:
            allowed_categories = AllowedCategory.to_list()
            raise InvalidChoiceError(value, allowed_categories, "Device") from exc

    @property
    def year(self) -> int:
        """Возвращает установленный год выпуска устройства."""
        return self._year

    @year.setter
    def year(self, new_year: int | None) -> None:
        """
        Устанавливает год выпуска устройства между текущим и 1990 годом.
        :param new_year: Год выпуска устройства.
        :raises TypeError: Если год был передан не в виде числа.
        :raises InvalidDeviceYearError: Если был нарушен диапазон возможных дат.
        :return: None.
        """
        if new_year is None:
            self._year = None
        else:
            self._year = validate_range_year(new_year, 1990, date.today().year)

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
        :raises TypeError: Если путь к картинке передан не в виде строки.
        :return: None.
        """
        if new_image is None:
            self._image = "/"  # TODO: ПОКА ЗАГЛУШКА, В БУДУЩЕМ ИСПРАВИТЬ
        else:
            self._image = validate_non_empty_string(new_image, "image", "Device")

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
        :raises TypeError: Если new_specs получен не в виде словаря.
        :return: None.
        """
        if new_specs is None:
            self._specs = {}
        elif isinstance(new_specs, dict):
            self._specs = copy.deepcopy(new_specs)
        else:
            raise TypeError("new_specs должен быть dict или None.")

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
        if isinstance(new_review, (Review, type(None))):
            self._review = new_review
        else:
            raise TypeError('"new_review" должен быть None или Review')

    def add_spec(self, key: str, value: Any) -> None:
        """
        Добавляет и обновляет характеристики в словаре spec.
        Если ключ уже существует, то значение перезаписывается
        :param key: Имя ключа.
        :param value: Значение ключа.
        :return: None.
        """
        self._specs[key] = value

    def remove_spec(self, key: str) -> None:
        """
        Удаляет характеристику по ключу key.
        :param key: Ключ по которому будет произведен поиск.
        :raises KeyError: Если ключ не найден.
        :return: None.
        """
        try:
            del self._specs[key]
        except KeyError as exc:
            raise KeyError(f"{key} не найден.") from exc

    @abstractmethod
    def get_device_type(self) -> str:
        """Возвращает строку с типом устройства."""
        pass

    @abstractmethod
    def get_short_description(self) -> str:
        """Возвращает краткое описание устройства."""
        pass

    def __str__(self) -> str:
        """Возвращает строковый формат объекта."""
        return (
            f"Info Device:\nModel: {self.model}\nCategory: "
            f"{self.category}\nYear: {self.year}\nImage: {self.image}"
        )

    def __repr__(self) -> str:
        """Возвращает строковый отчёт об объекте."""
        return (
            f"{self.__class__.__name__}(brand={self.brand!r}, model={self.model!r}, category={self.category!r}, "
            f"year={self.year}, image={self.image!r}, specs={self.specs}, review={self.review})"
        )
