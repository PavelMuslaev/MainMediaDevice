import pytest

from src.common.exceptions import EmptyFieldError, TextTooLongError, YearOutOfRangeError
from src.common.validators import (
    validate_non_empty_string,
    validate_range_year,
    validate_string_length,
)


@pytest.mark.parametrize(
    "raw_value, expected",
    [
        ("value", "value"),
        ("  value", "value"),
        ("value  ", "value"),
        ("\tvalue\n", "value"),
    ],
)
def test_validate_non_empty_string_returns_normalized_value(raw_value, expected):
    assert validate_non_empty_string(raw_value, "name", "Entity") == expected


@pytest.mark.parametrize(
    "raw_value, expected_exception",
    [
        ("", EmptyFieldError),
        ("   ", EmptyFieldError),
        (None, TypeError),
        (1, TypeError),
    ],
)
def test_validate_non_empty_string_rejects_invalid_values(
    raw_value, expected_exception
):
    with pytest.raises(expected_exception):
        validate_non_empty_string(raw_value, "name", "Entity")


@pytest.mark.parametrize(
    "raw_text, max_length, expected",
    [
        ("text", 4, "text"),
        ("  text  ", 4, "text"),
    ],
)
def test_validate_string_length_returns_normalized_value(
    raw_text, max_length, expected
):
    assert validate_string_length(raw_text, "summary", max_length, "Entity") == expected


@pytest.mark.parametrize(
    "raw_text, max_length, expected_exception",
    [
        ("", 10, EmptyFieldError),
        ("   ", 10, EmptyFieldError),
        (None, 10, TypeError),
        ("too long", 3, TextTooLongError),
    ],
)
def test_validate_string_length_rejects_invalid_values(
    raw_text, max_length, expected_exception
):
    with pytest.raises(expected_exception):
        validate_string_length(raw_text, "summary", max_length, "Entity")


@pytest.mark.parametrize("year", [1990, 2000, 2026])
def test_validate_range_year_accepts_boundaries_and_inside_values(year):
    assert validate_range_year(year, 1990, 2026, "year", "Device") == year


@pytest.mark.parametrize(
    "year, expected_exception",
    [
        (1989, YearOutOfRangeError),
        (2027, YearOutOfRangeError),
        ("2020", TypeError),
        (None, TypeError),
    ],
)
def test_validate_range_year_rejects_invalid_values(year, expected_exception):
    with pytest.raises(expected_exception):
        validate_range_year(year, 1990, 2026, "year", "Device")
