"""
Общие исключения для всего приложения.
"""


class AppError(Exception):
    """
    Базовое исключение для всех ожидаемых ошибок приложения.
    Все доменные исключения должны наследоваться от него.
    """
    pass


class ValidationError(AppError):
    """
    Ошибка валидации данных (неверный формат, пустое значение, выход за диапазон).
    """
    pass


class MissingRequiredFieldError(ValidationError):
    """
    Отсутствует обязательное поле в словаре или объекте.

    :param field_name: Имя отсутствующего поля.
    """
    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(f"Отсутствует обязательное поле: '{field_name}'.")


class InvalidValueError(ValidationError):
    """
    Недопустимое значение (не входит в допустимый набор, вне диапазона и т.д.)

    :param value: Некорректное значение.
    :param allowed: Список или описание допустимых значений.
    """
    def __init__(self, value: str | int, allowed: list[str] | str):
        self.value = value
        self.allowed = allowed
        if isinstance(allowed, list):
            allowed_str = ", ".join(str(v) for v in allowed)
            super().__init__(f"Недопустимое значение: '{value}'. Допустимые: {allowed_str}.")
        else:
            super().__init__(f"Недопустимое значение: '{value}'. Должно быть: {allowed}")
