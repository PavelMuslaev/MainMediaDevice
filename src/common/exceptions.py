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


class TextTooLongError(ValidationError):
    def __init__(self, value: str, field_name: str, max_length: int, entity: str):
        self.value = value
        self.field_name = field_name
        self.max_length = max_length
        self.entity = entity
        super().__init__(
            f"Превышена максимальная длина поля: '{self.field_name} {self.entity}'."
            f"Текущая длина: '{len(self.value)}'. Максимально-допустимая: '{self.max_length}'."
        )


class EmptyFieldError(ValidationError):
    def __init__(self, field_name: str, entity: str):
        self.field_name = field_name
        self.entity = entity
        super().__init__(
            f"Поле: '{self.field_name} {self.entity}'  не может быть пустым!"
        )


class MissingRequiredFieldError(ValidationError):
    """
    Отсутствует обязательное поле в словаре или объекте.

    :param field_name: Имя отсутствующего поля.
    """

    def __init__(self, field_name: str, entity: str):
        self.field_name = field_name
        self.entity = entity
        super().__init__(
            f"Отсутствует обязательное поле: '{self.field_name} {self.entity}'."
        )


class InvalidChoiceError(ValidationError):
    """
    Недопустимое значение (не входит в допустимый набор, вне диапазона и т.д.)

    :param value: Некорректное значение.
    :param allowed: Список или описание допустимых значений.
    """

    def __init__(self, value: str | int, allowed: list[str] | str, entity: str):
        self.value = value
        self.allowed = allowed
        self.entity = entity
        if isinstance(allowed, list):
            allowed_str = ", ".join(str(v) for v in allowed)
            super().__init__(
                f"Недопустимое значение: '{value} {self.entity}'. Допустимые: {allowed_str}."
            )
        else:
            super().__init__(
                f"Недопустимое значение: '{value}'. Должно быть: {allowed}"
            )
