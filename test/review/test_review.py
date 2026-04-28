from datetime import datetime
import pytest

from src.common.exceptions import (
    EmptyFieldError,
    TextTooLongError,
    MissingRequiredFieldError,
    InvalidChoiceError,
)
from src.review.review import Review
from src.review.status import ReviewStatus
from src.core.config import settings

FIXED_DATE_CREATE_REVIEW = datetime(2026, 1, 1)


@pytest.fixture
def minimal_review():
    """Отзыв с обязательными полями."""
    return Review(title="Test Review", content="Test fixture content")


@pytest.fixture
def full_review():
    """Отзыв со всеми полями."""
    return Review(
        title="Test Review",
        content="Test fixture content",
        author="Test Author",
        date=FIXED_DATE_CREATE_REVIEW,
        status=ReviewStatus.DRAFT,
        pros=[
            "Test Pro 1",
            "Test Pro 2",
        ],
        cons=[
            "Test Con 1",
            "Test Con 2",
        ],
    )


class TestReview:
    def test_init_with_full_params(self, full_review):
        assert full_review.title == "Test Review"
        assert full_review.content == "Test fixture content"
        assert full_review.author == "Test Author"
        assert full_review.date == FIXED_DATE_CREATE_REVIEW
        assert full_review.status == ReviewStatus.DRAFT
        assert full_review.pros == [
            "Test Pro 1",
            "Test Pro 2",
        ]
        assert full_review.cons == [
            "Test Con 1",
            "Test Con 2",
        ]

    def test_init_with_full_params_content(self, minimal_review):
        assert minimal_review.title == "Test Review"
        assert minimal_review.content == "Test fixture content"
        assert minimal_review.author == "Эксперт"
        assert minimal_review.date is not None
        assert minimal_review.status == ReviewStatus.PUBLISHED
        assert minimal_review.pros == []
        assert minimal_review.cons == []

    @pytest.mark.parametrize(
        "title, res",
        [
            ("", EmptyFieldError),
            ("   ", EmptyFieldError),
            (None, TypeError),
        ],
    )
    def test_invalid_title(self, title: str | None, res: type[Exception]):
        with pytest.raises(res):
            Review(title=title, content="valid")

    @pytest.mark.parametrize(
        "content, res",
        [
            ("", EmptyFieldError),
            ("   ", EmptyFieldError),
            (None, TypeError),
        ],
    )
    def test_invalid_content(self, content: str | None, res: type[Exception]):
        with pytest.raises(res):
            Review(title="valid", content=content)

    @pytest.mark.parametrize(
        "author, res",
        [
            ("", EmptyFieldError),
            ("    ", EmptyFieldError),
            (None, TypeError),
        ],
    )
    def test_invalid_author(self, author: str | None, res: type[Exception]):
        with pytest.raises(res):
            Review(
                title="valid",
                content="valid",
                author=author,
            )

    @pytest.mark.parametrize(
        "status, res",
        [
            ("invalid", InvalidChoiceError),
        ],
    )
    def test_invalid_status(self, status, res, minimal_review):
        with pytest.raises(res):
            minimal_review.status = status

    @pytest.mark.parametrize(
        "status",
        [
            ReviewStatus.PUBLISHED,
            ReviewStatus.DRAFT,
            ReviewStatus.ARCHIVED,
            ReviewStatus("published"),
            ReviewStatus("draft"),
            ReviewStatus("archived"),
            "published",
            "draft",
            "archived",
        ],
    )
    def test_valid_status(self, status, minimal_review):
        minimal_review.status = status

    @pytest.mark.parametrize(
        "pros, res",
        [
            ([""], EmptyFieldError),
            (["   "], EmptyFieldError),
            ([1, 2, 3], TypeError),
            (["a" * (settings.MAX_PRO_CON_LENGTH + 1)], TextTooLongError),
        ],
    )
    def test_invalid_pros(self, pros: list, res: type[Exception], minimal_review):
        with pytest.raises(res):
            minimal_review.pros = pros

    @pytest.mark.parametrize(
        "cons, res",
        [
            ([""], EmptyFieldError),
            (["   "], EmptyFieldError),
            ([1, 2, 3], TypeError),
            (["a" * (settings.MAX_PRO_CON_LENGTH + 1)], TextTooLongError),
        ],
    )
    def test_invalid_cons(self, cons: list, res: type[Exception], minimal_review):
        with pytest.raises(res):
            minimal_review.cons = cons

    @pytest.mark.parametrize(
        "pro, res",
        [
            ("", EmptyFieldError),
            ("   ", EmptyFieldError),
            (1, TypeError),
            (None, TypeError),
            ("a" * (settings.MAX_PRO_CON_LENGTH + 1), TextTooLongError),
        ],
    )
    def test_invalid_add_pro(self, pro, res, minimal_review):
        with pytest.raises(res):
            minimal_review.add_pro(pro)

    @pytest.mark.parametrize(
        "con, res",
        [
            ("", EmptyFieldError),
            ("   ", EmptyFieldError),
            (1, TypeError),
            (None, TypeError),
            ("a" * (settings.MAX_PRO_CON_LENGTH + 1), TextTooLongError),
        ],
    )
    def test_invalid_add_con(self, con, res, minimal_review):
        with pytest.raises(res):
            minimal_review.add_con(con)

    def test_add_pro(self, full_review):
        full_review.add_pro("Test Pro 3")
        assert len(full_review.pros) == 3
        assert full_review.pros == ["Test Pro 1", "Test Pro 2", "Test Pro 3"]

    def test_add_con(self, full_review):
        full_review.add_con("Test Con 3")
        assert len(full_review.cons) == 3
        assert full_review.cons == ["Test Con 1", "Test Con 2", "Test Con 3"]

    def test_remove_pro(self, full_review):
        full_review.remove_pro(0)
        assert len(full_review.pros) == 1
        assert full_review.pros == ["Test Pro 2"]

    def test_remove_con(self, full_review):
        full_review.remove_con(0)
        assert len(full_review.cons) == 1
        assert full_review.cons == ["Test Con 2"]


    def test_invalid_remove_pro(self, full_review):
        with pytest.raises(IndexError):
            full_review.remove_pro(10)

    def test_invalid_remove_con(self, full_review):
        with pytest.raises(IndexError):
            full_review.remove_con(10)

    def test_from_dict_minimal(self):
        data = {
            "title": "Test Title",
            "content": "Test Content",
        }
        review = Review.from_dict(data)
        assert review.title == "Test Title"
        assert review.content == "Test Content"
        assert review.author == "Эксперт"
        assert review.status == ReviewStatus.PUBLISHED
        assert review.pros == []
        assert review.cons == []

    def test_from_dict_full(self):
        data = {
            "title": "Test Title",
            "content": "Test Content",
            "author": "Test Author",
            "date": FIXED_DATE_CREATE_REVIEW,
            "status": ReviewStatus.PUBLISHED,
            "pros": ["Test Pro 1", "Test Pro 2"],
            "cons": ["Test Con 1", "Test Con 2"],
        }
        review = Review.from_dict(data)
        assert review.title == "Test Title"
        assert review.content == "Test Content"
        assert review.author == "Test Author"
        assert review.status == ReviewStatus.PUBLISHED
        assert review.pros == ["Test Pro 1", "Test Pro 2"]
        assert review.cons == ["Test Con 1", "Test Con 2"]

    def test_from_dict_missing_title(self):
        with pytest.raises(MissingRequiredFieldError):
            Review.from_dict({"content": "Test Content"})

    def test_from_dict_missing_content(self):
        with pytest.raises(MissingRequiredFieldError):
            Review.from_dict({"title": "Test Title"})

    def test_pros_normalization_on_setter(self, minimal_review):
        minimal_review.pros = ["Test Pro 1     ", "     Test Pro 2   "]
        assert minimal_review.pros == ["Test Pro 1", "Test Pro 2"]

    def test_cons_normalization_on_setter(self, minimal_review):
        minimal_review.cons = ["Test Con 1     ", "     Test Con 2   "]
        assert minimal_review.cons == ["Test Con 1", "Test Con 2"]

    def test_cons_normalization_on_init(self):
        review = Review(title="T", content="C", cons=["Test Con 1     ", "     Test Con 2   "])
        assert review.cons == ["Test Con 1", "Test Con 2"]

    def test_pros_normalization_on_init(self):
        review = Review(title="T", content="C", pros=["Test Pro 1     ", "     Test Pro 2   "])
        assert review.pros == ["Test Pro 1", "Test Pro 2"]

    def test_add_pro_normalization(self, minimal_review):
        minimal_review.add_pro("    Test Pro 1    ")
        assert minimal_review.pros == ["Test Pro 1"]

    def test_add_con_normalization(self, minimal_review):
        minimal_review.add_pro("    Test Pro 1    ")
        assert minimal_review.pros == ["Test Pro 1"]

