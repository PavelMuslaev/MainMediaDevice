from src.common.exceptions import AppError
from src.review.exceptions import ReviewError


def test_review_error_inherits_from_app_error():
    assert isinstance(ReviewError("review failure"), AppError)
