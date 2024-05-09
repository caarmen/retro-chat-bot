import dataclasses
import datetime as dt


@dataclasses.dataclass
class ParticipantText:
    participant_name: str
    text: str
    last_event_datetime: dt.datetime


ParticipantTexts = list[ParticipantText]
