import pytest

from src.review.status import ReviewStatus


class TestStatus:
    def test_read_all_status(self):
        # Порядок должен быть таким же, как в классе
        expected = [
            ReviewStatus.DRAFT.value,
            ReviewStatus.PUBLISHED.value,
            ReviewStatus.ARCHIVED.value,
        ]
        assert ReviewStatus.to_list() == expected

    def test_from_string_converts_valid_strings(self):
        assert ReviewStatus("draft") == ReviewStatus.DRAFT
        assert ReviewStatus("published") == ReviewStatus.PUBLISHED
        assert ReviewStatus("archived") == ReviewStatus.ARCHIVED

    def test_from_string_raises_on_invalid(self):
        with pytest.raises(ValueError):
            ReviewStatus("invalid")
