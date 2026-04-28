"""
Модуль для работы с отзывами (Review).

Содержит класс Review, типизированный словарь ReviewData для создания из dict.s
"""

from datetime import datetime
from typing import TypedDict, Required, Self
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field, replace

from src.review.status import ReviewStatus
from src.common.exceptions import MissingRequiredFieldError, InvalidChoiceError
from src.common.validators import (
    validate_non_empty_string,
    validate_string_length,
)
from src.core.config import settings


class Review:
    """Модель отзыва на устройство."""

    def __init__(
        self,
        title: str,
        content: str,
        author: str = "Эксперт",
        date: datetime | None = None,
        status: ReviewStatus | str = ReviewStatus.PUBLISHED,
        pros: Iterable[str] | None = None,
        cons: Iterable[str] | None = None,
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
        return self._pros.to_list()

    @pros.setter
    def pros(self, new_pros: Iterable[str] | None) -> None:
        """
        Устанавливает список преимуществ.

        :param new_pros: Список строк или None. При None создаётся пустой список.
        :raises TypeError: Если передан не список.
        :raises EmptyFieldError: Если значение - пустая строка или состоит из пробелов.
        """
        self._pros = ProsConsList.from_collections(new_pros, field_name="pros")

    @property
    def cons(self) -> list[str]:
        """Возвращает копию списка недостатков (изменение копии не влияет на объект)."""
        return self._cons.to_list()

    @cons.setter
    def cons(self, new_cons: Iterable[str] | None) -> None:
        """
        Устанавливает список недостатков.

        :param new_cons: Список строк или None. При None создаётся пустой список.
        :raises TypeError: Если передан не список.
        :raises EmptyFieldError: Если значение - пустая строка или состоит из пробелов.
        """
        self._cons = ProsConsList.from_collections(new_cons, field_name="cons")

    def add_pro(self, pro_text: str) -> None:
        """
        Добавляет новый пункт в список преимуществ.

        :param pro_text: Текст преимущества.
        :raises EmptyFieldError: Если pro_text - пустая строка.
        :raises TextTooLongError: Если длина превышает _MAX_PRO_CON_LENGTH.
        """
        self._pros = self._pros.add(pro_text)

    def add_con(self, con_text: str) -> None:
        """
        Добавляет новый пункт в список недостатков.

        :param con_text: Текст недостатка.
        :raises EmptyFieldError: Если con_text - пустая строка.
        :raises TextTooLongError: Если длина превышает _MAX_PRO_CON_LENGTH.
        """
        self._cons = self._cons.add(con_text)

    def remove_pro(self, index: int) -> None:
        """
        Удаляет пункт из списка преимуществ по индексу.

        :param index: Индекс удаляемого элемента (0-based).
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        self._pros = self._pros.remove(index)

    def remove_con(self, index: int) -> None:
        """
        Удаляет пункт из списка недостатков по индексу.

        :param index: Индекс удаляемого элемента (0-based).
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        self._cons = self._cons.remove(index)

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
        pros = ", ".join(self.pros) if self.pros else "—"
        cons = ", ".join(self.cons) if self.cons else "—"
        return (
            f"Review:\n"
            f"\ttitle={self.title}\n"
            f"\tcontent={self.content}\n"
            f"\tauthor={self.author}\n"
            f"\tdate={self.date}\n"
            f"\tstatus={self.status.value}\n"
            f"\tpros={pros}\n"
            f"\tcons={cons}"
        )

    def __repr__(self) -> str:
        """Возвращает строковое представление, по которому можно воссоздать объект."""
        return (
            f"Review(title={self.title!r}, content={self.content!r}, "
            f"author={self.author!r}, date={self.date!r}, "
            f"status=ReviewStatus.{self.status.name}, "
            f"pros={self.pros}, cons={self.cons})"
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
    pros: Iterable[str] | None
    cons: Iterable[str] | None


@dataclass(frozen=True, slots=True)
class ProsConsList:
    field_name: str
    entity: str = "Review"
    max_item_length: int = settings.MAX_PRO_CON_LENGTH
    _items: tuple[str, ...] = field(default_factory=tuple, repr=False)

    def __post_init__(self) -> None:
        validate_items = tuple(
            validate_string_length(
                item, self.field_name, self.max_item_length, self.entity
            )
            for item in self._items
        )
        object.__setattr__(self, "_items", validate_items)

    @classmethod
    def from_collections(
        cls,
        collections: Iterable[str] | None,
        *,
        field_name: str,
        entity: str = "Review",
        max_item_length: int = settings.MAX_PRO_CON_LENGTH,
    ) -> Self:
        if isinstance(collections, str):
            raise TypeError(
                f"'{entity}.{field_name}' должен быть коллекцией строк, а не {type(collections).__name__}."
            )

        if collections is None:
            prepared_collections: tuple[str, ...] = ()
        else:
            prepared_collections = tuple(collections)

        return cls(
            field_name=field_name,
            entity=entity,
            max_item_length=max_item_length,
            _items=prepared_collections,
        )

    def add(self, item: str) -> Self:
        normalized = validate_string_length(
            item, self.field_name, self.max_item_length, self.entity
        )
        return replace(self, _items=self._items + (normalized,))

    def remove(self, index: int) -> Self:
        items_list: list[str] = list(self._items)
        try:
            del items_list[index]
        except IndexError as ex:
            raise IndexError(
                f"Индекс {index} выходит за пределы списка "
                f"'{self.entity}.{self.field_name}' (размер {len(self._items)})."
            ) from ex
        else:
            # Не знаю какой способ выбрать
            # return object.__setattr__(self, "_items", tuple(items_list))
            # return self.__class__(_items=tuple(items_list), field_name=self.field_name)
            # return self.__class__.__setattr__(self, "_items", tuple(items_list))
            return replace(self, _items=tuple(items_list))

    def to_list(self) -> list[str]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[str]:
        return iter(self._items)

    def __getitem__(self, index: int) -> Self:
        return self._items[index]
