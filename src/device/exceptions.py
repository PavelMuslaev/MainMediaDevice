"""
Исключения для модуля устройство (Device).

Определяет базовое исключение для всех ошибок, связанных с устройствами.
Специфические исключения (например, InvalidCategoryError) должны наследоваться от DeviceError.
"""

from ..common.exceptions import AppError


class DeviceError(AppError):
    """Базовое исключение для всех ошибок, связанных с устройствами."""

    pass
