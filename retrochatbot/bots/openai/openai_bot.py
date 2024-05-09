import json
import logging
from typing import Awaitable, Callable

from openai import AsyncOpenAI

from retrochatbot.botapi.bot_api import Bot
from retrochatbot.botapi.participant_texts import ParticipantTexts

TOKEN_NOTHING = "__"

logger = logging.getLogger(__name__)


class OpenAiBot(Bot):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client = AsyncOpenAI()

    def _create_system_role_content(self, participant_texts: ParticipantTexts):
        return (
            "You are in a chat room using technology from the 90s. "
            "The UI is terminal-based. It is split screen, with one "
            "portion of the screen for each participant. Participants "
            "see each other type in real time, letter by letter. "
            f"There are {len(participant_texts)} participants in the room now. "
            f"You are one of the participants. Your name is '{self._name}'."
            "Given the following texts for the different participants, "
            "you can choose to type something now, or to not type anything for now. "
            f"If you don't think it makes sense to say anything now, reply '{TOKEN_NOTHING}'. "
            "Otherwise, reply the text you would like to say. "
            f"In any case, NEVER prefix your messages with <{self._name}> and NEVER include a timestamp."
        )

    async def on_participant_texts(
        self,
        participant_texts: ParticipantTexts,
        output_stream: Callable[[str], Awaitable],
    ):
        system_content = self._create_system_role_content(participant_texts)
        logger.debug(f"system content: {system_content}")
        messages = [
            {"role": "system", "content": system_content},
        ]
        messages.extend(
            [
                {
                    "role": (
                        "assistant" if pt.participant_name == self._name else "user"
                    ),
                    "content": f"{pt.last_event_datetime.strftime('%H:%M:%S')} <{pt.participant_name}> {pt.text}",
                }
                for pt in participant_texts
                if pt.text.strip()
            ]
        )
        logger.info(f"{json.dumps(messages, indent=2)}")
        try:
            stream = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                stream=True,
            )
            if stream:
                async for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        if TOKEN_NOTHING not in content:
                            await output_stream(content)
                        else:
                            logger.info("Bot is shy")
        except Exception as e:
            logger.exception("Error using chatgpt", exc_info=e)
            await output_stream(f"Oops {e}")
