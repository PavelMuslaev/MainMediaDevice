from ..common.exceptions import AppError


class ReviewError(AppError):
    """Базовое исключение для всех ошибок, связанных с отзывами."""
    pass


class InvalidStatusError(ReviewError):
    """
    TODO: ПОД ВОПРОСОМ ИХ НЕОБХОДИМОСТЬ
    Исключение для недопустимого статуса отзыва.

    :param status: Некорректное значение статуса.
    :param allowed: Список корректных значений статуса.
    """
    def __init__(self, status: str, allowed: list[str]):
        self._status = status
        self._allowed = allowed

        message = (
            f"Недопустимый статус: '{status}'. "
            f"Допустимые значения: {', '.join(self._allowed)}."
        )
        super().__init__(message)
