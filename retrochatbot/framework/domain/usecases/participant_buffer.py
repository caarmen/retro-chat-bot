import asyncio
import datetime as dt
import logging
from typing import Callable

from retrochatbot.framework.common.bounded_drop_queue import BoundedDropQueue
from retrochatbot.framework.domain.usecases.buffer_data_to_participant_texts import (
    KEY_BACKSPACE,
    KEY_ENTER,
)

logger = logging.getLogger(__name__)


class ParticipantBuffer:
    """
    Represents the buffer of key events sent by one participant.
    """

    def __init__(
        self,
        size: int,
        debounce_s: int,
        cb_participant_stopped_typing: Callable[[], None],
    ):
        self.data: BoundedDropQueue[str | dt.datetime] = BoundedDropQueue(max_size=size)
        self.is_bot_participant = False
        self._cb_participant_stopped_typing = cb_participant_stopped_typing
        self._task_emit: asyncio.Task | None = None
        self._debounce_s = debounce_s
        self._last_event_datetime = None

    def _is_valid_key(self, key: str):
        return key and (len(key) == 1 or key in [KEY_BACKSPACE, KEY_ENTER])

    def append(self, key: str):
        if not self._is_valid_key(key):
            return
        self.data.append(item=key)
        self._last_event_datetime = dt.datetime.now(dt.timezone.utc)
        self._debounce_emit()

    def resize(self, size: int):
        self.data.resize(max_size=size)

    def _debounce_emit(self):
        if self._task_emit:
            self._task_emit.cancel()

        async def delay_emit():
            await asyncio.sleep(self._debounce_s)
            await self._emit()

        self._task_emit = asyncio.create_task(delay_emit())

    async def _emit(self):
        try:
            self.data.append(self._last_event_datetime)
            if not self.is_bot_participant:
                await self._cb_participant_stopped_typing()
        except Exception as e:
            logger.exception("callback raised {e}", exc_info=e)
