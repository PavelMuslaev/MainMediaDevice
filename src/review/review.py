"""
Модуль для работы с отзывами (Review).
Содержит класс Review и доменные исключения.
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
    title: Required[str]
    content: Required[str]
    author: str
    date: datetime | None
    status: ReviewStatus | str
    pros: list[str] | None
    cons: list[str] | None


class Review:
    """Модель Review для работы с отзывами."""

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
        """Возвращает заголовок обзора."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = validate_non_empty_string(value, "title", "Review")

    @property
    def content(self) -> str:
        """Возвращает содержание обзора."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = validate_non_empty_string(value, "content", "Review")

    @property
    def author(self) -> str:
        """Возвращает автора обзора."""
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        self._author = validate_non_empty_string(value, "author", "Review")

    @property
    def status(self) -> ReviewStatus:
        """Возвращает статус обзора."""
        return self._status

    @status.setter
    def status(self, value: ReviewStatus | str) -> None:
        try:
            self._status = ReviewStatus(value)
        except ValueError as exc:
            review_status = ReviewStatus.to_list()
            raise InvalidChoiceError(value, review_status, "Review") from exc

    @property
    def date(self) -> datetime:
        """Возвращает дату и время создания обзора."""
        return self._date

    @date.setter
    def date(self, new_date: datetime | None) -> None:
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
        """Возвращает копию списка плюсов из обзора."""
        return self._pros.copy()

    @pros.setter
    def pros(self, new_pros: list[str] | None) -> None:
        if new_pros is None:
            self._pros = []
        else:
            self._pros = validate_list_string(new_pros, "Review")

    @property
    def cons(self) -> list[str]:
        """Возвращает копию списка минусов из обзора."""
        return self._cons.copy()

    @cons.setter
    def cons(self, new_cons: list[str] | None) -> None:
        if new_cons is None:
            self._cons = []
        else:
            self._cons = validate_list_string(new_cons, "Review")

    def add_pro(self, pro_text: str, max_length: int) -> None:
        validate_string_length(pro_text, "pro", max_length, "Review")
        self._pros.append(pro_text)

    def add_con(self, con_text: str, max_length: int) -> None:
        validate_string_length(con_text, "con", max_length, "Review")
        self._cons.append(con_text)

    def remove_pro(self, index: int) -> None:
        try:
            del self._pros[index]
        except IndexError as exc:
            raise IndexError(
                f"Индекс {index}  выходит за пределы списка преимуществ "
                f"(размер {len(self._pros)})."
            ) from exc

    def remove_con(self, index: int) -> None:
        try:
            del self._cons[index]
        except IndexError as exc:
            raise IndexError(
                f"Индекс {index}  выходит за пределы списка недостатков "
                f"(размер {len(self._cons)})."
            ) from exc

    @classmethod
    def from_dict(cls, data: ReviewData) -> Self:
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
        """Возвращает строковое представление объекта."""
        return (
            f"Info Review:\n\ttitle={self.title}\n\tcontent={self.content}"
            f"\n\tauthor={self.author}"
            f"\n\tdate={self.date}\n\tstatus={self.status}"
            f"\n\tpros={', '.join(self.pros)}\n\tcons={', '.join(self.cons)}"
        )

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта, по которому его можно воссоздать."""
        return (
            f"Review(title={self.title!r}, content={self.content!r}, "
            f"author={self.author!r}, date={self.date!r}, "
            f"status=ReviewStatus.{self.status.name}, "
            f"pros={self.pros}, cons={self.cons})"
        )
