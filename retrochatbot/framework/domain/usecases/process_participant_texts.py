from retrochatbot.botapi.bot_api import Bot
from retrochatbot.botapi.participant_texts import ParticipantTexts
from retrochatbot.framework.domain.adapters.room_adapter import RoomAdapter


async def process_participant_texts(
    adapter: RoomAdapter,
    bot: Bot,
    participant_texts: ParticipantTexts,
):
    await bot.on_participant_texts(participant_texts, output_stream=adapter.send_text)
