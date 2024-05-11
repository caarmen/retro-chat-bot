import datetime as dt

import pytest

from retrochatbot.botapi.participant_texts import ParticipantText, ParticipantTexts
from retrochatbot.framework.domain.usecases import (
    KEY_BACKSPACE,
    KEY_ENTER,
    buffer_data_to_participant_texts,
)

DATETIME_PAST_1 = dt.datetime(1996, 1, 1, 11, 55, 0)
DATETIME_PAST_2 = dt.datetime(1996, 1, 1, 11, 57, 0)


@pytest.mark.parametrize(
    argnames=["input_keys", "expected_text"],
    argvalues=[
        [
            ["h", "e", "l", "l", "o", DATETIME_PAST_1],
            [
                ParticipantText(
                    participant_name="jdoe",
                    text="hello",
                    last_event_datetime=DATETIME_PAST_1,
                )
            ],
        ],
        [
            ["h", "e", "l", "l", "o", KEY_BACKSPACE, DATETIME_PAST_1],
            [
                ParticipantText(
                    participant_name="jdoe",
                    text="hell",
                    last_event_datetime=DATETIME_PAST_1,
                )
            ],
        ],
        [
            ["h", "e", "l", "l", "o", KEY_BACKSPACE, KEY_ENTER, DATETIME_PAST_1],
            [
                ParticipantText(
                    participant_name="jdoe",
                    text="hell\n",
                    last_event_datetime=DATETIME_PAST_1,
                )
            ],
        ],
        [
            ["a", KEY_BACKSPACE, KEY_BACKSPACE, DATETIME_PAST_1],
            [],
        ],
        [
            ["a", "Meta", DATETIME_PAST_1],
            [
                ParticipantText(
                    participant_name="jdoe",
                    text="a",
                    last_event_datetime=DATETIME_PAST_1,
                )
            ],
        ],
        [
            ["h", "i", DATETIME_PAST_1],
            [
                ParticipantText(
                    participant_name="jdoe",
                    text="hi",
                    last_event_datetime=DATETIME_PAST_1,
                )
            ],
        ],
        [
            ["h", "i", DATETIME_PAST_1, "h", "i", "?"],
            [
                ParticipantText(
                    participant_name="jdoe",
                    text="hi",
                    last_event_datetime=DATETIME_PAST_1,
                ),
            ],
        ],
        [
            ["h", "i", DATETIME_PAST_1, "h", "i", "?", DATETIME_PAST_2],
            [
                ParticipantText(
                    participant_name="jdoe",
                    text="hi",
                    last_event_datetime=DATETIME_PAST_1,
                ),
                ParticipantText(
                    participant_name="jdoe",
                    text="hi?",
                    last_event_datetime=DATETIME_PAST_2,
                ),
            ],
        ],
    ],
)
def test_buffer_data_to_participant_texts(
    input_keys: list[str],
    expected_text: ParticipantTexts,
):

    actual_text = buffer_data_to_participant_texts(
        participant_name="jdoe",
        keys=input_keys,
    )
    assert actual_text == expected_text
