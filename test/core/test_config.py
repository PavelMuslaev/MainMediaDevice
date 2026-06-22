import pytest
from pydantic import ValidationError

from src.core.config import AppSettings, settings


def test_default_settings_values():
    assert settings.MAX_PRO_CON_LENGTH == 200
    assert settings.DEFAULT_START_YEAR_DEVICE == 1990
    assert settings.DEFAULT_IMAGE_DEVICE == "images/"


def test_app_settings_accepts_explicit_values():
    custom_settings = AppSettings(
        MAX_PRO_CON_LENGTH=50,
        DEFAULT_START_YEAR_DEVICE=2000,
        DEFAULT_IMAGE_DEVICE="custom/",
    )

    assert custom_settings.MAX_PRO_CON_LENGTH == 50
    assert custom_settings.DEFAULT_START_YEAR_DEVICE == 2000
    assert custom_settings.DEFAULT_IMAGE_DEVICE == "custom/"


@pytest.mark.parametrize(
    "field_name",
    ["MAX_PRO_CON_LENGTH", "DEFAULT_START_YEAR_DEVICE"],
)
def test_app_settings_rejects_non_positive_integer_fields(field_name):
    values = {
        "MAX_PRO_CON_LENGTH": 50,
        "DEFAULT_START_YEAR_DEVICE": 2000,
        "DEFAULT_IMAGE_DEVICE": "custom/",
        field_name: 0,
    }

    with pytest.raises(ValidationError):
        AppSettings(**values)
