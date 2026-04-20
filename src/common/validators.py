from datetime import datetime

from ..common.exceptions import EmptyFieldError, TextTooLongError
from ..device.exceptions import InvalidYearDeviceError


def validate_non_empty_string(value: str, field_name: str, entity: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"Поле '{field_name} {entity}' должно быть str, получен {type(value).__name__}"
        )
    if not value.strip():
        raise EmptyFieldError(field_name, entity)

    return value


def validate_string_length(
    text: str, field_name: str, max_length: int, entity: str
) -> str:
    text = validate_non_empty_string(text, field_name, entity)
    if len(text) > max_length:
        raise TextTooLongError(text, field_name, max_length, entity)

    return text


def validate_list_string(value_list: list[str], entity: str) -> list[str]:
    if not isinstance(value_list, list):
        raise TypeError(
            f"'value_list {entity}' должен быть list, получен {type(value_list).__name__}"
        )

    for i, item in enumerate(value_list):
        if not isinstance(item, str):
            raise TypeError(
                f"Элемент с индексом {i} не является строкой: {item!r} {entity}."
            )
        if not item.strip():
            raise ValueError(
                f"Элемент с индексом {i} пустая строка или состоит из пробелов: {item!r} {entity}."
            )

    return value_list.copy()


def validate_range_year(year: int, start_year: int, end_year: int) -> int:
    if isinstance(year, int):
        if 1990 < year < datetime.now().year:
            return year
        raise InvalidYearDeviceError(year, start_year, end_year)
    raise ValueError("Год должен быть установлен в виде целого числа.")
