from typing import Callable

from retrochatbot.botapi.participant_texts import ParticipantTexts
from retrochatbot.framework.domain.adapters.room_adapter import RoomAdapter
from retrochatbot.framework.domain.entities.participant import Participant
from retrochatbot.framework.domain.repositories.room_repository import RoomRepository
from retrochatbot.framework.domain.usecases.participant_buffer import ParticipantBuffer
from retrochatbot.framework.domain.usecases.participant_buffer_size import (
    calculate_participant_buffer_size,
)
from retrochatbot.framework.domain.usecases.participant_buffer_texts import (
    merge_participant_buffer_texts,
)


class ParticipantBufferAggregator:
    def __init__(
        self,
        repo: RoomRepository,
        adapter: RoomAdapter,
        cb_participant_texts_ready: Callable[[ParticipantTexts], None],
        debounce_s: float,
    ):
        self._repo = repo
        self._cb_participant_texts_ready = cb_participant_texts_ready
        self._buffers: dict[str, ParticipantBuffer] = {}
        self._debounce_s = debounce_s
        adapter.subscribe_participants(
            lambda participants: self._on_participants_changed(participants)
        )
        adapter.subscribe_key_typed_events(
            lambda key_typed_event: self._on_participant_typed(
                key_typed_event.participant_id, key_typed_event.key
            )
        )
        adapter.subscribe_id(lambda id: self._on_id_changed(id))

    def _on_id_changed(self, id: str):
        self._buffers[id].is_bot_participant = True

    def _on_participants_changed(
        self,
        participants: list[Participant],
    ):
        participant_change: RoomRepository.ParticipantChange = (
            self._repo.update_participants(participants)
        )

        # Delete buffers of participants who left
        for left_id in participant_change.left_ids:
            del self._buffers[left_id]

        # Resize buffers of remaining participants
        buffer_size = calculate_participant_buffer_size(
            participant_count=len(participants)
        )
        for buffer in self._buffers.values():
            buffer.resize(size=buffer_size)

        # Create buffers for new participants
        for joined_id in participant_change.joined_ids:
            self._buffers[joined_id] = ParticipantBuffer(
                size=buffer_size,
                debounce_s=self._debounce_s,
                cb_participant_stopped_typing=self._on_participant_stopped_typing,
            )

    def _on_participant_typed(
        self,
        participant_id: str,
        key: str,
    ):
        buffer: ParticipantBuffer = self._buffers.get(participant_id)
        if buffer:
            buffer.append(key)

    async def _on_participant_stopped_typing(self):
        participant_texts = merge_participant_buffer_texts(self._repo, self._buffers)
        await self._cb_participant_texts_ready(participant_texts)
