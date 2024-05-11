import datetime as dt

from retrochatbot.botapi.participant_texts import ParticipantText, ParticipantTexts

KEY_BACKSPACE = "Backspace"
KEY_ENTER = "Enter"


def keys_to_text(
    participant_name: str, keys: list[str | dt.datetime]
) -> ParticipantTexts:
    result: ParticipantTexts = []
    cur_text: list[str] = []
    for key in keys:
        if key == KEY_BACKSPACE and len(cur_text) > 0:
            cur_text.pop()
        elif key == KEY_ENTER:
            cur_text.append("\n")
        elif isinstance(key, str) and len(key) == 1:
            cur_text.append(key)
        elif isinstance(key, dt.datetime):
            if cur_text:
                result.append(
                    ParticipantText(
                        participant_name=participant_name,
                        text="".join(cur_text),
                        last_event_datetime=key,
                    )
                )
            cur_text = []
        # else ignore other keys
    return result
