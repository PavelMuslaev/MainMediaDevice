"""
Исключения для модуля отзывов (Review).

Определяет базовое исключение для всех ошибок, связанных с отзывами.
Специфические исключения (например, InvalidStatusError) должны наследоваться от ReviewError.
"""

from ..common.exceptions import AppError


class ReviewError(AppError):
    """Базовое исключение для всех ошибок, связанных с обзорами."""

    pass
