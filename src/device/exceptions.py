from ..common.exceptions import AppError


class DeviceError(AppError):
    """Базовое исключение для всех ошибок, связанных с устройствами."""
    pass


class InvalidAllowedCategoryError(DeviceError):
    """
    Возникает если пользователь пытается установить не зарегистрированную категорию устройства.

    :param cur_category: Категория переданная пользователем.
    :param categories: Список зарегистрированных категорий.
    """
    def __init__(self, cur_category: str, categories: list[str]):
        self._category = cur_category
        self._categories = categories

        message = f"Недопустимая категория: {self._category}. Допустимые значения: {", ".join(self._categories)}."
        super().__init__(message)


class InvalidDeviceYearError(DeviceError):
    """
    Возникает при попытке установить некорректный год устройства.

    :param year: Год переданный пользователем.
    :param start_year: Допустимое начало диапазона.
    :param end_year: Допустимый конец диапазона.
    """
    def __init__(self, year: int, start_year: int, end_year: int) -> None:
        self._year = year
        self._start_year = start_year
        self._end_year = end_year

        message = f"Некорректный год: {self._year}. Допустимый диапазон: {self._start_year}-{self._end_year}."
        super().__init__(message)
