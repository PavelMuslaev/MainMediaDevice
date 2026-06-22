from src.common.exceptions import AppError
from src.device.exceptions import DeviceError


def test_device_error_inherits_from_app_error():
    assert isinstance(DeviceError("device failure"), AppError)
