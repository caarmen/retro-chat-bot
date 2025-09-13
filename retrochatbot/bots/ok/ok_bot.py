import logging
from typing import Awaitable, Callable

from retrochatbot.botapi.bot_api import Bot
from retrochatbot.botapi.participant_texts import ParticipantTexts

logger = logging.getLogger(__name__)


class OkBot(Bot):
    async def on_participant_texts(
        self,
        participant_texts: ParticipantTexts,
        output_stream: Callable[[str], Awaitable],
    ) -> str | None:
        logger.info(f"on_participant_texts {participant_texts}")
        await output_stream("Ok.")
