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

    def _create_system_role_content(self):
        return (
            f"Your name is '{self._name}' and you are in a chat room. "
            "What would you like to say in this chat? "
            f"If you don't think it makes sense to say anything now, reply '{TOKEN_NOTHING}'. "
            f"NEVER reply with your name '{self._name}'"
        )

    async def on_participant_texts(
        self,
        participant_texts: ParticipantTexts,
        output_stream: Callable[[str], Awaitable],
    ):
        system_content = self._create_system_role_content()
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
                    "name": pt.participant_name,
                    "content": pt.text.strip(),
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
                did_send_something = False
                async for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        if TOKEN_NOTHING not in content:
                            await output_stream(content)
                            did_send_something = True
                        else:
                            logger.info("Bot is shy")
                # Add a trailing space to the full content which was sent.
                if did_send_something:
                    await output_stream(" ")
        except Exception as e:
            logger.exception("Error using chatgpt", exc_info=e)
            await output_stream(f"Oops {e}")
