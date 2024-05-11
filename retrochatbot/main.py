import argparse
import asyncio
import logging
from typing import Protocol
from urllib import parse

import socketio

from retrochatbot.framework.data.memory_room_repository import MemoryRoomRepository
from retrochatbot.framework.domain.usecases import load_bot
from retrochatbot.framework.domain.usecases.participant_buffer_aggregator import (
    ParticipantBufferAggregator,
)
from retrochatbot.framework.infrastructure.socketio_room_adapter import (
    SocketIoRoomAdapter,
)


class Arguments(Protocol):
    host: str
    room_id: str
    participant_name: str
    bot_class: str
    debounce_seconds: float
    log_level: str


async def connect(args: Arguments):
    url_qs = parse.urlencode(
        {
            "room_id": args.room_id,
            "participant_name": args.participant_name,
        }
    )
    url = f"{args.host}?{url_qs}"

    room_adapter = SocketIoRoomAdapter()

    bot = load_bot(
        full_bot_class_name=args.bot_class,
        participant_name=args.participant_name,
    )
    ParticipantBufferAggregator(
        repo=MemoryRoomRepository(),
        adapter=room_adapter,
        debounce_s=args.debounce_seconds,
        cb_participant_texts_ready=lambda participant_texts: bot.on_participant_texts(
            participant_texts, output_stream=room_adapter.send_text
        ),
    )

    sio = socketio.AsyncClient()
    sio.register_namespace(room_adapter)
    await sio.connect(
        url=url,
        socketio_path="/chat",
    )
    await sio.wait()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--room_id", required=True)
    parser.add_argument("--participant_name", required=True)
    parser.add_argument("--bot_class", required=True)
    parser.add_argument(
        "--debounce_seconds", default=5.0, type=float, help="(default %(default)s)"
    )
    parser.add_argument(
        "--log_level",
        required=False,
        choices=logging.getLevelNamesMapping().keys(),
        default="WARNING",
        help="(default %(default)s)",
    )

    args: Arguments = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    await connect(args)


if __name__ == "__main__":
    asyncio.run(main())
