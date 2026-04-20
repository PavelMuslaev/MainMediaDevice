from enum import StrEnum


class AllowedCategory(StrEnum):
    """Зарегистрированные категории устройств."""
    SMARTPHONE = "smartphone"
    HEADPHONE = "headphone"
    TABLET = "tablet"
    SMARTWATCH = "smartwatch"
    LAPTOP = "laptop"

    @staticmethod
    def to_list() -> list[str]:
        """Возвращает значения атрибутов перечисления в виде списка строк."""
        return [str(i) for i in AllowedCategory]