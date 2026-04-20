from enum import StrEnum


class ReviewStatus(StrEnum):
    """Статусы хранения обзора."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

    @staticmethod
    def to_list() -> list[str]:
        """Возвращает значения атрибутов перечисления в виде списка строк."""
        return [str(i) for i in ReviewStatus]
