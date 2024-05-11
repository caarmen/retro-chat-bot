import itertools

from retrochatbot.botapi.participant_texts import ParticipantTexts
from retrochatbot.framework.domain.entities.participant_buffer import ParticipantBuffer
from retrochatbot.framework.domain.repositories.room_repository import RoomRepository
from retrochatbot.framework.domain.usecases import keys_to_text


def merge_participant_buffer_texts(
    repo: RoomRepository,
    buffers: dict[str, ParticipantBuffer],
) -> ParticipantTexts:
    """
    :return: the texts of the different participants, ordered by timestamp.
    """
    return sorted(
        itertools.chain(
            *[
                keys_to_text(
                    participant_name=repo.get_participant_name(participant_id),
                    keys=buffer.data.data,
                )
                for (participant_id, buffer) in buffers.items()
            ]
        ),
        key=lambda x: x.last_event_datetime,
    )
