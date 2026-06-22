import pytest

from src.common.exceptions import (
    AppError,
    EmptyFieldError,
    InvalidChoiceError,
    MissingRequiredFieldError,
    TextTooLongError,
    ValidationError,
    YearOutOfRangeError,
)


@pytest.mark.parametrize(
    "exception",
    [
        EmptyFieldError("title", "Review"),
        MissingRequiredFieldError("content", "Review"),
        InvalidChoiceError("bad", "status", ["draft", "published"], "Review"),
        InvalidChoiceError("bad", "status", "known status", "Review"),
        TextTooLongError("abcdef", "pros", 5, "Review"),
        YearOutOfRangeError(1989, 1990, 2026, "year", "Device"),
    ],
)
def test_validation_exceptions_inherit_from_app_error(exception):
    assert isinstance(exception, ValidationError)
    assert isinstance(exception, AppError)


def test_text_too_long_error_stores_context():
    error = TextTooLongError("abcdef", "pros", 5, "Review")

    assert error.value == "abcdef"
    assert error.field_name == "pros"
    assert error.max_length == 5
    assert error.entity == "Review"
    assert "Review" in str(error)


def test_invalid_choice_error_stores_list_context():
    error = InvalidChoiceError("bad", "status", ["draft", "published"], "Review")

    assert error.value == "bad"
    assert error.field_name == "status"
    assert error.allowed == ["draft", "published"]
    assert error.entity == "Review"
    assert "draft" in str(error)


def test_year_out_of_range_error_stores_context():
    error = YearOutOfRangeError(1989, 1990, 2026, "year", "Device")

    assert error.year == 1989
    assert error.start_year == 1990
    assert error.end_year == 2026
    assert error.field_name == "year"
    assert error.entity == "Device"
