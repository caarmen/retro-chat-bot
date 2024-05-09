from retrochatbot.botapi.participant_texts import ParticipantText, ParticipantTexts
from retrochatbot.framework.domain.entities.participant_buffer import ParticipantBuffer
from retrochatbot.framework.domain.repositories.room_repository import RoomRepository
from retrochatbot.framework.domain.usecases import keys_to_text


def merge_participant_buffer_texts(
    repo: RoomRepository,
    buffers: dict[str, ParticipantBuffer],
) -> ParticipantTexts:
    """
    :return: a list of participant name to buffer text.
    """
    return sorted(
        [
            ParticipantText(
                participant_name=repo.get_participant_name(participant_id),
                text=keys_to_text(buffer.data.data),
                last_event_datetime=buffer.last_event_datetime,
            )
            for (participant_id, buffer) in buffers.items()
            if buffer.last_event_datetime
        ],
        key=lambda x: x.last_event_datetime,
    )
