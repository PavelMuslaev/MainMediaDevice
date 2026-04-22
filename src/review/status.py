"""
Статусы отзывов (Review).

Содержит перечисление возможных состояний, в которых может находиться отзыв.
"""

from enum import StrEnum


class ReviewStatus(StrEnum):
    """
    Статусы хранения обзора.

    Возможные значения:

    - `DRAFT` - черновик (ещё не опубликован, доступен только автору).
    - `PUBLISHED` - опубликован (виден всем пользователям).
    - `ARCHIVED` - архив (скрыт из общего доступа, но сохранён в системе).

    Пример использования:

    status = ReviewStatus.PUBLISHED
    print(status.value)  # "published"
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

    @classmethod
    def to_list(cls) -> list[str]:
        """Возвращает все допустимые значения статусов в виде списка строк."""
        return [str(i) for i in cls]
