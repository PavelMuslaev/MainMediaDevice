"""
Базовый абстрактный класс для всех устройств.

Определяет общие атрибуты (бренд, модель, категория, год выпуска,
изображение, характеристики, отзыв) и методы, которые должны быть
реализованы в классах-наследниках.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
import copy

from ..review.review import Review
from ..common.exceptions import InvalidChoiceError
from ..common.validators import validate_non_empty_string, validate_range_year
from .categories import DeviceCategory


class Device(ABC):
    """
    Абстрактный суперкласс для всех устройств.

    :cvar _DEFAULT_START_YEAR: Нижняя граница допустимого года выпуска.
    """

    _DEFAULT_START_YEAR = 1990

    def __init__(
        self,
        brand: str,
        model: str,
        category: DeviceCategory | str,
        year: int | None = None,
        image: str | None = None,
        specs: dict | None = None,
        review: Review | None = None,
    ):
        """
        Инициализирует экземпляр устройства.

        :param brand: Бренд устройства (не может быть пустым).
        :param model: Модель устройства (не может быть пустым).
        :param category: Категория устройства (enum или строка).
        :param year: Год выпуска (None допустим).
        :param image: URL изображения. Если None, устанавливается заглушка "/".
        :param specs: Характеристики (словарь). Если None, создаётся пустой словарь.
        :param review: Объект отзыва или None.

        :raises EmptyFieldError: Если brand, model или image (при передаче) - пустая строка.
        :raises InvalidChoiceError: Если category не входит в допустимые.
        :raises IncorrectRangeYear: Если год вне диапазона [1990, текущий].
        :raises TypeError: При неверном типе specs или review.
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
    def brand(self) -> str:
        """Возвращает бренд устройства."""
        return self._brand

    @brand.setter
    def brand(self, new_brand: str) -> None:
        self._brand = validate_non_empty_string(new_brand, "brand", "Device")

    @property
    def model(self) -> str:
        """Возвращает модель устройства."""
        return self._model

    @model.setter
    def model(self, new_model: str) -> None:
        self._model = validate_non_empty_string(new_model, "model", "Device")

    @property
    def category(self) -> DeviceCategory:
        """Возвращает категорию устройства (всегда объект AllowedCategory)."""
        return self._category

    @category.setter
    def category(self, value: DeviceCategory | str) -> None:
        """
        Устанавливает категорию устройства.

        :param value: Категория в виде enum или строки.
        :raises InvalidChoiceError: Если строка не соответствует допустимым категориям.
        """
        try:
            self._category = DeviceCategory(value)
        except ValueError as exc:
            allowed_categories = DeviceCategory.to_list()
            raise InvalidChoiceError(
                value, "category", allowed_categories, "Device"
            ) from exc

    @property
    def year(self) -> int | None:
        """Возвращает год выпуска устройства (может быть None)."""
        return self._year

    @year.setter
    def year(self, new_year: int | None) -> None:
        """
        Устанавливает год выпуска.

        :param new_year: Год или None. Если None, год остаётся незаданным.
        :raises YearOutOfRangeError: Если год вне допустимого диапазона.
        """
        if new_year is None:
            self._year = None
        else:
            self._year = validate_range_year(
                new_year,
                self._DEFAULT_START_YEAR,
                datetime.today().year,
                "year",
                "Device",
            )

    @property
    def image(self) -> str:
        """Возвращает ссылку на изображение устройства."""
        return self._image

    @image.setter
    def image(self, new_image: str | None) -> None:
        """
        Устанавливает ссылку на изображение.

        :param new_image: URL изображения. Если None, устанавливается заглушка "/".
        :raises EmptyFieldError: Если переданная строка пуста.
        """
        if new_image is None:
            self._image = "/"  # TODO: ПОКА ЗАГЛУШКА, В БУДУЩЕМ ИСПРАВИТЬ
        else:
            self._image = validate_non_empty_string(new_image, "image", "Device")

    @property
    def specs(self) -> dict:
        """
        Возвращает копию характеристик устройства.

        Возвращается глубокая копия, чтобы предотвратить внешние изменения.
        """
        return copy.deepcopy(self._specs)

    @specs.setter
    def specs(self, new_specs: dict | None) -> None:
        """
        Устанавливает характеристики устройства.

        :param new_specs: Словарь характеристик или None. При None создаётся пустой словарь.
        :raises TypeError: Если передан не dict и не None.
        """
        if new_specs is None:
            self._specs = {}
        elif isinstance(new_specs, dict):
            self._specs = copy.deepcopy(new_specs)
        else:
            raise TypeError("new_specs должен быть dict или None.")

    @property
    def review(self) -> Review | None:
        """Возвращает актуальный обзор на устройство (или None)."""
        return self._review

    @review.setter
    def review(self, new_review: Review | None) -> None:
        """
        Устанавливает обзор на устройство.

        :param new_review: Объект Review или None.
        :raises TypeError: Если передан не Review и не None.
        """
        if isinstance(new_review, (Review, type(None))):
            self._review = new_review
        else:
            raise TypeError('"new_review" должен быть None или Review')

    def add_spec(self, key: str, value: Any) -> None:
        """
        Добавляет или обновляет характеристику устройства.

        :param key: Название характеристики (например, "processor").
        :param value: Значение характеристики.
        """
        self._specs[key] = value

    def remove_spec(self, key: str) -> None:
        """
        Удаляет характеристику по ключу.

        :param key: Название характеристики.
        :raises KeyError: Если ключ не найден.
        """
        try:
            del self._specs[key]
        except KeyError as exc:
            raise KeyError(f"{key} не найден.") from exc

    @abstractmethod
    def get_device_type(self) -> str:
        """
        Возвращает строку с типом устройства.

        Должен быть реализован в наследниках.

        :return: Тип устройства (например, "smartphone").
        """
        pass

    @abstractmethod
    def get_short_description(self) -> str:
        """
        Возвращает краткое описание устройства.

        Должен быть реализован в наследниках.

        :return: Краткое описание (одна-две строки).
        """
        pass

    def __str__(self) -> str:
        """Возвращает удобочитаемое строковое представление устройства."""
        return (
            f"Info Device:\nBrand: {self.brand}\nModel: {self.model}\nCategory: "
            f"{self.category}\nYear: {self.year}\nImage: {self.image}"
        )

    def __repr__(self) -> str:
        """Возвращает строковое представление для воссоздания объекта."""
        return (
            f"{self.__class__.__name__}(brand={self.brand!r}, model={self.model!r}, category={self.category!r}, "
            f"year={self.year}, image={self.image!r}, specs={self.specs}, review={self.review})"
        )
