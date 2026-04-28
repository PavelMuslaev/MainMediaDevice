"""
Валидаторы общих типов данных.

Содержит набор функций для проверки и нормализации строк, списков и числовых значений.
Используется во всех доменных модулях для обеспечения целостности данных.
"""

from ..common.exceptions import EmptyFieldError, TextTooLongError, YearOutOfRangeError


def validate_non_empty_string(value: str, field_name: str, entity: str) -> str:
    """
    Проверяет, что переданное значение является непустой строкой.

    :param value: Проверяемое значение.
    :param field_name: Имя поля (для сообщения об ошибке).
    :param entity: Имя сущности (класса), к которому относится поле.

    :return: Исходная строка (С автоматической обрезкой пробелов).

    :raises TypeError: Если value не является строкой.
    :raises EmptyFieldError: Если строка пустая или состоит только из пробелов.
    """

    if not isinstance(value, str):
        raise TypeError(
            f"Поле '{field_name}.{entity}' должно быть str, получен {type(value).__name__}"
        )

    if not (normalized := value.strip()):
        raise EmptyFieldError(field_name, entity)

    return normalized


def validate_string_length(
    text: str, field_name: str, max_length: int, entity: str
) -> str:
    """
    Проверяет, что строка не пуста и не превышает максимальную длину.

    :param text: Проверяемая строка.
    :param field_name: Имя поля.
    :param max_length: Максимально допустимая длина.
    :param entity: Имя сущности (класса), к которому относится поле.

    :return: Исходная строка (С автоматической обрезкой пробелов).

    :raises TypeError: Если text не является строкой.
    :raises EmptyFieldError: Если строка пустая.
    :raises TextTooLongError: Если длина строки превышает max_length.
    """
    normalized = validate_non_empty_string(text, field_name, entity)
    if len(normalized) > max_length:
        raise TextTooLongError(normalized, field_name, max_length, entity)

    return normalized


def validate_range_year(
    year: int, start_year: int, end_year: int, field_name: str, entity: str
) -> int:
    """
    Проверяет, что год попадает в заданный диапазон (включительно).

    :param year: Проверяемый год.
    :param start_year: Нижняя граница диапазона.
    :param end_year: Верхняя граница диапазона.
    :param field_name: Имя поля (для сообщения об ошибке).
    :param entity: Имя сущности (класса), к которому относится поле.

    :return: Переданный год (без изменений).

    :raises TypeError: Если year не является целым числом.
    :raises YearOutOfRangeError: Если год вне допустимого диапазона.
    """
    if not isinstance(year, int):
        raise TypeError("Год должен быть установлен в виде целого числа.")

    if not (start_year <= year <= end_year):
        raise YearOutOfRangeError(year, start_year, end_year, field_name, entity)

    return year
