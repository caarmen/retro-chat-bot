from retrochatbot.framework.domain.entities.participant import Participant
from retrochatbot.framework.domain.repositories.room_repository import RoomRepository


class MemoryRoomRepository(RoomRepository):

    def __init__(self):
        self.participant_id_to_name: dict[str, str] = {}

    def get_participant_name(self, participant_id: str) -> str | None:
        return self.participant_id_to_name.get(participant_id)

    def update_participants(
        self, participants: list[Participant]
    ) -> RoomRepository.ParticipantChange:
        previous_ids: set[str] = set(self.participant_id_to_name.keys())
        current_ids: set[str] = {p.id for p in participants}
        left_ids: set[str] = previous_ids - current_ids
        joined_ids = current_ids - previous_ids
        self.participant_id_to_name = {p.id: p.name for p in participants}
        return RoomRepository.ParticipantChange(
            left_ids=left_ids,
            joined_ids=joined_ids,
        )
