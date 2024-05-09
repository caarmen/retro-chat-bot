import dataclasses


@dataclasses.dataclass
class KeyTypedEvent:
    participant_id: str
    key: str
