import pytest

from retrochatbot.framework.domain.usecases import (
    KEY_BACKSPACE,
    KEY_ENTER,
    keys_to_text,
)


@pytest.mark.parametrize(
    argnames=["input_keys", "expected_text"],
    argvalues=[
        [
            ["h", "e", "l", "l", "o"],
            "hello",
        ],
        [
            ["h", "e", "l", "l", "o", KEY_BACKSPACE],
            "hell",
        ],
        [
            ["h", "e", "l", "l", "o", KEY_BACKSPACE, KEY_ENTER],
            "hell\n",
        ],
        [
            ["a", KEY_BACKSPACE, KEY_BACKSPACE],
            "",
        ],
        [
            ["a", "Meta"],
            "a",
        ],
    ],
)
def test_keys_to_text(
    input_keys: list[str],
    expected_text: str,
):
    actual_text = keys_to_text(keys=input_keys)
    assert actual_text == expected_text
