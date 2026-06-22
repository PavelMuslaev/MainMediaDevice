import pytest

from src.common.exceptions import EmptyFieldError, TextTooLongError
from src.core.config import settings
from src.review.review import ProsConsList


@pytest.fixture
def pros_cons_list():
    return ProsConsList.from_collections(
        ["  Fast  ", "Compact"],
        field_name="pros",
    )


def test_pros_cons_list_from_none_creates_empty_list():
    result = ProsConsList.from_collections(None, field_name="pros")

    assert len(result) == 0
    assert result.to_list() == []


def test_pros_cons_list_normalizes_items(pros_cons_list):
    assert pros_cons_list.to_list() == ["Fast", "Compact"]


def test_pros_cons_list_returns_copy(pros_cons_list):
    result = pros_cons_list.to_list()
    result.append("Changed")

    assert pros_cons_list.to_list() == ["Fast", "Compact"]


def test_pros_cons_list_supports_len_iteration_and_indexing(pros_cons_list):
    assert len(pros_cons_list) == 2
    assert list(pros_cons_list) == ["Fast", "Compact"]
    assert pros_cons_list[0] == "Fast"


def test_pros_cons_list_add_returns_new_instance(pros_cons_list):
    result = pros_cons_list.add("  Durable  ")

    assert pros_cons_list.to_list() == ["Fast", "Compact"]
    assert result.to_list() == ["Fast", "Compact", "Durable"]


def test_pros_cons_list_remove_returns_new_instance(pros_cons_list):
    result = pros_cons_list.remove(0)

    assert pros_cons_list.to_list() == ["Fast", "Compact"]
    assert result.to_list() == ["Compact"]


@pytest.mark.parametrize(
    "collections, expected_exception",
    [
        ("single string", TypeError),
        ([1], TypeError),
        ([""], EmptyFieldError),
        (["   "], EmptyFieldError),
        (["a" * (settings.MAX_PRO_CON_LENGTH + 1)], TextTooLongError),
    ],
)
def test_pros_cons_list_rejects_invalid_collections(
    collections, expected_exception
):
    with pytest.raises(expected_exception):
        ProsConsList.from_collections(collections, field_name="pros")


@pytest.mark.parametrize(
    "item, expected_exception",
    [
        (1, TypeError),
        ("", EmptyFieldError),
        ("   ", EmptyFieldError),
        ("a" * (settings.MAX_PRO_CON_LENGTH + 1), TextTooLongError),
    ],
)
def test_pros_cons_list_add_rejects_invalid_items(
    item, expected_exception, pros_cons_list
):
    with pytest.raises(expected_exception):
        pros_cons_list.add(item)


@pytest.mark.parametrize("index", [2, -3])
def test_pros_cons_list_remove_rejects_out_of_range_index(index, pros_cons_list):
    with pytest.raises(IndexError):
        pros_cons_list.remove(index)
