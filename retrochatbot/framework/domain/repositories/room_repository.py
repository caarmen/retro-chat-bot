import dataclasses
from abc import ABC, abstractmethod

from retrochatbot.framework.domain.entities.participant import Participant


class RoomRepository(ABC):

    @abstractmethod
    def get_participant_name(
        self,
        participant_id: str,
    ) -> str | None:
        pass

    @dataclasses.dataclass
    class ParticipantChange:
        left_ids: list[str]
        joined_ids: list[str]

    @abstractmethod
    def update_participants(self, participants: list[Participant]) -> ParticipantChange:
        pass
