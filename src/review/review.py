"""
Модуль для работы с отзывами (Review).
Содержит класс Review и доменные исключения.
"""

from datetime import datetime
from typing import Optional, TypedDict, Required, Union

from .review_status import ReviewStatus
from .review_error import (EmptyReviewFieldError, InvalidStatusError,
                           ReviewTextTooLongError, MissingRequiredFieldsError)


class ReviewData(TypedDict, total=False):
    title: Required[str]
    content: Required[str]
    author: str
    date: Optional[datetime]
    status: Union[ReviewStatus, str]
    pros: Optional[list[str]]
    cons: Optional[list[str]]


class Review:
    """Модель Review для работы с отзывами."""

    def __init__(self, title: str, content: str, author: str='Эксперт',
                 date: Optional[datetime] = None,
                 status: ReviewStatus | str = ReviewStatus.PUBLISHED,
                 pros: Optional[list[str]] = None, cons: Optional[list[str]] = None):
        """
        Инициализирует объект отзыва.

        :param title:   Заголовок отзыва. Не может быть пустой строкой.
        :param content: Содержание (текст) отзыва.
        :param author:  Имя автора. По умолчанию 'Эксперт'.
        :param status:  Статус обзора. По умолчанию: "PUBLISHED".
        :param date: Дата и время создания. Если не указана,
                будет установлена текущая дата и время (через сеттер date).
        :param pros: Список преимуществ.
                Если передан список, создаётся его копия. Если None, создаётся пустой список.
        :param cons: Список недостатков.
                Если передан список, создаётся его копия. Если None, создаётся пустой список.
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
        """Возвращает заголовок обзора."""
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """
        Устанавливает заголовок.

        :param value: Новый текст заголовка.
        :raises TypeError: Если value не является строкой.
        :raises EmptyReviewFieldError: Если value пустая строка или состоит только из пробелов.
        :return: None.
        """
        if not isinstance(value, str):
            raise TypeError(f"Заголовок должен быть строкой, получен "
                            f"{type(value).__name__}.")
        if value.strip():
            self.__title = value
        else:
            raise EmptyReviewFieldError("title")

    @property
    def content(self) -> str:
        """Возвращает содержание обзора."""
        return self.__content

    @content.setter
    def content(self, value: str) -> None:
        """
        Устанавливает содержание статьи.

        :param value: Новый текст содержания.
        :raises TypeError: Если value не является строкой.
        :raises EmptyReviewFieldError: Если value пустая строка или состоит только из пробелов.
        :return: None.
        """
        if not isinstance(value, str):
            raise TypeError(f"Содержание должно быть строкой, получен "
                            f"{type(value).__name__}.")
        if value.strip():
            self.__content = value
        else:
            raise EmptyReviewFieldError("content")


    @property
    def author(self) -> str:
        """Возвращает автора обзора."""
        return self.__author

    @author.setter
    def author(self, value: str) -> None:
        """
        Устанавливает автора статьи.

        :param value: Новое имя автора.
        :raises TypeError: Если value не является строкой.
        :raises EmptyReviewFieldError: Если value пустая строка или состоит только из пробелов.
        :return: None.
        """
        if not isinstance(value, str):
            raise TypeError(f"Автор должен быть строкой, получен "
                            f"{type(value).__name__}.")
        if value.strip():
            self.__author = value
        else:
            raise EmptyReviewFieldError("author")


    @property
    def status(self) -> ReviewStatus:
        """Возвращает статус обзора."""
        return self.__status

    @status.setter
    def status(self, value: ReviewStatus | str) -> None:
        """
        Устанавливает статус обзора.

        :param value: Статус как объект ReviewStatus или строка.
        :raises TypeError: Если value не является ReviewStatus или строкой.
        :raises InvalidStatusError: Если строка не соответствует ни одному из допустимых значений.
        :return: None.
        """
        try:
            self.__status = ReviewStatus(value)
        except ValueError as exc:
            review_status: list[str] = [i.value for i in ReviewStatus]
            raise InvalidStatusError(value, review_status) from exc

    @property
    def date(self) -> datetime:
        """Возвращает дату и время создания обзора."""
        return self.__date

    @date.setter
    def date(self, new_date: datetime | None) -> None:
        """
        Устанавливает дату создания обзора.

        :param new_date: Дата написания обзора.
                        Если значение new_date - None, то дата автоматически сменится на актуальную.
        :raises TypeError: Если new_date не является datetime или None.
        :return: None.
        """
        if new_date is None:
            self.__date = datetime.now()
        elif isinstance(new_date, datetime):
            self.__date = new_date
        else:
            raise TypeError(
                f"Ожидается datetime или None, получен {type(new_date).__name__}."
            )

    @property
    def pros(self) -> list[str]:
        """Возвращает копию списка плюсов из обзора."""
        return self.__pros.copy()

    @pros.setter
    def pros(self, new_pros: list[str] | None) -> None:
        """
        Устанавливает список плюсов.

        :param new_pros: Новый список плюсов.
                        Если значение new_pros - None, то список минусов - [].
        :raises TypeError: Если new_pros не является list или None.
        :raises TypeError: Если хотя бы один элемент new_pros не str.
        :return: None.
        """
        if new_pros is None:
            self.__pros = []
        elif not isinstance(new_pros, list):
            raise TypeError(f"Ожидается list или None, получен {type(new_pros).__name__}.")
        elif not all(isinstance(nc, str) for nc in new_pros):
            raise TypeError("Ожидается что все элементы new_pros должны быть str.")
        else:
            self.__pros = new_pros.copy()

    @property
    def cons(self) -> list[str]:
        """Возвращает копию списка минусов из обзора."""
        return self.__cons.copy()

    @cons.setter
    def cons(self, new_cons: list[str] | None) -> None:
        """
        Устанавливает список минусов.

        :param new_cons: Новый список минусов.
                        Если значение new_cons - None, то список минусов - [].
        :raises TypeError: Если new_pros не является list или None.
        :return: None.
        """
        if new_cons is None:
            self.__cons = []
        elif not isinstance(new_cons, list):
            raise TypeError(f"Ожидается list или None, получен {type(new_cons).__name__}.")
        elif not all(isinstance(nc, str) for nc in new_cons):
            raise TypeError("Ожидается что все элементы new_cons должны быть str.")
        else:
            self.__cons = new_cons.copy()


    def add_pro(self, pro_text: str) -> None:
        """
        Добавляет новый плюс, в исходный список плюсов.
        :param pro_text: Новый плюс. Не может превышать 200 символов.
        :raises TypeError: Если pro_text не строка.
        :raises EmptyReviewFieldError: Если передан пустой текст.
        :raises ReviewTextTooLongError: Если длина текста превышает 200 символов.
        :return: None.
        """
        self._validate_text(pro_text, 'pro')
        self.__pros.append(pro_text)

    def add_con(self, con_text: str) -> None:
        """
        Добавляет новый минус, в исходный список минусов.
        :param con_text: Новый минус. Не может превышать 200 символов.
        :raises TypeError: Если con_text не строка.
        :raises EmptyReviewFieldError: Если передан пустой текст.
        :raises ReviewTextTooLongError: Если длина текста превышает 200 символов.
        :return: None.
        """
        self._validate_text(con_text, 'con')
        self.__cons.append(con_text)

    def remove_pro(self, index: int) -> None:
        """
        Удаляет плюс из общего списка плюсов по индексу.
        С проверкой диапазона.
        :param index: Индекс элементы, который нужно удалить.
        :raises IndexError: Если индекс выходит за пределы списка.
        :return: None.
        """
        try:
            del self.__pros[index]
        except IndexError as exc:
            raise IndexError(
                f'Индекс {index}  выходит за пределы списка преимуществ '
                f'(размер {len(self.__pros)}).') from exc

    def remove_con(self, index: int) -> None:
        """
        Удаляет минус из общего списка минусов по индексу.
        С проверкой диапазона.
        :param index: Индекс элементы, который нужно удалить.
        :raises IndexError: Если индекс выходит за пределы списка.
        :return: None.
        """
        try:
            del self.__cons[index]
        except IndexError as exc:
            raise IndexError(
                f"Индекс {index}  выходит за пределы списка недостатков "
                f"(размер {len(self.__cons)}).") from exc

    @staticmethod
    def _validate_text(text: str, field_type: str, max_length: int = 200) -> None:
        """
        Проверяет текст на тип, пустоту и максимальную длину.

        :param text: Проверяемая строка.
        :param field_type: Тип поля ('pro' или 'con') для сообщения об ошибках.
        :param max_length: Максимальная длина поля, по умолчанию 200 символов.
        :raises TypeError: Если text не строка.
        :raises EmptyReviewFieldError: Если передан пустой текст.
        :raises ReviewTextTooLongError: Если длина текста превышает max_length символов.
        :return: None.
        """
        if not isinstance(text, str):
            raise TypeError(f"{field_type.capitalize()} должен быть строкой,"
                            f" получен {type(text).__name__}.")
        if not text.strip():
            raise EmptyReviewFieldError(field_type)
        if len(text) > max_length:
            raise ReviewTextTooLongError(field_type, len(text))

    @classmethod
    def from_dict(cls, data: ReviewData) -> Review:
        """
        Преобразует словарь данных в экземпляр класса Review.
        :param data: Словарь с обязательными ключами: title, content
                    и опциональными: author, date, pros, cons.
        :raises MissingRequiredFieldsError: если пропущен обязательный аргумент.
        :return: экземпляр класса Review.
        """
        base_keys = ('title', 'content')

        for key in base_keys:
            if key not in data:
                raise MissingRequiredFieldsError(key)

        return cls(
            title=data['title'],
            content=data['content'],
            author=data.get('author', 'Эксперт'),
            status=data.get('status', ReviewStatus.PUBLISHED),
            date=data.get('date', None),
            pros=data.get('pros', None),
            cons=data.get('cons', None),
        )

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return (f"Info Device:\n\ttitle={self.title}\n\tcontent={self.content}"
                f"\n\tauthor={self.author}"
                f"\n\tdate={self.date}\n\tstatus={self.status}"
                f"\n\tpros={', '.join(self.pros)}\n\tcons={', '.join(self.cons)}")

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта, по которому его можно воссоздать."""
        return (f'Review(title={self.title!r}, content={self.content!r}, '
                f'author={self.author!r}, date={self.date!r}, '
                f'status=ReviewStatus.{self.status.name}, '
                f'pros={self.pros}, cons={self.cons})')
