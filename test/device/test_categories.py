import pytest

from src.device.categories import DeviceCategory


class TestCategory:
    def test_read_all_category(self):
        # Порядок должен быть таким же, как в классе
        expected = [
            DeviceCategory.SMARTPHONE.value,
            DeviceCategory.HEADPHONE.value,
            DeviceCategory.TABLET.value,
            DeviceCategory.SMARTWATCH.value,
            DeviceCategory.LAPTOP.value,
        ]
        assert DeviceCategory.to_list() == expected

    def test_from_string_converts_valid_strings(self):
        assert DeviceCategory("smartphone") == DeviceCategory.SMARTPHONE
        assert DeviceCategory("tablet") == DeviceCategory.TABLET
        assert DeviceCategory("headphone") == DeviceCategory.HEADPHONE

    def test_from_string_raises_on_invalid(self):
        with pytest.raises(ValueError):
            DeviceCategory("invalid")
