"""
Модуль для работы с отзывами (Review).

Содержит класс Review, типизированный словарь ReviewData для создания из dict.s
"""

from datetime import datetime
from typing import TypedDict, Required, Self

from .status import ReviewStatus
from ..common.exceptions import MissingRequiredFieldError, InvalidChoiceError
from ..common.validators import (
    validate_non_empty_string,
    validate_list_string,
    validate_string_length,
)


class ReviewData(TypedDict, total=False):
    """
    Типизированный словарь для передачи данных при создании Review через from_dict.

    :cvar title: Заголовок отзыва (обязательное поле).
    :cvar content: Текст отзыва (обязательное поле).
    :cvar author: Имя автора (по умолчанию "Эксперт").
    :cvar date: Дата и время создания (None → текущее время).
    :cvar status: Статус отзыва (ReviewStatus или строка, по умолчанию PUBLISHED).
    :cvar pros: Список преимуществ.
    :cvar cons: Список недостатков.
    """

    title: Required[str]
    content: Required[str]
    author: str
    date: datetime | None
    status: ReviewStatus | str
    pros: list[str] | None
    cons: list[str] | None


class Review:
    """
    Модель отзыва на устройство.

    :cvar MAX_PRO_CON_LENGTH: Максимальная длина одного элемента в списках pros/cons.
    """

    _MAX_PRO_CON_LENGTH = 200

    def __init__(
        self,
        title: str,
        content: str,
        author: str = "Эксперт",
        date: datetime | None = None,
        status: ReviewStatus | str = ReviewStatus.PUBLISHED,
        pros: list[str] | None = None,
        cons: list[str] | None = None,
    ):
        """
        Инициализирует отзыв.

        :param title: Заголовок (не может быть пустым).
        :param content: Содержание (не может быть пустым).
        :param author: Автор (по умолчанию "Эксперт").
        :param date: Дата создания. Если None, устанавливается текущее время.
        :param status: Статус (enum или строка).
        :param pros: Список преимуществ.
        :param cons: Список недостатков.

        :raises EmptyFieldError: Если title, content или author пустые.
        :raises InvalidChoiceError: Если status не соответствует допустимым.
        :raises TypeError: Если pros/cons не являются списком строк.
        :raises EmptyFieldError: Если в pros/cons есть пустая строка.
        """
        # Присвоение через свойства
        self.title = title
        self.content = content
        self.author = author
        self.status = status
        self.date = date
        self.pros = pros
        self.cons = cons

    @property
    def title(self) -> str:
        """Возвращает заголовок отзыва."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """
        Устанавливает заголовок отзыва.

        :param value: Новый заголовок.
        :raises EmptyFieldError: Если значение - пустая строка или состоит из пробелов.
        :raises TypeError: Если значение не является строкой.
        """
        self._title = validate_non_empty_string(value, "title", "Review")

    @property
    def content(self) -> str:
        """Возвращает содержание отзыва."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        """
        Устанавливает содержание отзыва.

        :param value: Новое содержание.
        :raises EmptyFieldError: Если значение - пустая строка или состоит из пробелов.
        :raises TypeError: Если значение не является строкой.
        """
        self._content = validate_non_empty_string(value, "content", "Review")

    @property
    def author(self) -> str:
        """Возвращает автора отзыва."""
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        """
        Устанавливает автора отзыва.

        :param value: Имя автора.
        :raises EmptyFieldError: Если значение - пустая строка или состоит из пробелов.
        :raises TypeError: Если значение не является строкой.
        """
        self._author = validate_non_empty_string(value, "author", "Review")

    @property
    def status(self) -> ReviewStatus:
        """Возвращает статус отзыва (всегда объект ReviewStatus)."""
        return self._status

    @status.setter
    def status(self, value: ReviewStatus | str) -> None:
        """
        Устанавливает статус отзыва.

        :param value: Статус (enum или строка).
        :raises InvalidChoiceError: Если строка не соответствует ни одному допустимому статусу.
        """
        try:
            self._status = ReviewStatus(value)
        except ValueError as exc:
            review_status = ReviewStatus.to_list()
            raise InvalidChoiceError(value, "status", review_status, "Review") from exc

    @property
    def date(self) -> datetime:
        """Возвращает дату и время создания обзора."""
        return self._date

    @date.setter
    def date(self, new_date: datetime | None) -> None:
        """
        Устанавливает дату создания отзыва.

        :param new_date: Объект datetime или None. При None устанавливается текущее время.
        :raises TypeError: Если передан не datetime и не None.
        """
        if new_date is None:
            self._date = datetime.now()
        elif isinstance(new_date, datetime):
            self._date = new_date
        else:
            raise TypeError(
                f"Ожидается datetime или None, получен {type(new_date).__name__}."
            )

    @property
    def pros(self) -> list[str]:
        """Возвращает копию списка преимуществ (изменение копии не влияет на объект)."""
        return self._pros.copy()

    @pros.setter
    def pros(self, new_pros: list[str] | None) -> None:
        """
        Устанавливает список преимуществ.

        :param new_pros: Список строк или None. При None создаётся пустой список.
        :raises TypeError: Если передан не список.
        :raises EmptyFieldError: Если значение - пустая строка или состоит из пробелов.
        """
        if new_pros is None:
            self._pros = []
        else:
            self._pros = validate_list_string(new_pros, "pros", "Review", self._MAX_PRO_CON_LENGTH)

    @property
    def cons(self) -> list[str]:
        """Возвращает копию списка недостатков (изменение копии не влияет на объект)."""
        return self._cons.copy()

    @cons.setter
    def cons(self, new_cons: list[str] | None) -> None:
        """
        Устанавливает список недостатков.

        :param new_cons: Список строк или None. При None создаётся пустой список.
        :raises TypeError: Если передан не список.
        :raises EmptyFieldError: Если значение - пустая строка или состоит из пробелов.
        """
        if new_cons is None:
            self._cons = []
        else:
            self._cons = validate_list_string(new_cons, "cons", "Review", self._MAX_PRO_CON_LENGTH)

    def add_pro(self, pro_text: str) -> None:
        """
        Добавляет новый пункт в список преимуществ.

        :param pro_text: Текст преимущества.
        :raises EmptyFieldError: Если pro_text - пустая строка.
        :raises TextTooLongError: Если длина превышает _MAX_PRO_CON_LENGTH.
        """
        normalized = validate_string_length(pro_text, "pro", self._MAX_PRO_CON_LENGTH, "Review")
        self._pros.append(normalized)

    def add_con(self, con_text: str) -> None:
        """
        Добавляет новый пункт в список недостатков.

        :param con_text: Текст недостатка.
        :raises EmptyFieldError: Если con_text - пустая строка.
        :raises TextTooLongError: Если длина превышает _MAX_PRO_CON_LENGTH.
        """
        normalized = validate_string_length(con_text, "con", self._MAX_PRO_CON_LENGTH, "Review")
        self._cons.append(normalized)

    def remove_pro(self, index: int) -> None:
        """
        Удаляет пункт из списка преимуществ по индексу.

        :param index: Индекс удаляемого элемента (0-based).
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        try:
            del self._pros[index]
        except IndexError as exc:
            raise IndexError(
                f"Индекс {index}  выходит за пределы списка преимуществ "
                f"(размер {len(self._pros)})."
            ) from exc

    def remove_con(self, index: int) -> None:
        """
        Удаляет пункт из списка недостатков по индексу.

        :param index: Индекс удаляемого элемента (0-based).
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        try:
            del self._cons[index]
        except IndexError as exc:
            raise IndexError(
                f"Индекс {index}  выходит за пределы списка недостатков "
                f"(размер {len(self._cons)})."
            ) from exc

    @classmethod
    def from_dict(cls, data: ReviewData) -> Self:
        """
        Создаёт экземпляр Review из словаря.

        :param data: Словарь с данными (должен содержать ключи "title" и "content").
        :return: Новый объект Review.
        :raises MissingRequiredFieldError: Если отсутствует "title" или "content".
        """
        base_keys = ("title", "content")

        for key in base_keys:
            if key not in data:
                raise MissingRequiredFieldError(key, "Review")

        return cls(
            title=data["title"],
            content=data["content"],
            author=data.get("author", "Эксперт"),
            status=data.get("status", ReviewStatus.PUBLISHED),
            date=data.get("date", None),
            pros=data.get("pros", None),
            cons=data.get("cons", None),
        )

    def __str__(self) -> str:
        """Возвращает удобочитаемое строковое представление отзыва."""
        return (
            f"Info Review:\n\ttitle={self.title}\n\tcontent={self.content}"
            f"\n\tauthor={self.author}"
            f"\n\tdate={self.date}\n\tstatus={self.status}"
            f"\n\tpros={', '.join(self.pros)}\n\tcons={', '.join(self.cons)}"
        )

    def __repr__(self) -> str:
        """Возвращает строковое представление, по которому можно воссоздать объект."""
        return (
            f"Review(title={self.title!r}, content={self.content!r}, "
            f"author={self.author!r}, date={self.date!r}, "
            f"status=ReviewStatus.{self.status.name}, "
            f"pros={self.pros}, cons={self.cons})"
        )
