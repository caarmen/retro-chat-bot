import logging
from abc import ABC, abstractmethod
from typing import Callable

from retrochatbot.framework.domain.entities.key_typed_event import KeyTypedEvent
from retrochatbot.framework.domain.entities.participant import Participant

ParticipantObserver = Callable[[list[Participant]], None]
KeyTypedObserver = Callable[[KeyTypedEvent], None]
IdObserver = Callable[[str], None]

logger = logging.getLogger(__name__)


class RoomAdapter(ABC):
    """
    Provides bidirectional communication with the remote room.
    Allows sending text to the server, and being notified of participant
    changes and participant text events.
    """

    def __init__(self):
        super().__init__("/")
        self._id_observers: list[IdObserver] = []
        self._participant_observers: list[ParticipantObserver] = []
        self._key_typed_observers: list[KeyTypedObserver] = []

    def subscribe_id(self, observer: IdObserver):
        self._id_observers.append(observer)

    def subscribe_participants(self, observer: ParticipantObserver):
        self._participant_observers.append(observer)

    def subscribe_key_typed_events(self, observer: KeyTypedObserver):
        self._key_typed_observers.append(observer)

    def unsubscribe_id(self, observer: IdObserver):
        self._id_observers.remove(observer)

    def unsubscribe_participants(self, observer: ParticipantObserver):
        self._participant_observers.remove(observer)

    def unsubscribe_key_typed_events(self, observer: KeyTypedObserver):
        self._key_typed_observers.remove(observer)

    def _notify_id(self, id: str):
        for observer in self._id_observers:
            try:
                observer(id)
            except Exception as e:
                logger.exception(f"Exception in id observer: {e}", exc_info=e)

    def _notify_key_typed_event(self, key_typed_event: KeyTypedEvent):
        for observer in self._key_typed_observers:
            try:
                observer(key_typed_event)
            except Exception as e:
                logger.exception(f"Exception in typed event observer: {e}", exc_info=e)

    def _notify_participants(self, participants: list[Participant]):
        for observer in self._participant_observers:
            try:
                observer(participants)
            except Exception as e:
                logger.exception(
                    f"Exception in typed participant observer: {e}", exc_info=e
                )

    @abstractmethod
    async def send_text(self, text: str):
        raise NotImplementedError()
