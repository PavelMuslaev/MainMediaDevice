from datetime import datetime

import pytest

from src.common.exceptions import EmptyFieldError, InvalidChoiceError, YearOutOfRangeError
from src.core.config import settings
from src.device.categories import DeviceCategory
from src.device.device import Device
from src.review.review import Review


class ConcreteDevice(Device):
    def get_device_type(self) -> str:
        return "test-device"

    def get_short_description(self) -> str:
        return f"{self.brand} {self.model}"


class SuperDelegatingDevice(Device):
    def get_device_type(self) -> str:
        return super().get_device_type()

    def get_short_description(self) -> str:
        return super().get_short_description()


@pytest.fixture
def review():
    return Review(title="Review title", content="Review content")


@pytest.fixture
def full_device(review):
    return ConcreteDevice(
        brand="Brand",
        model="Model",
        category=DeviceCategory.SMARTPHONE,
        year=2024,
        image="images/device.png",
        specs={"cpu": {"model": "M1"}, "ram": "8 GB"},
        review=review,
    )


@pytest.mark.parametrize(
    "category, expected",
    [
        (DeviceCategory.SMARTPHONE, DeviceCategory.SMARTPHONE),
        ("smartphone", DeviceCategory.SMARTPHONE),
        ("laptop", DeviceCategory.LAPTOP),
    ],
)
def test_device_initializes_with_valid_category_values(category, expected):
    device = ConcreteDevice(brand="Brand", model="Model", category=category)

    assert device.brand == "Brand"
    assert device.model == "Model"
    assert device.category == expected
    assert device.year is None
    assert device.image == settings.DEFAULT_IMAGE_DEVICE
    assert device.specs == {}
    assert device.review is None


def test_device_initializes_with_full_params(full_device, review):
    assert full_device.brand == "Brand"
    assert full_device.model == "Model"
    assert full_device.category == DeviceCategory.SMARTPHONE
    assert full_device.year == 2024
    assert full_device.image == "images/device.png"
    assert full_device.specs == {"cpu": {"model": "M1"}, "ram": "8 GB"}
    assert full_device.review is review


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("brand", ""),
        ("brand", "   "),
        ("model", ""),
        ("model", "   "),
        ("image", ""),
        ("image", "   "),
    ],
)
def test_device_rejects_empty_string_fields(field_name, value):
    kwargs = {
        "brand": "Brand",
        "model": "Model",
        "category": "smartphone",
        field_name: value,
    }

    with pytest.raises(EmptyFieldError):
        ConcreteDevice(**kwargs)


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("brand", None),
        ("brand", 123),
        ("model", None),
        ("model", 123),
        ("image", 123),
    ],
)
def test_device_rejects_non_string_text_fields(field_name, value):
    kwargs = {
        "brand": "Brand",
        "model": "Model",
        "category": "smartphone",
        field_name: value,
    }

    with pytest.raises(TypeError):
        ConcreteDevice(**kwargs)


@pytest.mark.parametrize("category", ["invalid", 1, None])
def test_device_rejects_invalid_categories(category):
    with pytest.raises(InvalidChoiceError):
        ConcreteDevice(brand="Brand", model="Model", category=category)


@pytest.mark.parametrize(
    "year",
    [
        settings.DEFAULT_START_YEAR_DEVICE,
        2020,
        datetime.today().year,
    ],
)
def test_device_accepts_valid_year_values(year):
    device = ConcreteDevice(
        brand="Brand",
        model="Model",
        category="smartphone",
        year=year,
    )

    assert device.year == year


@pytest.mark.parametrize(
    "year, expected_exception",
    [
        (settings.DEFAULT_START_YEAR_DEVICE - 1, YearOutOfRangeError),
        (datetime.today().year + 1, YearOutOfRangeError),
        ("2020", TypeError),
        (None, None),
    ],
)
def test_device_year_validation(year, expected_exception):
    if expected_exception is None:
        device = ConcreteDevice(
            brand="Brand",
            model="Model",
            category="smartphone",
            year=year,
        )
        assert device.year is None
    else:
        with pytest.raises(expected_exception):
            ConcreteDevice(
                brand="Brand",
                model="Model",
                category="smartphone",
                year=year,
            )


def test_device_specs_are_deep_copied_on_init_and_access():
    specs = {"cpu": {"model": "M1"}}
    device = ConcreteDevice(
        brand="Brand",
        model="Model",
        category="smartphone",
        specs=specs,
    )

    specs["cpu"]["model"] = "M2"
    returned_specs = device.specs
    returned_specs["cpu"]["model"] = "M3"

    assert device.specs == {"cpu": {"model": "M1"}}


@pytest.mark.parametrize("specs", ["bad", 1, []])
def test_device_rejects_invalid_specs(specs):
    with pytest.raises(TypeError):
        ConcreteDevice(brand="Brand", model="Model", category="smartphone", specs=specs)


def test_device_add_spec_updates_internal_specs(full_device):
    full_device.add_spec("storage", "256 GB")

    assert full_device.specs["storage"] == "256 GB"


def test_device_remove_spec_deletes_existing_key(full_device):
    full_device.remove_spec("ram")

    assert "ram" not in full_device.specs


def test_device_remove_spec_raises_for_missing_key(full_device):
    with pytest.raises(KeyError):
        full_device.remove_spec("missing")


def test_device_review_accepts_review_or_none(review):
    device = ConcreteDevice(brand="Brand", model="Model", category="smartphone")

    device.review = review
    assert device.review is review

    device.review = None
    assert device.review is None


@pytest.mark.parametrize("review_value", ["review", 1, object()])
def test_device_review_rejects_invalid_values(review_value):
    with pytest.raises(TypeError):
        ConcreteDevice(
            brand="Brand",
            model="Model",
            category="smartphone",
            review=review_value,
        )


def test_device_abstract_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Device(brand="Brand", model="Model", category="smartphone")


def test_device_abstract_base_methods_return_none_when_delegated():
    device = SuperDelegatingDevice(brand="Brand", model="Model", category="smartphone")

    assert device.get_device_type() is None
    assert device.get_short_description() is None


def test_device_string_representation_contains_main_fields(full_device):
    result = str(full_device)

    assert "Brand: Brand" in result
    assert "Model: Model" in result
    assert "Category: smartphone" in result
    assert "Year: 2024" in result


def test_device_repr_contains_recreatable_constructor_parts(full_device):
    result = repr(full_device)

    assert "ConcreteDevice" in result
    assert "brand='Brand'" in result
    assert "model='Model'" in result
    assert "specs={'cpu': {'model': 'M1'}, 'ram': '8 GB'}" in result
