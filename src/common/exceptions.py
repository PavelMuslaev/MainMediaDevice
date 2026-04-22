"""
Общие исключения для всего приложения.

Содержит иерархию базовых исключений, используемых во всех доменных модулях.
Все ожидаемые ошибки приложения должны наследоваться от AppError.
"""


class AppError(Exception):
    """
    Базовое исключение для всех ожидаемых ошибок приложения.

    Все доменные исключения должны наследоваться от него.
    Это позволяет единообразно перехватывать любые ожидаемые ошибки:

    Пример:

    try:
        ...
    except AppError as e:
        logger.error(f"Ошибка приложения: {e}")
        logger.error(f"Ошибка приложения: {e}")
    """

    pass


class ValidationError(AppError):
    """
    Ошибка валидации данных.

    Возникает при неверном формате, пустом значении, выходе за диапазон
    или несоответствии допустимым значениям.
    """

    pass


class TextTooLongError(ValidationError):
    """
    Превышена максимальная допустимая длина текстового поля.

    :param value: Некорректное значение (слишком длинная строка).
    :param field_name: Имя поля.
    :param max_length: Максимально допустимая длина.
    :param entity: Имя сущности (класса), к которой относится поле.
    """

    def __init__(self, value: str, field_name: str, max_length: int, entity: str):
        self.value = value
        self.field_name = field_name
        self.max_length = max_length
        self.entity = entity
        super().__init__(
            f"Превышена максимальная длина поля: '{self.entity}.{self.field_name}'."
            f"Текущая длина: '{len(self.value)}'. Максимально-допустимая: '{self.max_length}'."
        )


class EmptyFieldError(ValidationError):
    """
    Поле не может быть пустым (пустая строка или строка из пробелов).

    :param field_name: Имя поля.
    :param entity: Имя сущности (класса), к которой относится поле.
    """

    def __init__(self, field_name: str, entity: str):
        self.field_name = field_name
        self.entity = entity
        super().__init__(
            f"Поле: '{self.entity}.{self.field_name}' не может быть пустым!"
        )


class MissingRequiredFieldError(ValidationError):
    """
    Отсутствует обязательное поле в словаре или объекте.

    :param field_name: Имя отсутствующего поля.
    :param entity: Имя сущности (класса), к которой относится поле.
    """

    def __init__(self, field_name: str, entity: str):
        self.field_name = field_name
        self.entity = entity
        super().__init__(
            f"Отсутствует обязательное поле: '{self.entity}.{self.field_name}'."
        )


class InvalidChoiceError(ValidationError):
    """
    Недопустимое значение (не входит в допустимый набор).

    :param value: Некорректное значение.
    :param field_name: Имя поля.
    :param allowed: Список или описание допустимых значений.
    :param entity: Имя сущности (класса), к которой относится поле.
    """

    def __init__(
        self, value: str | int, field_name: str, allowed: list[str] | str, entity: str
    ):
        self.value = value
        self.field_name = field_name
        self.allowed = allowed
        self.entity = entity
        if isinstance(allowed, list):
            allowed_str = ", ".join(str(v) for v in allowed)
            super().__init__(
                f"Недопустимое значение '{self.entity}.{self.field_name}: {value}'. Допустимые: {allowed_str}."
            )
        else:
            super().__init__(
                f"Недопустимое значение '{self.entity}.{self.field_name}: {value}'. Должно быть: {allowed}"
            )


class YearOutOfRangeError(ValidationError):
    """
    Переданный год выходит за допустимые границы.

    :param year: Переданный год.
    :param start_year: Нижняя граница диапазона (включительно).
    :param end_year: Верхняя граница диапазона (включительно).
    :param field_name: Имя поля.
    :param entity: Имя сущности (класса), к которой относится поле.
    """

    def __init__(
        self, year: int, start_year: int, end_year: int, field_name: str, entity: str
    ):
        self.year = year
        self.start_year = start_year
        self.end_year = end_year
        self.field_name = field_name
        self.entity = entity
        super().__init__(
            f"Переданный год '{self.entity}.{self.field_name}: {self.year}', "
            f"не попадает в допустимый диапазон: {self.start_year}-{self.end_year}."
        )
