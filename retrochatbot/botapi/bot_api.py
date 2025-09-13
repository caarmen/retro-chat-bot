from abc import ABC, abstractmethod
from typing import Awaitable, Callable

from retrochatbot.botapi.participant_texts import ParticipantTexts


class Bot(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    async def on_participant_texts(
        self,
        participant_texts: ParticipantTexts,
        output_stream: Callable[[str], Awaitable],
    ):
        """
        :param participant_texts: texts for the different participants in the chat.
        :return: a message to send to the chat. Return None to not reply anything at this time.
        """
        raise NotImplementedError()
