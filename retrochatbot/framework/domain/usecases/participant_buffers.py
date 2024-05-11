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


class ParticipantBuffers:
    def __init__(
        self,
        repo: RoomRepository,
        adapter: RoomAdapter,
        callback: Callable[[ParticipantTexts], None],
        debounce_s: float,
    ):
        self.repo = repo
        self.callback = callback
        self.buffers: dict[str, ParticipantBuffer] = {}
        self._debounce_s = debounce_s
        adapter.subscribe_participants(
            lambda participants: self.update_participants(participants)
        )
        adapter.subscribe_key_typed_events(
            lambda key_typed_event: self.append(
                key_typed_event.participant_id, key_typed_event.key
            )
        )
        adapter.subscribe_id(lambda id: self._update_id(id))

    def _update_id(self, id: str):
        my_buffer = self.buffers[id]
        my_buffer.is_self = True

    def update_participants(
        self,
        participants: list[Participant],
    ):
        participant_change: RoomRepository.ParticipantChange = (
            self.repo.update_participants(participants)
        )

        for left_id in participant_change.left_ids:
            del self.buffers[left_id]
        buffer_size = calculate_participant_buffer_size(
            participant_count=len(participants)
        )
        for buffer in self.buffers.values():
            buffer.resize(size=buffer_size)
        for joined_id in participant_change.joined_ids:
            self.buffers[joined_id] = ParticipantBuffer(
                size=buffer_size,
                debounce_s=self._debounce_s,
                burst_callback=self.burst_callback,
            )

    def append(
        self,
        participant_id: str,
        key: str,
    ):
        buffer: ParticipantBuffer = self.buffers.get(participant_id)
        if buffer:
            buffer.append(key)

    async def burst_callback(self):
        participant_texts = merge_participant_buffer_texts(self.repo, self.buffers)
        await self.callback(participant_texts)
