class DeviceError(Exception):
    ...

class InvalidAllowedCategoryError(DeviceError):
    def __init__(self, cur_category: str, categories: list[str]):
        self._category = cur_category
        self._categories = categories

        super().__init__(
            f"Недопустимая категория: {self._category}. Допустимые значения: {", ".join(self._categories)}."
        )


class InvalidDeviceYearError(DeviceError):
    def __init__(self, year: int, cor_start_year: int, cor_end_year: int) -> None:
        self._year = year
        self._cor_start_year = cor_start_year
        self._cor_end_year = cor_end_year

        super().__init__(
            f"Некорректное значение кода: {self._year}. Допустимый диапазон: "
            f"{self._cor_start_year}-{self._cor_end_year}."
        )


class MissBaseKeyErrorDevice(DeviceError):
    def __init__(self, base_key: str):
        self._base_key = base_key
        super().__init__(f"Пропущен базовый ключ: {self._base_key}.")
