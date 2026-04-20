from ..common.exceptions import AppError


class ReviewError(AppError):
    """Базовое исключение для всех ошибок, связанных с отзывами."""
    pass


class EmptyReviewFieldError(ReviewError):
    """
    Исключение, возникающие при попытке установить пустое значение в обязательное поле.

    :param field_name: Имя поля, которое не может быть пустым.
    """
    def __init__(self, field_name: str):
        self._field_name = field_name
        super().__init__(f"Поле '{field_name}' не может быть пустым.")


class ReviewTextTooLongError(ReviewError):
    """
    Исключение для текстов, превышающих допустимую длину.
    Применяется преимуществам и недостаткам (pros/cons).

    :param field_type: Тип поля ('pro' or 'cons').
    :param length: Фактическая длина текста.
    :param max_length: Максимально допустимая длина (По умолчанию 200).
    """
    def __init__(self, field_type: str, length: int, max_length: int=200):
        self._field_type = field_type
        self._length = length
        self._max_length = max_length

        message = f"{field_type.capitalize()} превышает {max_length}, сейчас символов: {length}."
        super().__init__(message)


class InvalidStatusError(ReviewError):
    """
    Исключение для недопустимого статуса отзыва.

    :param status: Некорректное значение статуса.
    :param allowed: Список корректных значений статуса.
    """
    def __init__(self, status: str, allowed: list[str]):
        self._status = status
        self._allowed = allowed

        message = f"Недопустимый статус: '{status}'. Допустимые значения: {", ".join(self._allowed)}."
        super().__init__(message)
