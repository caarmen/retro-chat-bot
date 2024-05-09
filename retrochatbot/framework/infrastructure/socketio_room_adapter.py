import logging

from socketio import AsyncClientNamespace

from retrochatbot.framework.domain.adapters.room_adapter import RoomAdapter
from retrochatbot.framework.domain.entities.key_typed_event import KeyTypedEvent
from retrochatbot.framework.domain.entities.participant import Participant

logger = logging.getLogger(__name__)


class SocketIoRoomAdapter(RoomAdapter, AsyncClientNamespace):
    def on_connect(self):
        self._notify_id(self.my_id)

    async def on_typed(self, data):
        self._notify_key_typed_event(
            KeyTypedEvent(
                participant_id=data["sid"],
                key=data["key"],
            )
        )

    async def on_joined(self, data):
        self._on_participants_changed(data["participants"])

    async def on_left(self, data):
        self._on_participants_changed(data["participants"])

    def _on_participants_changed(self, participant_data: list[dict[str, str]]):
        participants: list[Participant] = [
            Participant(**item) for item in participant_data
        ]
        logger.info(f"participants now {participants}")
        self._notify_participants(participants)

    async def send_text(
        self,
        text: str,
    ):
        for key in text:
            await self.emit(
                event="typed",
                data={
                    "key": key,
                    "ctrl": False,
                },
            )

    @property
    def my_id(self) -> str:
        return self.client.namespaces.get(self.namespace, self.client.sid)
