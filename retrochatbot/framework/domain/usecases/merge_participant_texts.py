import itertools

from retrochatbot.botapi.participant_texts import ParticipantTexts
from retrochatbot.framework.domain.repositories.room_repository import RoomRepository
from retrochatbot.framework.domain.usecases import buffer_data_to_participant_texts
from retrochatbot.framework.domain.usecases.participant_buffer import ParticipantBuffer


def merge_participant_texts(
    repo: RoomRepository,
    buffers: dict[str, ParticipantBuffer],
) -> ParticipantTexts:
    """
    :return: the texts of the different participants, ordered by timestamp.
    """
    return sorted(
        itertools.chain(
            *[
                buffer_data_to_participant_texts(
                    participant_name=repo.get_participant_name(participant_id),
                    keys=buffer.data.data,
                )
                for (participant_id, buffer) in buffers.items()
            ]
        ),
        key=lambda x: x.last_event_datetime,
    )
