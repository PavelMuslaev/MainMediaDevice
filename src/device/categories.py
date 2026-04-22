"""
Допустимые категории устройств.

Содержит перечисление всех категорий, которые могут быть присвоены устройству.
Используется для валидации и обеспечения типобезопасности при работе с категориями.
"""

from enum import StrEnum


class DeviceCategory(StrEnum):
    """
    Зарегистрированные категории устройств.

    Возможные значения:

    - `SMARTPHONE` - смартфон.
    - `HEADPHONE` - наушники.
    - `TABLET` - планшет.
    - `SMARTWATCH` - умные часы.
    - `LAPTOP` - ноутбук.

    Пример использования::

    category = DeviceCategory.SMARTPHONE
    print(category.value)  # "smartphone"

    # Проверка валидности строки
    if raw_value in DeviceCategory.to_list():
        category = DeviceCategory(raw_value)
    """

    SMARTPHONE = "smartphone"
    HEADPHONE = "headphone"
    TABLET = "tablet"
    SMARTWATCH = "smartwatch"
    LAPTOP = "laptop"

    @classmethod
    def to_list(cls) -> list[str]:
        """Возвращает значения атрибутов перечисления в виде списка строк."""
        return [str(i) for i in cls]
